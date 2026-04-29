import { Note, Score } from './types';
import { JianpuRenderer } from './renderer';
import { MidiExporter } from './midi';

// 获取DOM元素
const canvas = document.getElementById('score-canvas') as HTMLCanvasElement;
const titleInput = document.getElementById('title-input') as HTMLInputElement;
const tempoInput = document.getElementById('tempo-input') as HTMLInputElement;
const beatsInput = document.getElementById('beats-input') as HTMLInputElement;
const statusMsg = document.getElementById('status-msg') as HTMLElement;
const noteEditing = document.getElementById('note-editing') as HTMLElement;
const scrollBar = document.getElementById('scroll-bar') as HTMLInputElement;
const pageInfo = document.getElementById('page-info') as HTMLElement;
const btnPageUp = document.getElementById('btn-page-up') as HTMLButtonElement;
const btnPageDown = document.getElementById('btn-page-down') as HTMLButtonElement;

// 初始化渲染器
const renderer = new JianpuRenderer(canvas);

// 当前选中的音符ID
let selectedNoteId: number | null = null;

// 编辑模式: 'edit'=编辑面板, 'select'=选择模式(键盘导航)
let editMode: 'edit' | 'select' = 'edit';

// 上一个输入音符的时值（用于连续输入）
let lastDuration: number = 1;

// 初始化测试数据
const testScore: Score = {
  title: '测试曲谱',
  tempo: 60,
  beatsPerBar: 4,
  notes: [
    { id: 0, value: '1', octave: 0, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 1, value: '2', octave: 0, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 2, value: '3', octave: 0, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 3, value: '1', octave: 0, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 4, value: 'bar', octave: 0, duration: 0, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 5, value: '5', octave: 0, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 6, value: '5', octave: 0, duration: 0.5, dotted: true, ban: 0, yan: 0, lineBreak: false },
    { id: 7, value: '6', octave: 0, duration: 0.5, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 8, value: 'bar', octave: 0, duration: 0, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 9, value: '1', octave: 1, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 10, value: '1', octave: -1, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 11, value: 'space', octave: 0, duration: 0.5, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 12, value: '2', octave: 0, duration: 0.25, dotted: false, ban: 0, yan: 0, lineBreak: false },
    { id: 13, value: '3', octave: 0, duration: 0.125, dotted: false, ban: 0, yan: 0, lineBreak: false },
  ],
};

// 加载乐谱
let score: Score = JSON.parse(JSON.stringify(testScore));
let history: Score[] = [JSON.parse(JSON.stringify(score))];
let historyIndex: number = 0;

// 渲染
function render(): void {
  renderer.loadScore(score);
  renderer.render();
  updateNotePanel();
  updateScrollBar();
}

// 更新状态
function setStatus(msg: string): void {
  statusMsg.textContent = msg;
}

// 更新音符编辑面板
function updateNotePanel(): void {
  if (selectedNoteId === null) {
    noteEditing.innerHTML = '<p>请在画布上点击选择音符</p>';
    return;
  }

  const note = score.notes.find(n => n.id === selectedNoteId);
  if (!note) {
    noteEditing.innerHTML = '<p>音符不存在</p>';
    return;
  }

  noteEditing.innerHTML = `
    <div class="note-edit-form">
      <p>音符 ID: ${note.id}</p>
      <label>类型: <select id="edit-value">
        <option value="1" ${note.value === '1' ? 'selected' : ''}>1</option>
        <option value="2" ${note.value === '2' ? 'selected' : ''}>2</option>
        <option value="3" ${note.value === '3' ? 'selected' : ''}>3</option>
        <option value="4" ${note.value === '4' ? 'selected' : ''}>4</option>
        <option value="5" ${note.value === '5' ? 'selected' : ''}>5</option>
        <option value="6" ${note.value === '6' ? 'selected' : ''}>6</option>
        <option value="7" ${note.value === '7' ? 'selected' : ''}>7</option>
        <option value="0" ${note.value === '0' ? 'selected' : ''}>0 休止</option>
        <option value="bar" ${note.value === 'bar' ? 'selected' : ''}>小节线</option>
        <option value="space" ${note.value === 'space' ? 'selected' : ''}>空格</option>
      </select></label>
      <label>八度: <input type="number" id="edit-octave" value="${note.octave}" min="-2" max="2" style="width:50px"></label>
      <label>时值: <select id="edit-duration">
        <option value="4" ${note.duration === 4 ? 'selected' : ''}>4 拍</option>
        <option value="3" ${note.duration === 3 ? 'selected' : ''}>3 拍</option>
        <option value="2" ${note.duration === 2 ? 'selected' : ''}>2 拍</option>
        <option value="1" ${note.duration === 1 ? 'selected' : ''}>1 拍</option>
        <option value="0.5" ${note.duration === 0.5 ? 'selected' : ''}>1/2 拍</option>
        <option value="0.25" ${note.duration === 0.25 ? 'selected' : ''}>1/4 拍</option>
        <option value="0.125" ${note.duration === 0.125 ? 'selected' : ''}>1/8 拍</option>
      </select></label>
      <label>附点: <input type="checkbox" id="edit-dotted" ${note.dotted ? 'checked' : ''}></label>
      <label>板: <input type="checkbox" id="edit-ban" ${note.ban === 1 ? 'checked' : ''}></label>
      <label>眼: <input type="checkbox" id="edit-yan" ${note.yan === 1 ? 'checked' : ''}></label>
      <label>分页符: <input type="checkbox" id="edit-linebreak" ${note.lineBreak ? 'checked' : ''}></label>
      <div class="btn-group">
        <button id="btn-delete-note">删除</button>
      </div>
    </div>
  `;

  // 绑定编辑事件
  document.getElementById('edit-value')?.addEventListener('change', (e) => {
    const value = (e.target as HTMLSelectElement).value;
    updateNote(selectedNoteId!, { value });
  });
  document.getElementById('edit-octave')?.addEventListener('change', (e) => {
    const octave = parseInt((e.target as HTMLInputElement).value);
    updateNote(selectedNoteId!, { octave });
  });
  document.getElementById('edit-duration')?.addEventListener('change', (e) => {
    const duration = parseFloat((e.target as HTMLSelectElement).value);
    updateNote(selectedNoteId!, { duration });
  });
  document.getElementById('edit-dotted')?.addEventListener('change', (e) => {
    const dotted = (e.target as HTMLInputElement).checked;
    updateNote(selectedNoteId!, { dotted });
  });
  document.getElementById('edit-ban')?.addEventListener('change', (e) => {
    const ban = (e.target as HTMLInputElement).checked ? 1 : 0;
    updateNote(selectedNoteId!, { ban });
  });
  document.getElementById('edit-yan')?.addEventListener('change', (e) => {
    const yan = (e.target as HTMLInputElement).checked ? 1 : 0;
    updateNote(selectedNoteId!, { yan });
  });
  document.getElementById('edit-linebreak')?.addEventListener('change', (e) => {
    const lineBreak = (e.target as HTMLInputElement).checked;
    updateNote(selectedNoteId!, { lineBreak });
  });
  document.getElementById('btn-delete-note')?.addEventListener('click', () => {
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
    setStatus('已撤销');
  }
}

// 重做
function redo(): void {
  if (historyIndex < history.length - 1) {
    historyIndex++;
    score = JSON.parse(JSON.stringify(history[historyIndex]));
    selectedNoteId = null;
    render();
    setStatus('已重做');
  }
}

// 更新音符
function updateNote(id: number, updates: Partial<Note>): void {
  const note = score.notes.find(n => n.id === id);
  if (!note) return;
  saveHistory();
  Object.assign(note, updates);
  render();
  setStatus(`已更新音符 ${id}`);
}

// 删除音符
function deleteNote(id: number): void {
  const index = score.notes.findIndex(n => n.id === id);
  if (index === -1) return;
  saveHistory();
  score.notes.splice(index, 1);
  if (selectedNoteId === id) selectedNoteId = null;
  render();
  setStatus('已删除音符');
}

// 添加音符
function addNote(note: Omit<Note, 'id'>, insertAfterId?: number): void {
  saveHistory();
  const maxId = score.notes.length > 0 ? Math.max(...score.notes.map(n => n.id)) : -1;
  const newNote = { ...note, id: maxId + 1 };

  // 如果指定了插入位置，在该音符后面插入
  if (insertAfterId !== undefined) {
    const idx = score.notes.findIndex(n => n.id === insertAfterId);
    if (idx !== -1) {
      score.notes.splice(idx + 1, 0, newNote);
    } else {
      score.notes.push(newNote);
    }
  } else {
    score.notes.push(newNote);
  }

  // 更新时值记忆（音符和空格记时值，小节线不记）
  if (note.value !== 'bar') {
    lastDuration = note.duration;
  }
  render();
  setStatus(`已添加音符 ${note.value} (时值: ${lastDuration}拍)`);
}

// 清空
function clear(): void {
  if (confirm('确定要清空所有音符吗？')) {
    saveHistory();
    score.notes = [];
    selectedNoteId = null;
    render();
    setStatus('已清空');
  }
}

// 导出JSON
function exportJson(): void {
  const json = JSON.stringify(score, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.download = `${score.title || '简谱'}.json`;
  link.href = url;
  link.click();
  URL.revokeObjectURL(url);
  setStatus('已导出JSON');
}

// 导出PNG
async function exportPng(): Promise<void> {
  await renderer.saveImage(`${score.title || '简谱'}.png`);
  setStatus('已导出PNG');
}

// 导出MIDI
async function exportMidi(): Promise<void> {
  const exporter = new MidiExporter(score);
  await exporter.save(`${score.title || '简谱'}.mid`);
  setStatus('已导出MIDI');
}

// 初始化
render();
updateScrollBar();
setStatus('就绪 - 点击音符可编辑');

// 工具栏事件
document.getElementById('btn-add-note')?.addEventListener('click', () => {
  addNote({ value: '1', octave: 0, duration: 1, dotted: false, ban: 0, yan: 0, lineBreak: false });
});

document.getElementById('btn-add-bar')?.addEventListener('click', () => {
  addNote({ value: 'bar', octave: 0, duration: 0, dotted: false, ban: 0, yan: 0, lineBreak: false });
});

document.getElementById('btn-add-space')?.addEventListener('click', () => {
  addNote({ value: 'space', octave: 0, duration: 0.5, dotted: false, ban: 0, yan: 0, lineBreak: false });
});

// 模式切换
document.getElementById('btn-mode')?.addEventListener('click', () => {
  editMode = editMode === 'edit' ? 'select' : 'edit';
  const btn = document.getElementById('btn-mode');
  if (btn) {
    btn.textContent = editMode === 'edit' ? '编辑模式' : '选择模式';
    btn.style.background = editMode === 'edit' ? '#e8e8e8' : '#ffecb3';
  }
  setStatus(editMode === 'edit' ? '编辑模式：方向键调整八度/时值' : '选择模式：方向键切换音符');
});

document.getElementById('btn-clear')?.addEventListener('click', clear);
document.getElementById('btn-undo')?.addEventListener('click', undo);
document.getElementById('btn-redo')?.addEventListener('click', redo);
document.getElementById('btn-export-json')?.addEventListener('click', exportJson);
document.getElementById('btn-export-png')?.addEventListener('click', exportPng);
document.getElementById('btn-export-midi')?.addEventListener('click', exportMidi);

// 曲名/速度/拍数变更
titleInput?.addEventListener('change', () => {
  score.title = titleInput.value;
});

tempoInput?.addEventListener('change', () => {
  score.tempo = parseInt(tempoInput.value) || 60;
});

beatsInput?.addEventListener('change', () => {
  score.beatsPerBar = parseInt(beatsInput.value) || 4;
});

// 键盘事件
window.addEventListener('keydown', (e) => {
  // Ctrl+Z 撤销
  if (e.ctrlKey && e.key === 'z') {
    undo();
    e.preventDefault();
  }
  // Ctrl+Y 重做
  if (e.ctrlKey && e.key === 'y') {
    redo();
    e.preventDefault();
  }
  // Delete 删除选中音符
  if (e.key === 'Delete' && selectedNoteId !== null) {
    deleteNote(selectedNoteId);
    e.preventDefault();
  }

  // 编辑模式下：数字键/空格/b 快速输入
  if (editMode === 'edit') {
    // 数字 0-7 输入音符（插入到选中音符后面）
    if (/^[0-7]$/.test(e.key)) {
      addNote({ value: e.key, octave: 0, duration: lastDuration, dotted: false, ban: 0, yan: 0, lineBreak: false }, selectedNoteId ?? undefined);
      e.preventDefault();
      return;
    }
    // 空格键输入空格（插入到选中音符后面）
    if (e.key === ' ' || e.key === 'space') {
      addNote({ value: 'space', octave: 0, duration: lastDuration, dotted: false, ban: 0, yan: 0, lineBreak: false }, selectedNoteId ?? undefined);
      e.preventDefault();
      return;
    }
    // b键切换板（需选中音符）
    if (e.key === 'b' && selectedNoteId !== null) {
      const note = score.notes.find(n => n.id === selectedNoteId);
      if (note) {
        updateNote(selectedNoteId, { ban: note.ban === 1 ? 0 : 1 });
      }
      e.preventDefault();
      return;
    }
    // x键输入小节线
    if (e.key === 'x') {
      if (selectedNoteId === null) {
        addNote({ value: 'bar', octave: 0, duration: 0, dotted: false, ban: 0, yan: 0, lineBreak: false });
        e.preventDefault();
        return;
      }
    }
    // y键切换眼（需要选中音符）
    if (e.key === 'y' && selectedNoteId !== null) {
      const note = score.notes.find(n => n.id === selectedNoteId);
      if (note) {
        updateNote(selectedNoteId, { yan: note.yan === 1 ? 0 : 1 });
      }
      e.preventDefault();
      return;
    }
    // .键切换附点（需要选中音符）
    if (e.key === '.' && selectedNoteId !== null) {
      const note = score.notes.find(n => n.id === selectedNoteId);
      if (note) {
        updateNote(selectedNoteId, { dotted: !note.dotted });
      }
      e.preventDefault();
      return;
    }
  }

  // 方向键处理
  if (selectedNoteId === null) return;

  if (editMode === 'select') {
    // 选择模式：左右切换选中音符
    const noteIds = score.notes.map(n => n.id);
    const currentIdx = noteIds.indexOf(selectedNoteId);
    if (e.key === 'ArrowRight' && currentIdx < noteIds.length - 1) {
      selectedNoteId = noteIds[currentIdx + 1];
      render();
      setStatus(`已选择音符 ID:${selectedNoteId}`);
      e.preventDefault();
    }
    if (e.key === 'ArrowLeft' && currentIdx > 0) {
      selectedNoteId = noteIds[currentIdx - 1];
      render();
      setStatus(`已选择音符 ID:${selectedNoteId}`);
      e.preventDefault();
    }
  } else {
    // 编辑模式：上下调整八度，左右调整时值
    const note = score.notes.find(n => n.id === selectedNoteId);
    if (!note) return;

    if (e.key === 'ArrowUp') {
      updateNote(selectedNoteId, { octave: Math.min(2, note.octave + 1) });
      e.preventDefault();
    }
    if (e.key === 'ArrowDown') {
      updateNote(selectedNoteId, { octave: Math.max(-2, note.octave - 1) });
      e.preventDefault();
    }
    if (e.key === 'ArrowRight') {
      // 右键：时值变短（向0.125方向）
      const durations = [4, 3, 2, 1, 0.5, 0.25, 0.125];
      const currentIdx = durations.indexOf(note.duration);
      if (currentIdx === -1 || currentIdx >= durations.length - 1) {
        // 不在列表中或已是最短，跳过
      } else {
        updateNote(selectedNoteId, { duration: durations[currentIdx + 1] });
        lastDuration = durations[currentIdx + 1];
      }
      e.preventDefault();
    }
    if (e.key === 'ArrowLeft') {
      // 左键：时值变长（向4拍方向）
      const durations = [4, 3, 2, 1, 0.5, 0.25, 0.125];
      const currentIdx = durations.indexOf(note.duration);
      if (currentIdx > 0) {
        updateNote(selectedNoteId, { duration: durations[currentIdx - 1] });
        lastDuration = durations[currentIdx - 1];
      }
      e.preventDefault();
    }
  }
});

// 画布点击事件 - 选择音符
canvas.addEventListener('click', (e) => {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  const mouseX = (e.clientX - rect.left) * scaleX;
  const mouseY = (e.clientY - rect.top) * scaleY;

  const noteInfo = renderer.findNoteAt(mouseX, mouseY);
  if (noteInfo) {
    selectedNoteId = noteInfo.id;
    render();
    setStatus(`已选择音符 ID:${noteInfo.id}`);
  } else {
    selectedNoteId = null;
    render();
  }
});

// 滚动条控制
function updateScrollBar(): void {
  const totalHeight = renderer.getTotalHeight();
  const visibleHeight = canvas.height;
  const maxScroll = Math.max(0, totalHeight - visibleHeight);

  scrollBar.max = String(maxScroll);
  scrollBar.value = String(renderer.getScrollY());
  scrollBar.style.display = maxScroll > 0 ? 'block' : 'none';

  // 更新页码信息
  const notesPerRow = Math.floor((canvas.width - 80) / 40);
  const totalRows = Math.ceil((score.notes.length || 0) / notesPerRow);
  const rowsPerPage = renderer.getRowsPerPage();
  const currentPage = Math.floor(renderer.getScrollY() / (rowsPerPage * 80)) + 1;
  pageInfo.textContent = `第 ${currentPage} / ${Math.max(1, totalRows)} 页`;
}

scrollBar?.addEventListener('input', () => {
  renderer.setScrollY(parseInt(scrollBar.value));
  render();
});

btnPageUp?.addEventListener('click', () => {
  const notesPerRow = Math.floor((canvas.width - 80) / 40);
  const rowsPerPage = Math.floor(canvas.height / 80);
  const step = rowsPerPage * notesPerRow;
  const noteIds = score.notes.map(n => n.id);
  const currentIdx = selectedNoteId !== null ? noteIds.indexOf(selectedNoteId) : -1;
  const newIdx = Math.max(0, currentIdx - step);
  if (noteIds.length > 0) {
    selectedNoteId = noteIds[newIdx];
  }
  renderer.setScrollY(Math.max(0, renderer.getScrollY() - rowsPerPage * 80));
  render();
  updateScrollBar();
  if (selectedNoteId !== null) setStatus(`已选择音符 ID:${selectedNoteId}`);
});

btnPageDown?.addEventListener('click', () => {
  const rowsPerPage = Math.floor(canvas.height / 80);
  const noteIds = score.notes.map(n => n.id);
  const currentIdx = selectedNoteId !== null ? noteIds.indexOf(selectedNoteId) : -1;
  const step = rowsPerPage * Math.floor((canvas.width - 80) / 40);
  const newIdx = Math.min(noteIds.length - 1, currentIdx + step);
  if (noteIds.length > 0) {
    selectedNoteId = noteIds[newIdx];
  }
  renderer.setScrollY(renderer.getScrollY() + rowsPerPage * 80);
  render();
  updateScrollBar();
  if (selectedNoteId !== null) setStatus(`已选择音符 ID:${selectedNoteId}`);
});

// 鼠标滚轮横向滚动
canvas.addEventListener('wheel', (e) => {
  if (e.shiftKey) {
    const currentScroll = renderer.getScrollX();
    renderer.setScrollX(Math.max(0, currentScroll - e.deltaY));
    render();
  } else {
    // 纵向滚动
    const currentScroll = renderer.getScrollY();
    const maxScroll = Math.max(0, renderer.getTotalHeight() - canvas.height);
    renderer.setScrollY(Math.min(maxScroll, Math.max(0, currentScroll + e.deltaY)));
    render();
    updateScrollBar();
  }
  e.preventDefault();
}, { passive: false });