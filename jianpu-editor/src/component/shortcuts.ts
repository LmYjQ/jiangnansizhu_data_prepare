import { Note, Score } from "../types";
import { SelectionManager } from "./selection";

// 快捷键管理器类
export class ShortcutManager {
  private score: Score;
  private selectedNoteId: number | null;
  private selectionManager: SelectionManager;
  private clipBoardNotes: Note[] = [];
  
  // 回调函数
  private onSaveHistory: () => void;
  private onAutoAddBarLines: () => void;
  private onRender: () => void;
  private onUpdateNotePanel: () => void;
  private onSetStatus: (message: string) => void;
  private onUpdateNote: (id: number, updates: Partial<Note>) => void;

  constructor(
    score: Score,
    selectedNoteId: number | null,
    selectionManager: SelectionManager,
    onSaveHistory: () => void,
    onAutoAddBarLines: () => void,
    onRender: () => void,
    onUpdateNotePanel: () => void,
    onSetStatus: (message: string) => void,
    onUpdateNote: (id: number, updates: Partial<Note>) => void
  ) {
    this.score = score;
    this.selectedNoteId = selectedNoteId;
    this.selectionManager = selectionManager;
    this.onSaveHistory = onSaveHistory;
    this.onAutoAddBarLines = onAutoAddBarLines;
    this.onRender = onRender;
    this.onUpdateNotePanel = onUpdateNotePanel;
    this.onSetStatus = onSetStatus;
    this.onUpdateNote = onUpdateNote;
  }

  // 更新选中的音符ID
  updateSelectedNoteId(noteId: number | null): void {
    this.selectedNoteId = noteId;
  }

  // 获取选中的音符ID
  getSelectedNoteId(): number | null {
    return this.selectedNoteId;
  }

  // 复制选中的音符
  copySelectedNotes(): void {
    const multiSelectedIds = this.selectionManager.getMultiSelectedIds();
    const targetIds =
      multiSelectedIds.length > 0
        ? multiSelectedIds
        : this.selectedNoteId
          ? [this.selectedNoteId]
          : [];
    if (targetIds.length === 0) {
      this.onSetStatus("请先选择音符");
      return;
    }
    this.clipBoardNotes = JSON.parse(
      JSON.stringify(this.score.notes.filter((n) => targetIds.includes(n.id))),
    );
    this.onSetStatus(`已复制 ${this.clipBoardNotes.length} 个音符`);
  }

  // 剪切选中的音符
  cutSelectedNotes(): void {
    const multiSelectedIds = this.selectionManager.getMultiSelectedIds();
    const targetIds =
      multiSelectedIds.length > 0
        ? multiSelectedIds
        : this.selectedNoteId
          ? [this.selectedNoteId]
          : [];
    if (targetIds.length === 0) {
      this.onSetStatus("请先选择音符");
      return;
    }
    this.onSaveHistory();
    this.clipBoardNotes = JSON.parse(
      JSON.stringify(this.score.notes.filter((n) => targetIds.includes(n.id))),
    );
    this.score.notes = this.score.notes.filter((n) => !targetIds.includes(n.id));
    this.selectedNoteId = null;
    this.selectionManager.clearSelection();
    this.onAutoAddBarLines();
    this.onRender();
    this.onSetStatus(`已剪切 ${this.clipBoardNotes.length} 个音符`);
  }

  // 粘贴复制的音符
  pasteCopiedNotes(): void {
    if (this.clipBoardNotes.length === 0) {
      this.onSetStatus("剪贴板为空，请先复制音符");
      return;
    }
    this.onSaveHistory();

    // 计算插入位置
    let insertIdx = this.score.notes.length;
    if (this.selectedNoteId !== null) {
      const idx = this.score.notes.findIndex((n) => n.id === this.selectedNoteId);
      if (idx !== -1) insertIdx = idx + 1;
    }

    // 生成全新不重复的ID
    let maxId =
      this.score.notes.length > 0 ? Math.max(...this.score.notes.map((n) => n.id)) : -1;
    const newNotes = this.clipBoardNotes.map((note) => {
      maxId++;
      return { ...JSON.parse(JSON.stringify(note)), id: maxId };
    });

    // 批量插入
    this.score.notes.splice(insertIdx, 0, ...newNotes);
    this.onAutoAddBarLines();
    this.selectionManager.clearSelection();
    this.onRender();
    this.onSetStatus(`已粘贴 ${newNotes.length} 个音符`);
  }

  // 处理键盘事件
  handleKeyDown(e: KeyboardEvent): void {
    const isMeta = e.ctrlKey || e.metaKey;

    // 核心快捷键：复制/剪切/粘贴/撤销/重做
    if (isMeta && e.key.toLowerCase() === "c") {
      this.copySelectedNotes();
      e.preventDefault();
      return;
    }
    if (isMeta && e.key.toLowerCase() === "x") {
      this.cutSelectedNotes();
      e.preventDefault();
      return;
    }
    if (isMeta && e.key.toLowerCase() === "v") {
      this.pasteCopiedNotes();
      e.preventDefault();
      return;
    }

    // 删除：支持批量删除+单个删除
    if (e.key === "Delete" || e.key === "Backspace") {
      const multiSelectedIds = this.selectionManager.getMultiSelectedIds();
      const targetIds =
        multiSelectedIds.length > 0
          ? multiSelectedIds
          : this.selectedNoteId
            ? [this.selectedNoteId]
            : [];
      if (targetIds.length === 0) return;
      this.onSaveHistory();
      this.score.notes = this.score.notes.filter((n) => !targetIds.includes(n.id));
      this.selectedNoteId = null;
      this.selectionManager.clearSelection();
      this.onAutoAddBarLines();
      this.onRender();
      this.onSetStatus(`已删除 ${targetIds.length} 个音符`);
      e.preventDefault();
      return;
    }
  }
}
