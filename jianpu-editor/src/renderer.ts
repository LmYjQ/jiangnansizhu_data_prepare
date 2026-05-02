// jianpu-editor/src/renderer.ts
import {
  Note,
  NoteRenderInfo,
  RenderConfig,
  DEFAULT_CONFIG,
  Score,
} from "./types";

/**
 * 简谱渲染器 - div流式布局，原生浏览器滚动
 */
export class JianpuSVGRenderer {
  private container: HTMLElement;
  private config: RenderConfig;
  private score: Score | null = null;
  private noteInfos: NoteRenderInfo[] = [];

  // 内部选中状态管理
  private selectedNoteId: number | null = null;
  private multiSelectedIds: number[] = [];

  // 光标相关属性
  private cursorElement: HTMLElement | null = null;
  private cursorVisible: boolean = true;
  private cursorBlinkInterval: number | null = null;
  private cursorPosition: {
    index: number;
    x: number;
    y: number;
    row: number;
  } | null = null;

  // 渲染期间当前行div
  private currentRowDiv: HTMLElement | null = null;

  constructor(container: HTMLElement, config: Partial<RenderConfig> = {}) {
    this.container = container;
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.container.style.position = "relative";
    this.initCursor();
  }

  loadScore(score: Score): void {
    this.score = score;
    this.noteInfos = [];
    // 不在此处重置光标，由 render() 结束时负责恢复或初始化到末尾
  }

  // ======================
  // 光标方法
  // ======================
  private initCursor(): void {
    if (this.cursorElement) return;

    this.cursorElement = document.createElement("div");
    this.cursorElement.className = "jianpu-cursor";
    this.container.appendChild(this.cursorElement);
    this.startCursorBlinking();
  }

  private startCursorBlinking(): void {
    if (this.cursorBlinkInterval !== null) {
      clearInterval(this.cursorBlinkInterval);
    }
    this.cursorBlinkInterval = window.setInterval(() => {
      if (!this.cursorElement) return;
      this.cursorVisible = !this.cursorVisible;
      this.cursorElement.style.opacity = this.cursorVisible ? "1" : "0";
    }, 500);
  }

  private stopCursorBlinking(): void {
    if (this.cursorBlinkInterval !== null) {
      clearInterval(this.cursorBlinkInterval);
      this.cursorBlinkInterval = null;
    }
  }

  private updateCursorPosition(
    x: number,
    y: number,
    row: number,
    index: number,
  ): void {
    this.cursorPosition = { index, x, y, row };
    if (!this.cursorElement) return;

    const { lineSpacing } = this.config;
    const cursorHeight = lineSpacing * 0.8;

    // 光标是 position:absolute，left/top 从容器 padding edge 算起（即容器左/上边缘）。
    // 但音符 div 排列在内容区，起点偏移了 padding。需补偿才能对齐。
    const cs = getComputedStyle(this.container);
    const pl = parseFloat(cs.paddingLeft) || 0;
    const pt = parseFloat(cs.paddingTop) || 0;

    this.cursorElement.style.left = `${x + pl}px`;
    this.cursorElement.style.top = `${y - cursorHeight / 2 + pt}px`;
    this.cursorElement.style.height = `${cursorHeight}px`;
    this.cursorElement.style.display = "block";

    this.cursorVisible = true;
    this.cursorElement.style.opacity = "1";
  }

  setCursorPosition(index: number): void {
    if (!this.score || index < 0 || index > this.score.notes.length) return;

    const { noteSpacing, lineSpacing } = this.config;
    const startX = 50;

    if (index === 0) {
      this.updateCursorPosition(
        startX - noteSpacing / 2,
        lineSpacing * 0.5,
        0,
        0,
      );
    } else if (index === this.score.notes.length) {
      if (this.noteInfos.length > 0) {
        const lastNote = this.noteInfos[this.noteInfos.length - 1];
        const cursorX = lastNote.x + noteSpacing;
        const cursorY = lastNote.y + lastNote.height / 2;
        this.updateCursorPosition(cursorX, cursorY, lastNote.row, index);
      } else {
        this.updateCursorPosition(
          startX - noteSpacing / 2,
          lineSpacing * 0.5,
          0,
          0,
        );
      }
    } else {
      const noteInfo = this.noteInfos[index - 1];
      const cursorX = noteInfo.x + noteSpacing;
      const cursorY = noteInfo.y + noteInfo.height / 2;
      this.updateCursorPosition(cursorX, cursorY, noteInfo.row, index);
    }
  }

  getCursorPosition(): {
    index: number;
    x: number;
    y: number;
    row: number;
  } | null {
    return this.cursorPosition;
  }

  setCursorAtNote(noteId: number): void {
    const noteIndex = this.score?.notes.findIndex((n) => n.id === noteId);
    if (noteIndex === undefined || noteIndex === -1) return;
    this.setCursorPosition(noteIndex + 1);
  }

  setCursorAtPosition(x: number, y: number, row: number): void {
    let closestIndex = 0;
    let minDistance = Infinity;

    for (let i = 0; i <= this.noteInfos.length; i++) {
      let targetX: number;
      let targetY: number;

      if (i === 0) {
        const { noteSpacing, lineSpacing } = this.config;
        targetX = 50 - noteSpacing / 2;
        targetY = lineSpacing * 0.5;
      } else if (i === this.noteInfos.length) {
        const lastNote = this.noteInfos[i - 1];
        targetX = lastNote.x + this.config.noteSpacing;
        targetY = lastNote.y + lastNote.height / 2;
      } else {
        const noteInfo = this.noteInfos[i - 1];
        targetX = noteInfo.x + this.config.noteSpacing;
        targetY = noteInfo.y + noteInfo.height / 2;
      }

      const distance = Math.sqrt(
        Math.pow(x - targetX, 2) + Math.pow(y - targetY, 2),
      );
      const noteRow =
        i === 0
          ? 0
          : i === this.noteInfos.length
            ? this.noteInfos[i - 1].row
            : this.noteInfos[i].row;

      if (noteRow === row && distance < minDistance) {
        minDistance = distance;
        closestIndex = i;
      }
    }

    this.setCursorPosition(closestIndex);
  }

  hideCursor(): void {
    if (this.cursorElement) this.cursorElement.style.display = "none";
    this.stopCursorBlinking();
  }

  showCursor(): void {
    if (this.cursorElement) this.cursorElement.style.display = "block";
    this.startCursorBlinking();
  }

  // ======================
  // 高亮方法
  // ======================
  clearAllHighlight(): void {
    const all = this.container.querySelectorAll(
      ".note-group.selected, .note-single-selected, .note-batch-selected",
    );
    all.forEach((el) => {
      el.classList.remove(
        "selected",
        "note-single-selected",
        "note-batch-selected",
      );
    });
  }

  highlightSelectedNotes(): void {
    this.clearAllHighlight();

    if (this.multiSelectedIds.length > 0) {
      this.multiSelectedIds.forEach((id) => {
        const el = this.container.querySelector(`#note-${id}`);
        if (el) el.classList.add("note-batch-selected");
      });
      return;
    }

    if (this.selectedNoteId !== null) {
      const el = this.container.querySelector(`#note-${this.selectedNoteId}`);
      if (el) el.classList.add("note-single-selected");
    }
  }

  selectNote(noteId: number | null): void {
    this.selectedNoteId = noteId;
    this.multiSelectedIds = [];
    this.highlightSelectedNotes();
  }

  setMultiSelected(ids: number[]): void {
    this.multiSelectedIds = [...ids];
    this.selectedNoteId = null;
    this.highlightSelectedNotes();
  }

  // 滚动方法 - 委托给原生浏览器滚动
  setScrollY(y: number): void {
    this.container.scrollTop = Math.max(
      0,
      Math.min(y, this.container.scrollHeight - this.container.clientHeight),
    );
  }

  getScrollY(): number {
    return this.container.scrollTop;
  }

  setScrollX(x: number): void {
    this.container.scrollLeft = Math.max(0, x);
  }

  getScrollX(): number {
    return this.container.scrollLeft;
  }

  getTotalHeight(): number {
    return this.container.scrollHeight;
  }

  getTotalWidth(): number {
    return this.container.scrollWidth;
  }

  getRowsPerPage(): number {
    return Math.floor(this.container.clientHeight / this.config.lineSpacing);
  }

  private getBeatLines(type: number | null): number {
    if (type === null) return 0;
    if (type >= 99)
      return this.score?.beatsPerBar ? this.score.beatsPerBar - 1 : 3;
    if (type >= 2) return 1;
    if (type >= 1) return 0;
    if (type >= 0.5) return 1;
    if (type >= 0.25) return 2;
    return 3;
  }

  renderNote(note: Note, x: number, y: number, row: number): NoteRenderInfo {
    const {
      noteSpacing,
      lineSpacing,
      noteFontSize,
      dotRadius,
      octaveDotOffset,
    } = this.config;
    const width = noteSpacing;
    const totalHeight = lineSpacing;

    const noteDiv = document.createElement("div");
    noteDiv.id = `note-${note.id}`;
    noteDiv.className = "note-group";
    noteDiv.style.cssText = `
      width: ${width}px;
      height: ${lineSpacing}px;
    
    `;

    noteDiv.addEventListener("click", (e) => {
      e.stopPropagation();
      const event = new CustomEvent("note-click", {
        detail: { noteId: note.id },
        bubbles: true,
      });
      this.container.dispatchEvent(event);
    });

    if (this.currentRowDiv) {
      this.currentRowDiv.appendChild(noteDiv);
    }

    if (note.value === "bar") {
      const barLine = document.createElement("div");
      barLine.className = "note-bar";

      noteDiv.appendChild(barLine);

      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - totalHeight / 2,
        width,
        height: totalHeight,
        row,
        value: note.value,
        type: null,
        octave: 0,
        duration: note.duration,
        dotted: false,
        beatLines: 0,
        lineBreak: note.lineBreak,
      });
    } else if (note.value === "space") {
      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - totalHeight / 2,
        width,
        height: totalHeight,
        row,
        value: note.value,
        type: null,
        octave: 0,
        duration: note.duration,
        dotted: false,
        beatLines: 0,
        lineBreak: note.lineBreak,
      });
    } else if (note.value === "0") {
      const noteValue = document.createElement("div");
      noteValue.textContent = "0";
      noteValue.style.fontFamily = "Songti, SimSun, serif";
      noteValue.style.fontSize = `${noteFontSize}px`;
      noteDiv.appendChild(noteValue);

      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - totalHeight / 2,
        width,
        height: totalHeight,
        row,
        value: note.value,
        type: note.type,
        octave: note.octave,
        duration: note.duration,
        dotted: note.dotted,
        beatLines: 0,
        lineBreak: note.lineBreak,
      });
    } else if (/[1-7]/.test(note.value)) {
      let noteColor = "#000";
      if (note.yan) noteColor = "blue";
      else if (note.ban) noteColor = "orange";

      const noteValue = document.createElement("div");
      noteValue.textContent = note.value;
      noteValue.style.fontFamily = "Songti, SimSun, serif";
      noteValue.style.fontSize = `${noteFontSize}px`;
      noteValue.style.color = noteColor;
      noteDiv.appendChild(noteValue);

      const beatLines = this.getBeatLines(note.type);
      if (note.duration < 1) {
        for (let i = 0; i < beatLines; i++) {
          const line = document.createElement("div");
          line.style.cssText = `
            position: absolute;
            width: 20px;
            height: 1.5px;
            background-color: #000;
            top: calc(50% + ${14 + i * 6}px);
            left: 50%;
            transform: translateX(-50%);
          `;
          noteDiv.appendChild(line);
        }
      } else {
        for (let i = 0; i < beatLines; i++) {
          const line = document.createElement("div");
          line.style.cssText = `
            position: absolute;
            width: 6px;
            height: 1.5px;
            background-color: #000;
            top: 50%;
            left: ${16 + i * 8}px;
            transform: translateY(-50%);
          `;
          noteDiv.appendChild(line);
        }
      }

      if (note.octave !== 0) {
        const radius = dotRadius;
        const offset = octaveDotOffset;
        if (note.octave > 0) {
          for (let i = 0; i < note.octave; i++) {
            const dot = document.createElement("div");
            dot.style.cssText = `
              position: absolute;
              width: ${radius * 1.3}px;
              height: ${radius * 1.3}px;
              border-radius: 50%;
              background-color: #000;
              top: calc(50% - ${offset + i * (radius * 2 + 2)}px);
              left: 50%;
              transform: translate(-50%, -50%);
            `;
            noteDiv.appendChild(dot);
          }
        } else {
          for (let i = 0; i < Math.abs(note.octave); i++) {
            const dot = document.createElement("div");
            dot.style.cssText = `
              position: absolute;
              width: ${radius * 1.3}px;
              height: ${radius * 1.3}px;
              border-radius: 50%;
              background-color: #000;
              top: calc(50% + ${offset + i * (radius * 2 + 2)}px);
              left: 50%;
              transform: translate(-50%, -50%);
            `;
            noteDiv.appendChild(dot);
          }
        }
      }

      if (note.dotted) {
        const dotted = document.createElement("div");
        dotted.style.cssText = `
          position: absolute;
          width: ${dotRadius * 1.3}px;
          height: ${dotRadius * 1.3}px;
          border-radius: 50%;
          background-color: #000;
          top: calc(50% + 6px);
          left: calc(50% + 8px);
          transform: translate(-50%, -50%);
        `;
        noteDiv.appendChild(dotted);
      }

      this.noteInfos.push({
        id: note.id,
        x: x - width / 2,
        y: y - totalHeight / 2,
        width,
        height: totalHeight,
        row,
        value: note.value,
        octave: note.octave,
        duration: note.duration,
        dotted: note.dotted,
        type: note.type,
        beatLines,
        lineBreak: note.lineBreak,
      });
    }

    return this.noteInfos[this.noteInfos.length - 1];
  }

  private createRowDiv(row: number): HTMLElement {
    const { lineSpacing } = this.config;
    const rowDiv = document.createElement("div");
    rowDiv.className = "score-row";
    rowDiv.dataset.row = row.toString();
    rowDiv.style.cssText = `
      display: flex;
      align-items: center;
      height: ${lineSpacing}px;
      position: relative;
      overflow: visible;
      flex-shrink: 0;
    `;
    return rowDiv;
  }

  /**
   * 渲染整首乐谱
   */
  render(): void {
    if (!this.score) return;

    // 清空容器内容，保留光标元素
    const children = Array.from(this.container.children);
    children.forEach((child) => {
      if (child !== this.cursorElement) {
        this.container.removeChild(child);
      }
    });
    this.initCursor();

    const { noteSpacing, lineSpacing } = this.config;
    const startX = 50;

    this.noteInfos = [];
    let currentX = startX;
    let currentRow = 0;

    const containerWidth = this.container.clientWidth;
    const availableWidth = containerWidth - 100;

    const notes = this.score.notes;

    // 创建第一行
    this.currentRowDiv = this.createRowDiv(0);
    const leadingSpacer = document.createElement("div");
    leadingSpacer.style.cssText = `width: ${startX - noteSpacing / 2}px; flex-shrink: 0;`;
    this.currentRowDiv.appendChild(leadingSpacer);
    this.container.insertBefore(this.currentRowDiv, this.cursorElement);

    let i = 0;
    while (i < notes.length) {
      const note = notes[i];

      // 1. 遇到小节线，直接渲染
      if (note.value === "bar") {
        const rowY = lineSpacing * 0.5 + currentRow * lineSpacing;
        this.renderNote(note, currentX, rowY, currentRow);
        currentX += noteSpacing;
        i++;
        continue;
      }

      // 2. 截取当前小节所有音符
      const barStart = i;
      let barEnd = barStart;
      let totalBarWidth = 0;
      let tempBeat = 0;

      for (let j = barStart; j < notes.length; j++) {
        const n = notes[j];
        if (n.value === "bar") break;
        totalBarWidth += noteSpacing;
        tempBeat += n.duration;
        if (tempBeat >= 1) {
          totalBarWidth += noteSpacing * 0.5;
          tempBeat = 0;
        }
        barEnd = j;
      }

      // 3. 判断是否需要换行
      const remainingWidth = availableWidth - currentX;
      const needWrap = totalBarWidth > remainingWidth && currentX !== startX;

      if (needWrap) {
        currentRow++;
        currentX = startX;
        this.currentRowDiv = this.createRowDiv(currentRow);
        const ls = document.createElement("div");
        ls.style.cssText = `width: ${startX - noteSpacing / 2}px; flex-shrink: 0;`;
        this.currentRowDiv.appendChild(ls);
        this.container.insertBefore(this.currentRowDiv, this.cursorElement);
      }

      // 4. 渲染整个小节
      tempBeat = 0;
      for (let j = barStart; j <= barEnd; j++) {
        const n = notes[j];
        const rowY = lineSpacing * 0.5 + currentRow * lineSpacing;
        this.renderNote(n, currentX, rowY, currentRow);

        tempBeat += n.duration;
        currentX += noteSpacing;

        if (tempBeat >= 1) {
          if (this.currentRowDiv) {
            const spacer = document.createElement("div");
            spacer.style.cssText = `width: ${noteSpacing * 0.5}px; flex-shrink: 0;`;
            this.currentRowDiv.appendChild(spacer);
          }
          currentX += noteSpacing * 0.5;
          tempBeat = 0;
        }
      }

      i = barEnd + 1;
    }

    this.highlightSelectedNotes();
    if (this.cursorPosition) {
      const clampedIndex = Math.min(this.cursorPosition.index, this.score.notes.length);
      this.setCursorPosition(clampedIndex);
    } else {
      this.setCursorPosition(this.score.notes.length);
    }
  }

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

  getNoteInfos(): NoteRenderInfo[] {
    return [...this.noteInfos];
  }
}
