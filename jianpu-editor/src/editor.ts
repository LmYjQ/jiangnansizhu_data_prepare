import { Note, Score } from './types';
import { JianpuRenderer } from './renderer';

/**
 * 音符编辑器
 */
export class Editor {
  private renderer: JianpuRenderer;
  private score: Score;
  private selectedNoteId: number | null = null;
  private history: Score[] = [];
  private historyIndex: number = -1;
  private maxHistory: number = 50;

  constructor(renderer: JianpuRenderer, initialScore?: Score) {
    this.renderer = renderer;
    this.score = initialScore || {
      title: '未命名',
      tempo: 60,
      beatsPerBar: 4,
      notes: [],
    };
    this.renderer.loadScore(this.score);
  }

  /**
   * 保存到历史记录
   */
  private saveHistory(): void {
    // 移除当前指针之后的所有历史
    this.history = this.history.slice(0, this.historyIndex + 1);
    // 深拷贝当前乐谱
    this.history.push(JSON.parse(JSON.stringify(this.score)));
    // 限制历史长度
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }
    this.historyIndex = this.history.length - 1;
  }

  /**
   * 撤销
   */
  undo(): void {
    if (this.historyIndex > 0) {
      this.historyIndex--;
      this.score = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
      this.renderer.loadScore(this.score);
      this.renderer.render();
    }
  }

  /**
   * 重做
   */
  redo(): void {
    if (this.historyIndex < this.history.length - 1) {
      this.historyIndex++;
      this.score = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
      this.renderer.loadScore(this.score);
      this.renderer.render();
    }
  }

  /**
   * 添加音符
   */
  addNote(note: Omit<Note, 'id'>): Note {
    this.saveHistory();
    const newNote: Note = {
      ...note,
      id: this.score.notes.length > 0
        ? Math.max(...this.score.notes.map(n => n.id)) + 1
        : 0,
    };
    this.score.notes.push(newNote);
    this.renderer.loadScore(this.score);
    this.renderer.render();
    return newNote;
  }

  /**
   * 更新音符
   */
  updateNote(id: number, updates: Partial<Omit<Note, 'id'>>): boolean {
    this.saveHistory();
    const note = this.score.notes.find(n => n.id === id);
    if (!note) return false;
    Object.assign(note, updates);
    this.renderer.loadScore(this.score);
    this.renderer.render();
    return true;
  }

  /**
   * 删除音符
   */
  deleteNote(id: number): boolean {
    this.saveHistory();
    const index = this.score.notes.findIndex(n => n.id === id);
    if (index === -1) return false;
    this.score.notes.splice(index, 1);
    if (this.selectedNoteId === id) {
      this.selectedNoteId = null;
    }
    this.renderer.loadScore(this.score);
    this.renderer.render();
    return true;
  }

  /**
   * 获取音符
   */
  getNote(id: number): Note | undefined {
    return this.score.notes.find(n => n.id === id);
  }

  /**
   * 获取所有音符
   */
  getNotes(): Note[] {
    return [...this.score.notes];
  }

  /**
   * 选择音符
   */
  selectNote(id: number | null): void {
    this.selectedNoteId = id;
  }

  /**
   * 获取选中的音符
   */
  getSelectedNote(): Note | undefined {
    return this.selectedNoteId !== null ? this.getNote(this.selectedNoteId) : undefined;
  }

  /**
   * 清空乐谱
   */
  clear(): void {
    this.saveHistory();
    this.score.notes = [];
    this.selectedNoteId = null;
    this.renderer.loadScore(this.score);
    this.renderer.render();
  }

  /**
   * 导入乐谱
   */
  importScore(score: Score): void {
    this.score = score;
    this.history = [JSON.parse(JSON.stringify(score))];
    this.historyIndex = 0;
    this.selectedNoteId = null;
    this.renderer.loadScore(this.score);
    this.renderer.render();
  }

  /**
   * 导出具谱
   */
  exportScore(): Score {
    return JSON.parse(JSON.stringify(this.score));
  }

  /**
   * 设置曲名
   */
  setTitle(title: string): void {
    this.score.title = title;
  }

  /**
   * 设置速度
   */
  setTempo(tempo: number): void {
    this.score.tempo = tempo;
  }

  /**
   * 设置每小节拍数
   */
  setBeatsPerBar(beats: number): void {
    this.score.beatsPerBar = beats;
  }

  /**
   * 获取曲名
   */
  getTitle(): string {
    return this.score.title;
  }

  /**
   * 获取速度
   */
  getTempo(): number {
    return this.score.tempo;
  }

  /**
   * 获取每小节拍数
   */
  getBeatsPerBar(): number {
    return this.score.beatsPerBar;
  }

  /**
   * 渲染
   */
  render(): void {
    this.renderer.render();
  }

  /**
   * 键盘快捷键处理
   */
  handleKeyDown(e: KeyboardEvent): boolean {
    // Ctrl+Z = 撤销
    if (e.ctrlKey && e.key === 'z') {
      this.undo();
      return true;
    }
    // Ctrl+Y = 重做
    if (e.ctrlKey && e.key === 'y') {
      this.redo();
      return true;
    }
    // Delete = 删除选中音符
    if (e.key === 'Delete' && this.selectedNoteId !== null) {
      this.deleteNote(this.selectedNoteId);
      return true;
    }
    // 数字键 1-7 = 切换音符值
    if (this.selectedNoteId !== null && ['1', '2', '3', '4', '5', '6', '7', '0'].includes(e.key)) {
      this.updateNote(this.selectedNoteId, { value: e.key });
      return true;
    }
    // 空格键 = 播放/暂停（待实现）
    return false;
  }
}