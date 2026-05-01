// jianpu-editor/src/component/history.ts
import { Score } from "../types";
import { SelectionManager } from "./selection";

// 历史记录管理器类
export class HistoryManager {
  private score: Score;
  private history: Score[];
  private historyIndex: number;
  private selectedNoteId: number | null;
  private selectionManager: SelectionManager;
  
  // 回调函数
  private onRender: () => void;
  private onSetStatus: (message: string) => void;
  private onSaveScore: (isManual: boolean) => void;

  constructor(
    score: Score,
    selectedNoteId: number | null,
    selectionManager: SelectionManager,
    onRender: () => void,
    onSetStatus: (message: string) => void,
    onSaveScore: (isManual: boolean) => void
  ) {
    this.score = score;
    this.history = [JSON.parse(JSON.stringify(score))];
    this.historyIndex = 0;
    this.selectedNoteId = selectedNoteId;
    this.selectionManager = selectionManager;
    this.onRender = onRender;
    this.onSetStatus = onSetStatus;
    this.onSaveScore = onSaveScore;
  }

  // 更新选中的音符ID
  updateSelectedNoteId(noteId: number | null): void {
    this.selectedNoteId = noteId;
  }

  // 获取选中的音符ID
  getSelectedNoteId(): number | null {
    return this.selectedNoteId;
  }

  // 保存历史记录
  saveHistory(): void {
    this.history = this.history.slice(0, this.historyIndex + 1);
    this.history.push(JSON.parse(JSON.stringify(this.score)));
    if (this.history.length > 50) {
      this.history.shift();
    }
    this.historyIndex = this.history.length - 1;
    this.onSaveScore(false);
  }

  // 撤销
  undo(): void {
    if (this.historyIndex > 0) {
      this.historyIndex--;
      this.score = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
      this.selectedNoteId = null;
      this.selectionManager.clearSelection();
      this.onRender();
      this.onSetStatus("已撤销");
    }
  }

  // 重做
  redo(): void {
    if (this.historyIndex < this.history.length - 1) {
      this.historyIndex++;
      this.score = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
      this.selectedNoteId = null;
      this.selectionManager.clearSelection();
      this.onRender();
      this.onSetStatus("已重做");
    }
  }

  // 处理键盘事件
  handleKeyDown(e: KeyboardEvent): void {
    const isMeta = e.ctrlKey || e.metaKey;
    
    // 撤销
    if (isMeta && e.key.toLowerCase() === "z") {
      this.undo();
      e.preventDefault();
      return;
    }
    
    // 重做
    if (isMeta && e.key.toLowerCase() === "y") {
      this.redo();
      e.preventDefault();
      return;
    }
  }
}
