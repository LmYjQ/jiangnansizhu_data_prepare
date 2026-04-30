import { Note, Score } from "./types";
import { JianpuSVGRenderer } from "./renderer";
import { MidiExporter } from "./midi";
import { listen } from "@tauri-apps/api/event";
import { invoke } from "@tauri-apps/api/core";

// 获取DOM元素
const svgElementRaw = document.getElementById("score-svg");
if (!(svgElementRaw instanceof SVGSVGElement)) {
  throw new Error('Element with id "score-svg" is not an SVGSVGElement.');
}
const svgElement = svgElementRaw;
const titleInput = document.getElementById("title-input") as HTMLInputElement;
const tempoInput = document.getElementById("tempo-input") as HTMLInputElement;
const beatsInput = document.getElementById("beats-input") as HTMLInputElement;
const noteInput = document.getElementById("note‌-input") as HTMLSelectElement;

const statusMsg = document.getElementById("status-msg") as HTMLElement;
const noteEditing = document.getElementById("note-editing") as HTMLElement;
const btnPageUp = document.getElementById("btn-page-up") as HTMLButtonElement;
const btnPageDown = document.getElementById(
  "btn-page-down",
) as HTMLButtonElement;

// 初始化渲染器
const renderer = new JianpuSVGRenderer(svgElement);

// 当前选中的音符ID
let selectedNoteId: number | null = null;

// 编辑模式: 'edit'=编辑面板, 'select'=选择模式(键盘导航)
let editMode: "edit" | "select" = "edit";

// 上一个输入音符的时值（用于连续输入）
let lastDuration: number = 1;

// MIDI音符转简谱（C调）
// MIDI音符60 = 中央C = 简谱1（中音）
function midiToJianpu(midiNote: number): { value: string; octave: number } {
  // MIDI 60 = 1（中音），每12个半音一个八度
  const relativeNote = midiNote - 60;
  const octave = Math.floor(relativeNote / 12);
  const noteInOctave = ((relativeNote % 12) + 12) % 12;

  // C大调音阶映射
  const jianpuNotes = ["1", "2", "3", "4", "5", "6", "7"];
  const scaleIndex = [0, 2, 4, 5, 7, 9, 11];
  const noteIndex = scaleIndex.findIndex((s) => s === noteInOctave);

  if (noteIndex === -1) {
    // 升降音处理
    if (noteInOctave === 1) return { value: "1", octave }; // #1 -> 1
    if (noteInOctave === 3) return { value: "2", octave }; // #2 -> 2
    if (noteInOctave === 6) return { value: "5", octave }; // #5 -> 5
    if (noteInOctave === 8) return { value: "6", octave }; // #6 -> 6
    if (noteInOctave === 10) return { value: "7", octave }; // #7 -> 7
    return { value: "1", octave: 0 };
  }

  return { value: jianpuNotes[noteIndex], octave };
}

// 初始化MIDI输入
async function initMidi(): Promise<void> {
  const statusEl = document.getElementById("midi-status");
  if (!statusEl) return;

  try {
    // 先启动 MIDI 监听
    const result = await invoke<string>("start_midi_listener");
    setStatus(result);
    statusEl.textContent = "监听中...";

    // 然后监听事件（不等待）
    listen<{ note: number; velocity: number }>("midi-note", (event) => {
      const note = event.payload.note;
      const jianpu = midiToJianpu(note);
      const value = jianpu.value;

      // 跳过非音符值
      if (!/^[0-7]$/.test(value)) {
        setStatus(`不支持的音符: MIDI ${note}`);
        return;
      }

      // 插入音符
      addNote(
        {
          value,
          octave: jianpu.octave,
          type: lastDuration,
          duration: lastDuration,
          dotted: false,
          ban: 0,
          yan: 0,
          lineBreak: false,
        },
        selectedNoteId ?? undefined,
      );
    });

    listen<string>("midi-connected", (event) => {
      const statusEl = document.getElementById("midi-status");
      if (statusEl) {
        statusEl.textContent = event.payload;
        statusEl.className = "midi-status connected";
      }
      setStatus(`MIDI已连接: ${event.payload}`);
    });

    listen<string>("midi-error", (event) => {
      const statusEl = document.getElementById("midi-status");
      if (statusEl) {
        statusEl.textContent = "连接失败";
        statusEl.className = "midi-status error";
      }
      setStatus(`MIDI错误: ${event.payload}`);
    });
  } catch (err) {
    console.error("MIDI初始化失败:", err);
    statusEl.textContent = "初始化失败";
    statusEl.className = "midi-status error";
    setStatus("MIDI初始化失败");
  }
}

// 初始化测试数据
const testScore: Score = {
  title: "测试曲谱",
  tempo: 60,
  beatsPerBar: 4,
  notes: [
    // {
    //   id: 0,
    //   value: "1",
    //   octave: 0,
    //   duration: 1,
    //   dotted: false,
    //   ban: 0,
    //   yan: 0,
    //   lineBreak: false,
    // },
  ],
};

/**
 * 自动添加小节线
 */
function autoAddBarLines(): void {
  // 移除所有现有的小节线
  score.notes = score.notes.filter((note) => note.value !== "bar");

  // 计算每小节应该包含的拍数
  const beatsPerBar = score.beatsPerBar || 4;

  // 遍历音符，计算累计拍数
  let currentBeat = 0;
  const newNotes = [];

  for (const note of score.notes) {
    newNotes.push(note);

    // 只计算音符和空格，不计算小节线
    if (note.value !== "bar") {
      currentBeat += note.duration;

      // 如果累计拍数达到或超过每小节拍数，添加小节线
      if (currentBeat >= beatsPerBar) {
        // 创建小节线
        const maxId =
          score.notes.length > 0
            ? Math.max(...score.notes.map((n) => n.id))
            : -1;
        const barLine = {
          id: maxId + 1,
          value: "bar",
          octave: 0,
          type: null,
          duration: 0,
          dotted: false,
          ban: 0,
          yan: 0,
          lineBreak: false,
        };
        newNotes.push(barLine);

        // 重置累计拍数
        currentBeat = 0;
      }
    }
  }

  // 更新乐谱
  score.notes = newNotes;
}

// 加载乐谱
let score: Score = JSON.parse(JSON.stringify(testScore));
let history: Score[] = [JSON.parse(JSON.stringify(score))];
let historyIndex: number = 0;

// 渲染
function render(): void {
  renderer.loadScore(score);
  renderer.render();
  updateNotePanel();
}

// 更新状态
function setStatus(msg: string): void {
  statusMsg.textContent = msg;
}

// 更新音符编辑面板
function updateNotePanel(): void {
  if (selectedNoteId === null) {
    noteEditing.innerHTML = "<p>请在画布上点击选择音符</p>";
    return;
  }

  const note = score.notes.find((n) => n.id === selectedNoteId);
  if (!note) {
    noteEditing.innerHTML = "<p>音符不存在</p>";
    return;
  }
  noteEditing.innerHTML = `
    <div class="note-edit-form">
      <p>音符 ID: ${note.id}</p>
      <label>音名: <select id="edit-value">
        <option value="1" ${note.value === "1" ? "selected" : ""}>1</option>
        <option value="2" ${note.value === "2" ? "selected" : ""}>2</option>
        <option value="3" ${note.value === "3" ? "selected" : ""}>3</option>
        <option value="4" ${note.value === "4" ? "selected" : ""}>4</option>
        <option value="5" ${note.value === "5" ? "selected" : ""}>5</option>
        <option value="6" ${note.value === "6" ? "selected" : ""}>6</option>
        <option value="7" ${note.value === "7" ? "selected" : ""}>7</option>
        <option value="0" ${note.value === "0" ? "selected" : ""}>0 休止</option>
        <option value="bar" ${note.value === "bar" ? "selected" : ""}>小节线</option>
        <option value="space" ${note.value === "space" ? "selected" : ""}>空格</option>
      </select></label>
      <label>八度: <input type="number" id="edit-octave" value="${note.octave}" min="-2" max="2" style="width:50px"></label>
      <label>音符类型: <select id="edit-node">
        <option value="99" ${note.type === 99 ? "selected" : ""}>全音符</option>
        <option value="2" ${note.type === 2 ? "selected" : ""}>二分音符</option>
        <option value="1" ${note.type === 1 ? "selected" : ""}>四分音符</option>
        <option value="0.5" ${note.type === 0.5 ? "selected" : ""}>八分音符</option>
        <option value="0.25" ${note.type === 0.25 ? "selected" : ""}>十六分音符</option>
        <option value="0.125" ${note.type === 0.125 ? "selected" : ""}>三十二分音符</option>
      </select></label>
      <label>附点: <input type="checkbox" id="edit-dotted" ${note.dotted ? "checked" : ""}></label>
      <label>板: <input type="checkbox" id="edit-ban" ${note.ban === 1 ? "checked" : ""}></label>
      <label>眼: <input type="checkbox" id="edit-yan" ${note.yan === 1 ? "checked" : ""}></label>
      <label>分页符: <input type="checkbox" id="edit-linebreak" ${note.lineBreak ? "checked" : ""}></label>
      <div class="btn-group">
        <button id="btn-delete-note">删除</button>
      </div>
    </div>
  `;

  // 绑定编辑事件
  document.getElementById("edit-value")?.addEventListener("change", (e) => {
    const value = (e.target as HTMLSelectElement).value;
    updateNote(selectedNoteId!, { value });
  });
  document.getElementById("edit-octave")?.addEventListener("change", (e) => {
    const octave = parseInt((e.target as HTMLInputElement).value);
    updateNote(selectedNoteId!, { octave });
  });
  document.getElementById("edit-node")?.addEventListener("change", (e) => {
    const type = parseFloat((e.target as HTMLSelectElement).value);
    updateNote(selectedNoteId!, { type });
  });
  document.getElementById("edit-dotted")?.addEventListener("change", (e) => {
    const dotted = (e.target as HTMLInputElement).checked;
    updateNote(selectedNoteId!, { dotted });
  });
  document.getElementById("edit-ban")?.addEventListener("change", (e) => {
    const ban = (e.target as HTMLInputElement).checked ? 1 : 0;
    updateNote(selectedNoteId!, { ban });
  });
  document.getElementById("edit-yan")?.addEventListener("change", (e) => {
    const yan = (e.target as HTMLInputElement).checked ? 1 : 0;
    updateNote(selectedNoteId!, { yan });
  });
  document.getElementById("edit-linebreak")?.addEventListener("change", (e) => {
    const lineBreak = (e.target as HTMLInputElement).checked;
    updateNote(selectedNoteId!, { lineBreak });
  });
  document.getElementById("btn-delete-note")?.addEventListener("click", () => {
    deleteNote(selectedNoteId!);
  });
}

// 保存到历史
function saveHistory(): void {
  history = history.slice(0, historyIndex + 1);
  history.push(JSON.parse(JSON.stringify(score)));
  if (history.length > 50) {
    history.shift();
  }
  historyIndex = history.length - 1;
}

// 撤销
function undo(): void {
  if (historyIndex > 0) {
    historyIndex--;
    score = JSON.parse(JSON.stringify(history[historyIndex]));
    selectedNoteId = null;
    render();
    setStatus("已撤销");
  }
}

// 重做
function redo(): void {
  if (historyIndex < history.length - 1) {
    historyIndex++;
    score = JSON.parse(JSON.stringify(history[historyIndex]));
    selectedNoteId = null;
    render();
    setStatus("已重做");
  }
}

// 更新音符
function updateNote(id: number, updates: Partial<Note>): void {
  const note = score.notes.find((n) => n.id === id);
  if (!note) return;
  saveHistory();
  if (updates.type === 99) {
    note.duration = score.beatsPerBar || 4;
  } else {
    // 计算当前的实际时长
    const currentActualDuration = note.type || 0;

    if (updates.dotted) {
      note.duration = currentActualDuration * 1.5;
    } else {
      note.duration = currentActualDuration;
    }
  }

  // 应用其他更新
  Object.assign(note, updates);

  // 自动添加小节线
  autoAddBarLines();

  render();
  setStatus(`已更新音符 ${id}`);
}

// 删除音符
function deleteNote(id: number): void {
  const index = score.notes.findIndex((n) => n.id === id);
  if (index === -1) return;
  saveHistory();
  score.notes.splice(index, 1);
  if (selectedNoteId === id) selectedNoteId = null;

  // 自动添加小节线
  autoAddBarLines();

  render();
  setStatus("已删除音符");
}

// 添加音符
function addNote(note: Omit<Note, "id">, insertAfterId?: number): void {
  saveHistory();
  const maxId =
    score.notes.length > 0 ? Math.max(...score.notes.map((n) => n.id)) : -1;
  const newNote = { ...note, id: maxId + 1 };

  // 如果指定了插入位置，在该音符后面插入
  if (insertAfterId !== undefined) {
    const idx = score.notes.findIndex((n) => n.id === insertAfterId);
    if (idx !== -1) {
      score.notes.splice(idx + 1, 0, newNote);
    } else {
      score.notes.push(newNote);
    }
  } else {
    score.notes.push(newNote);
  }

  // 更新时值记忆（音符和空格记时值，小节线不记）
  if (note.value !== "bar") {
    lastDuration = note.duration;
  }

  // 自动添加小节线
  autoAddBarLines();

  render();
  setStatus(`已添加音符 ${note.value} (时值: ${lastDuration}拍)`);
}

// 清空
function clear(): void {
  console.log("clear");
  // if (confirm("确定要清空所有音符吗？")) {
    saveHistory(); // 取消注释：清空操作也保存到历史，支持撤销
    score.notes = []; // 清空所有音符
    selectedNoteId = null; // 重置选中状态
    autoAddBarLines(); // 虽然是空的，但确保没有遗留的小节线
    render(); // 重新渲染
    setStatus("已清空");
  // }
}

// 导出JSON
function exportJson(): void {
  const json = JSON.stringify(score, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.download = `${score.title || "简谱"}.json`;
  link.href = url;
  link.click();
  URL.revokeObjectURL(url);
  setStatus("已导出JSON");
}

// 导出MIDI
async function exportMidi(): Promise<void> {
  const exporter = new MidiExporter(score);
  await exporter.save(`${score.title || "简谱"}.mid`);
  setStatus("已导出MIDI");
}

// 初始化
autoAddBarLines();
render();
setStatus("就绪 - 点击音符可编辑");

// 模式切换
document.getElementById("btn-mode")?.addEventListener("click", () => {
  editMode = editMode === "edit" ? "select" : "edit";
  const btn = document.getElementById("btn-mode");
  if (btn) {
    btn.textContent = editMode === "edit" ? "编辑模式" : "选择模式";
    btn.style.background = editMode === "edit" ? "#e8e8e8" : "#ffecb3";
  }
  setStatus(
    editMode === "edit"
      ? "编辑模式：方向键调整八度/时值"
      : "选择模式：方向键切换音符",
  );
});

document.getElementById("btn-clear")?.addEventListener("click", clear);
document.getElementById("btn-undo")?.addEventListener("click", undo);
document.getElementById("btn-redo")?.addEventListener("click", redo);
document
  .getElementById("btn-export-json")
  ?.addEventListener("click", exportJson);
document
  .getElementById("btn-export-midi")
  ?.addEventListener("click", exportMidi);

// MIDI输入按钮
document.getElementById("btn-midi-in")?.addEventListener("click", () => {
  initMidi();
});

// 添加音符输入变更事件
noteInput?.addEventListener("change", () => {
  lastDuration = parseFloat(noteInput.value);
  setStatus(`已设定音符为 ${lastDuration} 拍`);
});

// 曲名/速度/拍数变更
titleInput?.addEventListener("change", () => {
  score.title = titleInput.value;
});

tempoInput?.addEventListener("change", () => {
  score.tempo = parseInt(tempoInput.value) || 60;
});

beatsInput?.addEventListener("change", () => {
  score.beatsPerBar = parseInt(beatsInput.value) || 4;
});

// 键盘事件
window.addEventListener("keydown", (e) => {
  // console.log(e.key);
  // Ctrl+Z 撤销
  if (e.ctrlKey && e.key === "z") {
    undo();
    e.preventDefault();
  }
  // Ctrl+Y 重做
  if (e.ctrlKey && e.key === "y") {
    redo();
    e.preventDefault();
  }
  // Delete 删除选中音符
  if (
    (e.key === "Delete" || e.key === "Backspace") &&
    selectedNoteId !== null
  ) {
    deleteNote(selectedNoteId);
    e.preventDefault();
  }

  // 编辑模式下：数字键/空格/b 快速输入
  if (editMode === "edit") {
    // 数字 0-7 输入音符（插入到选中音符后面）
    if (/^[0-7]$/.test(e.key)) {
      addNote(
        {
          value: e.key,
          octave: 0,
          type: lastDuration,
          duration: lastDuration === 99 ? score.beatsPerBar : lastDuration,
          dotted: false,
          ban: 0,
          yan: 0,
          lineBreak: false,
        },
        selectedNoteId ?? undefined,
      );
      e.preventDefault();
      return;
    }
    // b键切换板（需选中音符）
    if (e.key === "b" && selectedNoteId !== null) {
      const note = score.notes.find((n) => n.id === selectedNoteId);
      if (note) {
        updateNote(selectedNoteId, { ban: note.ban === 1 ? 0 : 1 });
      }
      e.preventDefault();
      return;
    }

    // y键切换眼（需要选中音符）
    if (e.key === "y" && selectedNoteId !== null) {
      const note = score.notes.find((n) => n.id === selectedNoteId);
      if (note) {
        updateNote(selectedNoteId, { yan: note.yan === 1 ? 0 : 1 });
      }
      e.preventDefault();
      return;
    }
    // .键切换附点（需要选中音符）
    if (e.key === "." && selectedNoteId !== null) {
      const note = score.notes.find((n) => n.id === selectedNoteId);
      if (note) {
        updateNote(selectedNoteId, { dotted: !note.dotted });
      }
      e.preventDefault();
      return;
    }
  }

  // 方向键处理
  if (selectedNoteId === null) return;

  if (editMode === "select") {
    // 选择模式：左右切换选中音符
    const noteIds = score.notes.map((n) => n.id);
    const currentIdx = noteIds.indexOf(selectedNoteId);
    if (e.key === "ArrowRight" && currentIdx < noteIds.length - 1) {
      selectedNoteId = noteIds[currentIdx + 1];
      render();
      setStatus(`已选择音符 ID:${selectedNoteId}`);
      e.preventDefault();
    }
    if (e.key === "ArrowLeft" && currentIdx > 0) {
      selectedNoteId = noteIds[currentIdx - 1];
      render();
      setStatus(`已选择音符 ID:${selectedNoteId}`);
      e.preventDefault();
    }
  } else {
    // 编辑模式：上下调整八度，左右调整时值
    const note = score.notes.find((n) => n.id === selectedNoteId);
    if (!note) return;

    if (e.key === "ArrowUp") {
      updateNote(selectedNoteId, { octave: Math.min(2, note.octave + 1) });
      e.preventDefault();
    }
    if (e.key === "ArrowDown") {
      updateNote(selectedNoteId, { octave: Math.max(-2, note.octave - 1) });
      e.preventDefault();
    }
  }
});

// 监听音符点击事件
svgElement.addEventListener("note-click", (e) => {
  const event = e as CustomEvent<{ noteId: number }>;
  selectedNoteId = event.detail.noteId;
  renderer.selectNote(selectedNoteId);
  updateNotePanel();
  setStatus(`已选择音符 ID:${selectedNoteId}`);
});

btnPageUp?.addEventListener("click", () => {
  const notesPerRow = Math.floor((svgElement.width.baseVal.value - 80) / 40);
  const rowsPerPage = Math.floor(svgElement.height.baseVal.value / 80);
  const step = rowsPerPage * notesPerRow;
  const noteIds = score.notes.map((n) => n.id);
  const currentIdx =
    selectedNoteId !== null ? noteIds.indexOf(selectedNoteId) : -1;
  const newIdx = Math.max(0, currentIdx - step);
  if (noteIds.length > 0) {
    selectedNoteId = noteIds[newIdx];
  }
  render();
  if (selectedNoteId !== null) setStatus(`已选择音符 ID:${selectedNoteId}`);
});

btnPageDown?.addEventListener("click", () => {
  const rowsPerPage = Math.floor(svgElement.height.baseVal.value / 80);
  const noteIds = score.notes.map((n) => n.id);
  const currentIdx =
    selectedNoteId !== null ? noteIds.indexOf(selectedNoteId) : -1;
  const step =
    rowsPerPage * Math.floor((svgElement.width.baseVal.value - 80) / 40);
  const newIdx = Math.min(noteIds.length - 1, currentIdx + step);
  if (noteIds.length > 0) {
    selectedNoteId = noteIds[newIdx];
  }
  render();
  if (selectedNoteId !== null) setStatus(`已选择音符 ID:${selectedNoteId}`);
});
