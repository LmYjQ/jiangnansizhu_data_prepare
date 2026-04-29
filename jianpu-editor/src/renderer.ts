import { Note, NoteRenderInfo, RenderConfig, DEFAULT_CONFIG, Score } from './types';

/**
 * 简谱渲染器 - 支持多行和横向滚动
 */
export class JianpuRenderer {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private config: RenderConfig;
  private score: Score | null = null;
  private noteInfos: NoteRenderInfo[] = [];  // 存储所有音符的渲染信息
  private scrollX: number = 0;               // 横向滚动位置
  private scrollY: number = 0;               // 纵向滚动位置

  constructor(canvas: HTMLCanvasElement, config: Partial<RenderConfig> = {}) {
    this.canvas = canvas;
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Failed to get canvas context');
    this.ctx = ctx;
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * 加载乐谱
   */
  loadScore(score: Score): void {
    this.score = score;
    this.noteInfos = [];
  }

  /**
   * 设置纵向滚动位置
   */
  setScrollY(y: number): void {
    this.scrollY = Math.max(0, y);
  }

  /**
   * 获取纵向滚动位置
   */
  getScrollY(): number {
    return this.scrollY;
  }

  /**
   * 设置横向滚动位置
   */
  setScrollX(x: number): void {
    this.scrollX = Math.max(0, x);
  }

  /**
   * 获取横向滚动位置
   */
  getScrollX(): number {
    return this.scrollX;
  }

  /**
   * 获取总高度（用于滚动计算）
   */
  getTotalHeight(): number {
    if (!this.score || this.score.notes.length === 0) return this.canvas.height;
    const notesPerRow = this.getNotesPerRow();
    // 计算总行数（含手动分页符产生的额外行）
    let totalRows = 1;
    for (let i = 0; i < this.score.notes.length; i++) {
      if ((i > 0 && i % notesPerRow === 0) || this.score.notes[i].lineBreak) {
        totalRows++;
      }
    }
    return totalRows * this.config.lineSpacing;
  }

  /**
   * 获取总宽度（用于滚动计算）
   */
  getTotalWidth(): number {
    if (!this.score || this.score.notes.length === 0) return this.canvas.width;
    return this.noteInfos.length > 0
      ? this.noteInfos[this.noteInfos.length - 1].x + this.config.noteSpacing * 2
      : this.canvas.width;
  }

  /**
   * 获取每页行数
   */
  getRowsPerPage(): number {
    return Math.floor(this.canvas.height / this.config.lineSpacing);
  }

  /**
   * 获取拍线条数
   * 1拍=0条, 2拍=1条, 3拍=2条, 4拍=3条
   * 1/2拍=1条, 1/4拍=2条, 1/8拍=3条
   */
  private getBeatLines(duration: number): number {
    if (duration >= 4) return 3;
    if (duration >= 3) return 2;
    if (duration >= 2) return 1;
    if (duration >= 1) return 0;
    if (duration >= 0.5) return 1;
    if (duration >= 0.25) return 2;
    return 3;
  }

  /**
   * 绘制音符数字
   */
  private drawNoteValue(value: string, x: number, y: number): void {
    this.ctx.font = `${this.config.noteFontSize}px Songti, SimSun, serif`;
    this.ctx.fillStyle = '#000';
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(value, x, y);
  }

  /**
   * 绘制圆点（八度点或附点）
   */
  private drawDot(x: number, y: number, radius: number = this.config.dotRadius): void {
    this.ctx.beginPath();
    this.ctx.arc(x, y, radius, 0, Math.PI * 2);
    this.ctx.fill();
  }

  /**
   * 绘制时值线（音符下方的短线，用于1/2、1/4、1/8拍）
   */
  private drawBeatLinesBelow(x: number, y: number, count: number): void {
    if (count <= 0) return;
    this.ctx.strokeStyle = '#000';
    this.ctx.lineWidth = 1.5;
    for (let i = 0; i < count; i++) {
      const lineY = y + 14 + i * 6;
      this.ctx.beginPath();
      this.ctx.moveTo(x - 10, lineY);
      this.ctx.lineTo(x + 10, lineY);
      this.ctx.stroke();
    }
  }

  /**
   * 绘制时值线（音符右侧的短线，用于2、3、4拍）
   */
  private drawBeatLinesRight(x: number, y: number, count: number): void {
    if (count <= 0) return;
    this.ctx.strokeStyle = '#000';
    this.ctx.lineWidth = 1.5;
    for (let i = 0; i < count; i++) {
      const lineX = x + 12 + i * 8;
      this.ctx.beginPath();
      this.ctx.moveTo(lineX, y);
      this.ctx.lineTo(lineX + 6, y);
      this.ctx.stroke();
    }
  }

  /**
   * 绘制八度加点
   */
  private drawOctaveDots(x: number, y: number, octave: number): void {
    if (octave === 0) return;
    const radius = this.config.dotRadius;
    const offset = this.config.octaveDotOffset;

    if (octave > 0) {
      // 高八度：上方加点
      for (let i = 0; i < octave; i++) {
        this.drawDot(x, y - offset - i * (radius * 2 + 2), radius * 0.8);
      }
    } else {
      // 低八度：下方加点（在拍线下方）
      for (let i = 0; i < Math.abs(octave); i++) {
        this.drawDot(x, y + offset + 20 + i * (radius * 2 + 2), radius * 0.8);
      }
    }
  }

  /**
   * 绘制附点
   */
  private drawDotted(x: number, y: number): void {
    this.ctx.fillStyle = '#000';
    this.drawDot(x + 18, y + 6, this.config.dotRadius);
  }

  /**
   * 绘制小节线
   */
  private drawBarLine(x: number, _y: number, rowY: number): void {
    const height = this.config.lineSpacing * 0.8;
    this.ctx.strokeStyle = '#000';
    this.ctx.lineWidth = 1;
    this.ctx.beginPath();
    this.ctx.moveTo(x, rowY - height / 2);
    this.ctx.lineTo(x, rowY + height / 2);
    this.ctx.stroke();
  }

  /**
   * 渲染单个音符，返回渲染信息
   */
  renderNote(note: Note, x: number, y: number, row: number): NoteRenderInfo {
    const width = this.config.noteSpacing;
    const height = this.config.noteFontSize;

    // 处理不同类型的音符
    if (note.value === 'bar') {
      // 小节线
      this.drawBarLine(x, y, y);
      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - height / 2,
        width,
        height,
        row,
        value: note.value,
        octave: 0,
        duration: note.duration,
        dotted: false,
        beatLines: 0,
        lineBreak: note.lineBreak,
      });
    } else if (note.value === 'space') {
      // 空格，不渲染但占位
      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - height / 2,
        width,
        height,
        row,
        value: note.value,
        octave: 0,
        duration: note.duration,
        dotted: false,
        beatLines: 0,
        lineBreak: note.lineBreak,
      });
    } else if (note.value === '0') {
      // 休止符
      this.drawNoteValue('0', x, y);
      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - height / 2,
        width,
        height,
        row,
        value: note.value,
        octave: note.octave,
        duration: note.duration,
        dotted: note.dotted,
        beatLines: 0,
        lineBreak: note.lineBreak,
      });
    } else if (/[1-7]/.test(note.value)) {
      // 普通音符 1-7
      this.drawNoteValue(note.value, x, y);
      // 画时值线：短于1拍画在下方，长于1拍画在右侧
      const beatLines = this.getBeatLines(note.duration);
      if (note.duration < 1) {
        this.drawBeatLinesBelow(x, y, beatLines);
      } else {
        this.drawBeatLinesRight(x, y, beatLines);
      }
      // 再画八度点（低八度点在拍线下方）
      this.drawOctaveDots(x, y, note.octave);
      // 最后画附点
      if (note.dotted) {
        this.drawDotted(x, y);
      }
      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - height / 2,
        width,
        height,
        row,
        value: note.value,
        octave: note.octave,
        duration: note.duration,
        dotted: note.dotted,
        beatLines,
        lineBreak: note.lineBreak,
      });
    }

    return this.noteInfos[this.noteInfos.length - 1];
  }

  /**
   * 计算每行能容纳的音符数
   */
  private getNotesPerRow(): number {
    const availableWidth = this.canvas.width - 80;
    return Math.floor(availableWidth / this.config.noteSpacing);
  }

  /**
   * 渲染整首乐谱
   */
  render(): void {
    if (!this.score) return;

    const { width, height } = this.canvas;
    const { noteSpacing, lineSpacing } = this.config;
    const startX = 50;
    const notesPerRow = this.getNotesPerRow();

    // 清空画布
    this.ctx.fillStyle = '#fff';
    this.ctx.fillRect(0, 0, width, height);

    // 重置音符信息
    this.noteInfos = [];

    let currentX = startX;
    let currentRow = 0;
    let noteIndex = 0;

    // 渲染每个音符
    for (const note of this.score.notes) {
      // 换行检查：达到每行音符数上限 或 手动分页符
      if ((noteIndex > 0 && noteIndex % notesPerRow === 0) || note.lineBreak) {
        currentRow++;
        currentX = startX;
      }

      const rowY = lineSpacing * 0.5 + currentRow * lineSpacing - this.scrollY;
      const x = currentX - this.scrollX;

      // 只渲染可见区域内的音符
      if (x > -noteSpacing && x < width + noteSpacing) {
        // 渲染音符（统一调用renderNote处理所有类型）
        this.renderNote(note, x, rowY, currentRow);
      }

      currentX += noteSpacing;
      noteIndex++;
    }
  }

  /**
   * 根据坐标查找音符
   */
  findNoteAt(mouseX: number, mouseY: number): NoteRenderInfo | null {
    for (const info of this.noteInfos) {
      if (
        mouseX >= info.x &&
        mouseX <= info.x + info.width &&
        mouseY >= info.y &&
        mouseY <= info.y + info.height
      ) {
        return info;
      }
    }
    return null;
  }

  /**
   * 获取音符的渲染信息
   */
  getNoteInfos(): NoteRenderInfo[] {
    return [...this.noteInfos];
  }

  /**
   * 导出具画布为图片
   */
  exportAsImage(type: 'png' | 'jpeg' = 'png'): string {
    return this.canvas.toDataURL(`image/${type}`);
  }

  /**
   * 保存图片
   */
  async saveImage(filename: string, type: 'png' | 'jpeg' = 'png'): Promise<void> {
    const dataUrl = this.exportAsImage(type);
    const link = document.createElement('a');
    link.download = filename;
    link.href = dataUrl;
    link.click();
  }
}