// jianpu-editor/src/main.ts
import { Note, Score } from "./types";
import { JianpuSVGRenderer } from "./renderer";
import { MidiExporter } from "./midi";
import { listen } from "@tauri-apps/api/event";
import { invoke } from "@tauri-apps/api/core";
import { SelectionManager } from "./component/selection"; 
import { ShortcutManager } from "./component/shortcuts";
import { HistoryManager } from "./component/history";

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
const btnPageDown = document.getElementById("btn-page-down") as HTMLButtonElement;

// 初始化渲染器
const renderer = new JianpuSVGRenderer(svgElement);

// 核心基础状态
let selectedNoteId: number | null = null;
let editMode: "edit" | "select" = "edit";
let lastDuration: number = 1;

// 全量音符ID（实时同步乐谱）
let allNoteIds: number[] = [];

// 初始化测试数据
const testScore: Score = {
  title: "测试曲谱",
  tempo: 60,
  beatsPerBar: 4,
  notes: [],
};

// 加载乐谱
let score: Score = JSON.parse(JSON.stringify(testScore));

// ========== 新增：自动保存/加载功能（LocalStorage，零依赖，最简单） ==========
const STORAGE_KEY = "jianpu-current-score";

// 保存当前乐谱到本地
function saveScore(isManual: boolean = false): void {
  try {
    const saveData = JSON.stringify(score);
    localStorage.setItem(STORAGE_KEY, saveData);

    // 仅手动保存时显示提示
    if (isManual) {
      setStatus(`✅ 已成功保存: ${score.title || "简谱"}`);
    }
  } catch (err) {
    console.error("乐谱保存失败:", err);
    // 手动保存失败才提示错误，自动保存静默失败不打扰用户
    if (isManual) {
      setStatus("❌ 保存失败，请重试");
    }
  }
}

// 更新状态
function setStatus(msg: string): void {
  statusMsg.textContent = msg;
}

// 自动添加小节线
function autoAddBarLines(): void {
  score.notes = score.notes.filter((note) => note.value !== "bar");
  const beatsPerBar = score.beatsPerBar || 4;
  let currentBeat = 0;
  const newNotes = [];

  for (const note of score.notes) {
    newNotes.push(note);
    if (note.value !== "bar") {
      currentBeat += note.duration;
      if (currentBeat >= beatsPerBar) {
        const maxId =
          score.notes.length > 0
            ? Math.max(...score.notes.map((n) => n.id))
            : -1;
        newNotes.push({
          id: maxId + 1,
          value: "bar",
          octave: 0,
          type: null,
          duration: 0,
          dotted: false,
          ban: 0,
          yan: 0,
          lineBreak: false,
        });
        currentBeat = 0;
      }
    }
  }
  score.notes = newNotes;
  // 实时同步全量音符ID
  allNoteIds = score.notes.map((n) => n.id);
  // 更新选择管理器中的音符ID
  selectionManager.updateNoteIds(allNoteIds);
}

// 渲染（核心同步音符元素+高亮）
function render(): void {
  renderer.loadScore(score);
  renderer.render();
  updateNotePanel();
  // 每次渲染同步全量音符ID
  allNoteIds = score.notes.map((n) => n.id);
  // 更新选择管理器中的音符ID
  selectionManager.updateNoteIds(allNoteIds);
  // 缓存所有音符元素和位置（用于框选）
  selectionManager.cacheNoteElements();
}

// 更新音符编辑面板
function updateNotePanel(): void {
  const multiSelectedIds = selectionManager.getMultiSelectedIds();
  
  if (multiSelectedIds.length > 1) {
    noteEditing.innerHTML = `<p>已批量选中 ${multiSelectedIds.length} 个音符</p><p>可使用 Ctrl+C/V 复制粘贴 | Delete删除</p>`;
    return;
  }
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

// 更新音符
function updateNote(id: number, updates: Partial<Note>): void {
  const note = score.notes.find((n) => n.id === id);
  if (!note) return;
  saveHistory();
  if (updates.type === 99) {
    note.duration = score.beatsPerBar || 4;
  } else {
    const currentActualDuration = updates.type || note.type || 0;
    note.duration = updates.dotted
      ? currentActualDuration * 1.5
      : currentActualDuration;
  }
  Object.assign(note, updates);
  autoAddBarLines();
  render();
  setStatus(`已更新音符 ${id}, 时值: ${note.duration}拍`);
}

// 删除音符
function deleteNote(id: number): void {
  const index = score.notes.findIndex((n) => n.id === id);
  if (index === -1) return;
  saveHistory();
  score.notes.splice(index, 1);
  if (selectedNoteId === id) selectedNoteId = null;
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

  if (insertAfterId !== undefined) {
    const idx = score.notes.findIndex((n) => n.id === insertAfterId);
    idx !== -1
      ? score.notes.splice(idx + 1, 0, newNote)
      : score.notes.push(newNote);
  } else {
    score.notes.push(newNote);
  }

  if (note.value !== "bar") {
    lastDuration = note.duration;
  }
  autoAddBarLines();
  render();
  setStatus(`已添加音符 ${note.value} (时值: ${lastDuration}拍)`);
}

// 清空
function clear(): void {
  saveHistory();
  score.notes = [];
  selectedNoteId = null;
  selectionManager.clearSelection();
  autoAddBarLines();
  render();
  setStatus("已清空");
}

// 导入JSON
function importJson(): void {
  try {
    // 创建隐藏的文件输入框
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json,application/json";
    input.style.display = "none";
    document.body.appendChild(input);

    // 监听文件选择
    input.addEventListener("change", async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) {
        document.body.removeChild(input);
        return;
      }

      try {
        // 读取文件
        const text = await file.text();
        const importedScore = JSON.parse(text) as Score;

        // 简单校验
        if (!importedScore || !Array.isArray(importedScore.notes)) {
          setStatus("导入失败：JSON格式不正确");
          document.body.removeChild(input);
          return;
        }

        // 保存历史
        saveHistory();

        // 更新乐谱
        score = importedScore;
        selectedNoteId = null;
        selectionManager.clearSelection();
        
        // 更新管理器中的选中状态
        shortcutManager.updateSelectedNoteId(selectedNoteId);
        historyManager.updateSelectedNoteId(selectedNoteId);
        
        autoAddBarLines();
        render();

        setStatus(`已成功导入: ${importedScore.title || "简谱"}`);
      } catch (parseErr) {
        console.error("解析JSON失败:", parseErr);
        setStatus("导入失败：JSON解析错误");
      } finally {
        // 清理
        document.body.removeChild(input);
      }
    });

    // 触发文件选择
    input.click();
  } catch (err) {
    console.error("导入JSON失败:", err);
    setStatus("导入JSON失败，请重试");
  }
}

// 导出JSON
function exportJson(): void {
  try {
    const json = JSON.stringify(score, null, 2);
    const blob = new Blob([json], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `${score.title || "简谱"}.json`;

    // 关键修复1：必须显式加到DOM树里
    link.style.position = "fixed";
    link.style.left = "-9999px";
    link.style.top = "-9999px";
    document.body.appendChild(link);

    // 关键修复2：用更兼容的方式触发点击
    const clickEvent = new MouseEvent("click", {
      bubbles: true,
      cancelable: true,
      view: window,
    });
    link.dispatchEvent(clickEvent);

    // 关键修复3：延迟清理，确保点击事件执行完
    setTimeout(() => {
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }, 200);

    setStatus("已导出JSON");
  } catch (err) {
    console.error("导出JSON失败:", err);
    setStatus("导出JSON失败，请重试");
  }
}

// 导出MIDI
async function exportMidi(): Promise<void> {
  const exporter = new MidiExporter(score);
  await exporter.save(`${score.title || "简谱"}.mid`);
  setStatus("已导出MIDI");
}

// 应用初始化时自动加载上次保存的乐谱
function autoLoad(): void {
  try {
    const savedData = localStorage.getItem(STORAGE_KEY);
    if (!savedData) return;

    const loadedScore = JSON.parse(savedData) as Score;
    if (!loadedScore || !Array.isArray(loadedScore.notes)) return;

    // 加载保存的乐谱
    score = loadedScore;
    // 重置选中状态
    selectedNoteId = null;
    selectionManager.clearSelection();
    
    // 更新管理器中的选中状态
    shortcutManager.updateSelectedNoteId(selectedNoteId);
    historyManager.updateSelectedNoteId(selectedNoteId);

    setStatus("已自动加载上次保存的乐谱");
  } catch (err) {
    console.error("自动加载失败:", err);
  }
}

// 保存到历史
function saveHistory(): void {
  historyManager.saveHistory();
}

// 初始化选择管理器
let multiSelectedIds: number[] = [];

const selectionManager = new SelectionManager(
  svgElement,
  renderer,
  (selectedIds) => {
    // 选中状态变化回调
    multiSelectedIds = selectedIds;
  },
  (message) => {
    // 状态更新回调
    setStatus(message);
  },
  () => {
    // 音符面板更新回调
    updateNotePanel();
  }
);

// 初始化快捷键管理器
const shortcutManager = new ShortcutManager(
  score,
  selectedNoteId,
  selectionManager,
  saveHistory,
  autoAddBarLines,
  render,
  updateNotePanel,
  setStatus,
  updateNote
);

// 初始化历史记录管理器
const historyManager = new HistoryManager(
  score,
  selectedNoteId,
  selectionManager,
  render,
  setStatus,
  saveScore
);

// MIDI音符转简谱（C调）
function midiToJianpu(midiNote: number): { value: string; octave: number } {
  const relativeNote = midiNote - 60;
  const octave = Math.floor(relativeNote / 12);
  const noteInOctave = ((relativeNote % 12) + 12) % 12;

  const jianpuNotes = ["1", "2", "3", "4", "5", "6", "7"];
  const scaleIndex = [0, 2, 4, 5, 7, 9, 11];
  const noteIndex = scaleIndex.findIndex((s) => s === noteInOctave);

  if (noteIndex === -1) {
    if (noteInOctave === 1) return { value: "1", octave };
    if (noteInOctave === 3) return { value: "2", octave };
    if (noteInOctave === 6) return { value: "5", octave };
    if (noteInOctave === 8) return { value: "6", octave };
    if (noteInOctave === 10) return { value: "7", octave };
    return { value: "1", octave: 0 };
  }

  return { value: jianpuNotes[noteIndex], octave };
}

// 初始化MIDI输入
async function initMidi(): Promise<void> {
  const statusEl = document.getElementById("midi-status");
  if (!statusEl) return;

  try {
    const result = await invoke<string>("start_midi_listener");
    setStatus(result);
    statusEl.textContent = "监听中...";

    listen<{ note: number; velocity: number }>("midi-note", (event) => {
      const note = event.payload.note;
      const jianpu = midiToJianpu(note);
      const value = jianpu.value;

      if (!/^[0-7]$/.test(value)) {
        setStatus(`不支持的音符: MIDI ${note}`);
        return;
      }

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

// ========== 音符点击事件（单选+Shift连续多选） ==========
svgElement.addEventListener(
  "note-click",
  (e) => {
    // 框选过程中不触发单选
    const event = e as CustomEvent<{ noteId: number }>;
    const clickNoteId = event.detail.noteId;

    // Shift+点击：连续多选
    if ((e as MouseEvent).shiftKey && selectedNoteId !== null) {
      const startIdx = allNoteIds.indexOf(selectedNoteId);
      const endIdx = allNoteIds.indexOf(clickNoteId);
      if (startIdx !== -1 && endIdx !== -1) {
        const minIdx = Math.min(startIdx, endIdx);
        const maxIdx = Math.max(startIdx, endIdx);
        const selectedIds = allNoteIds.slice(minIdx, maxIdx + 1);
        selectionManager.setMultiSelectedIds(selectedIds);
        updateNotePanel();
        setStatus(`已选中 ${selectedIds.length} 个音符`);
        return;
      }
    }

    // 普通点击：单选
    selectionManager.clearSelection();
    selectedNoteId = clickNoteId;
    selectionManager.setSelectedNoteId(selectedNoteId);
    renderer.selectNote(selectedNoteId);
    updateNotePanel();
    setStatus(`已选择音符 ID:${selectedNoteId}, 时值: ${score.notes.find((n) => n.id === selectedNoteId)?.duration || 0}拍`);
    
    // 更新管理器中的选中状态
    shortcutManager.updateSelectedNoteId(selectedNoteId);
    historyManager.updateSelectedNoteId(selectedNoteId);
  },
  { capture: true },
);

// ========== 键盘事件（全兼容Win/Mac） ==========
window.addEventListener("keydown", (e) => {
  // 使用快捷键管理器处理快捷键
  shortcutManager.handleKeyDown(e);
  historyManager.handleKeyDown(e);

  // 编辑模式：数字键快速输入音符
  if (editMode === "edit") {
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
    // 快捷键切换属性
    if (e.key === "b" && selectedNoteId !== null) {
      const note = score.notes.find((n) => n.id === selectedNoteId);
      if (note) updateNote(selectedNoteId, { ban: note.ban ? 0 : 1 });
      e.preventDefault();
      return;
    }
    if (e.key === "y" && selectedNoteId !== null) {
      const note = score.notes.find((n) => n.id === selectedNoteId);
      if (note) updateNote(selectedNoteId, { yan: note.yan ? 0 : 1 });
      e.preventDefault();
      return;
    }
    if (e.key === "." && selectedNoteId !== null) {
      const note = score.notes.find((n) => n.id === selectedNoteId);
      if (note) updateNote(selectedNoteId, { dotted: !note.dotted });
      e.preventDefault();
      return;
    }
  }

  if (selectedNoteId === null) return;

  // 选择模式：方向键切换音符
  if (editMode === "select") {
    const currentIdx = allNoteIds.indexOf(selectedNoteId);
    if (e.key === "ArrowRight" && currentIdx < allNoteIds.length - 1) {
      selectedNoteId = allNoteIds[currentIdx + 1];
      selectionManager.clearSelection();
      renderer.selectNote(selectedNoteId);
      updateNotePanel();
      setStatus(`已选择音符 ID:${selectedNoteId}`);
      
      // 更新管理器中的选中状态
      shortcutManager.updateSelectedNoteId(selectedNoteId);
      historyManager.updateSelectedNoteId(selectedNoteId);
      
      e.preventDefault();
    }
    if (e.key === "ArrowLeft" && currentIdx > 0) {
      selectedNoteId = allNoteIds[currentIdx - 1];
      selectionManager.clearSelection();
      renderer.selectNote(selectedNoteId);
      updateNotePanel();
      setStatus(`已选择音符 ID:${selectedNoteId}`);
      
      // 更新管理器中的选中状态
      shortcutManager.updateSelectedNoteId(selectedNoteId);
      historyManager.updateSelectedNoteId(selectedNoteId);
      
      e.preventDefault();
    }
  } else {
    // 编辑模式：上下调整八度
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

// 初始化
autoLoad();
autoAddBarLines();
render();
setStatus("就绪 - 点击选中音符 | 按住鼠标/触摸板拖动可框选多个音符");

// 原有按钮绑定
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
document.getElementById("btn-undo")?.addEventListener("click", () => historyManager.undo());
document.getElementById("btn-redo")?.addEventListener("click", () => historyManager.redo());
document
  .getElementById("btn-save-manual")
  ?.addEventListener("click", () => saveScore(true));
document
  .getElementById("btn-import-json")
  ?.addEventListener("click", importJson);
document
  .getElementById("btn-export-json")
  ?.addEventListener("click", exportJson);
document
  .getElementById("btn-export-midi")
  ?.addEventListener("click", exportMidi);
document
  .getElementById("btn-midi-in")
  ?.addEventListener("click", () => initMidi());

noteInput?.addEventListener("change", () => {
  lastDuration = parseFloat(noteInput.value);
  setStatus(`已设定音符为 ${lastDuration} 拍`);
});

titleInput?.addEventListener("change", () => {
  score.title = titleInput.value;
});
tempoInput?.addEventListener("change", () => {
  score.tempo = parseInt(tempoInput.value) || 60;
});
beatsInput?.addEventListener("change", () => {
  score.beatsPerBar = parseInt(beatsInput.value) || 4;
});

// 翻页按钮
btnPageUp?.addEventListener("click", () => {
  const notesPerRow = Math.floor((svgElement.width.baseVal.value - 80) / 40);
  const rowsPerPage = Math.floor(svgElement.height.baseVal.value / 80);
  const step = rowsPerPage * notesPerRow;
  const currentIdx =
    selectedNoteId !== null ? allNoteIds.indexOf(selectedNoteId) : -1;
  const newIdx = Math.max(0, currentIdx - step);
  if (allNoteIds.length > 0) {
    selectedNoteId = allNoteIds[newIdx];
    selectionManager.clearSelection();
    
    // 更新管理器中的选中状态
    shortcutManager.updateSelectedNoteId(selectedNoteId);
    historyManager.updateSelectedNoteId(selectedNoteId);
  }
  render();
  if (selectedNoteId !== null) setStatus(`已选择音符 ID:${selectedNoteId}`);
});

btnPageDown?.addEventListener("click", () => {
  const rowsPerPage = Math.floor(svgElement.height.baseVal.value / 80);
  const step =
    rowsPerPage * Math.floor((svgElement.width.baseVal.value - 80) / 40);
  const currentIdx =
    selectedNoteId !== null ? allNoteIds.indexOf(selectedNoteId) : -1;
  const newIdx = Math.min(allNoteIds.length - 1, currentIdx + step);
  if (allNoteIds.length > 0) {
    selectedNoteId = allNoteIds[newIdx];
    selectionManager.clearSelection();
    
    // 更新管理器中的选中状态
    shortcutManager.updateSelectedNoteId(selectedNoteId);
    historyManager.updateSelectedNoteId(selectedNoteId);
  }
  render();
  if (selectedNoteId !== null) setStatus(`已选择音符 ID:${selectedNoteId}`);
});
