import {
  Note,
  NoteRenderInfo,
  RenderConfig,
  DEFAULT_CONFIG,
  Score,
} from "./types";

/**
 * 简谱SVG渲染器 - 支持多行和横向滚动
 */
export class JianpuSVGRenderer {
  private svgElement: SVGSVGElement;
  private config: RenderConfig;
  private score: Score | null = null;
  private noteInfos: NoteRenderInfo[] = [];
  private scrollX: number = 0;
  private scrollY: number = 0;

  constructor(svgElement: SVGSVGElement, config: Partial<RenderConfig> = {}) {
    this.svgElement = svgElement;
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.svgElement.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    this.svgElement.style.width = "100%";
    this.svgElement.style.height = "100%";
    this.svgElement.addEventListener(
      "wheel",
      (e) => {
        if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
          e.preventDefault();
          this.setScrollY(this.scrollY + e.deltaY);
        }
      },
      { passive: false },
    );
  }

  loadScore(score: Score): void {
    this.score = score;
    this.noteInfos = [];
  }

  setScrollY(y: number): void {
    const maxScroll = Math.max(
      0,
      this.getTotalHeight() - this.svgElement.clientHeight,
    );
    this.scrollY = Math.max(0, Math.min(y, maxScroll));
    this.render();
  }

  getScrollY(): number {
    return this.scrollY;
  }

  setScrollX(x: number): void {
    this.scrollX = Math.max(0, x);
    if (this.svgElement.parentElement) {
      this.svgElement.parentElement.scrollLeft = this.scrollX;
    }
  }

  getScrollX(): number {
    return this.scrollX;
  }

  getTotalHeight(): number {
    if (!this.score || this.score.notes.length === 0) return 500;
    const notesPerRow = this.getNotesPerRow();
    let totalRows = 1;
    for (let i = 0; i < this.score.notes.length; i++) {
      if ((i > 0 && i % notesPerRow === 0) || this.score.notes[i].lineBreak) {
        totalRows++;
      }
    }
    return totalRows * this.config.lineSpacing + 100;
  }

  getTotalWidth(): number {
    if (!this.score || this.score.notes.length === 0) return 1200;
    return this.noteInfos.length > 0
      ? this.noteInfos[this.noteInfos.length - 1].x +
          this.config.noteSpacing * 2
      : 1200;
  }

  getRowsPerPage(): number {
    const svgRect = this.svgElement.getBoundingClientRect();
    return Math.floor(svgRect.height / this.config.lineSpacing);
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
    const width = this.config.noteSpacing;
    const height = this.config.noteFontSize;
    let totalHeight = height;

    if (note.octave > 0) {
      const radius = this.config.dotRadius;
      const offset = this.config.octaveDotOffset;
      totalHeight += offset + note.octave * (radius * 2 + 2);
    }

    if (note.octave < 0 || (note?.type && note?.type < 1) || note.dotted) {
      const radius = this.config.dotRadius;
      const offset = this.config.octaveDotOffset;
      const beatLines = this.getBeatLines(note?.type);
      const extraHeight = Math.max(
        offset + Math.abs(note.octave) * (radius * 2 + 2),
        14 + beatLines * 6,
        note.dotted ? 6 : 0,
      );
      totalHeight += extraHeight;
    }

    const foreignObject = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "foreignObject",
    );
    foreignObject.setAttribute("id", `note-${note.id}`);
    foreignObject.setAttribute("class", "note-group");
    foreignObject.setAttribute("x", (x - width / 2).toString());
    foreignObject.setAttribute("y", (y - totalHeight / 2).toString());
    foreignObject.setAttribute("width", width.toString());
    foreignObject.setAttribute("height", totalHeight.toString());

    const div = document.createElement("div");
    div.style.width = "100%";
    div.style.height = "100%";
    div.style.position = "relative";
    div.style.display = "flex";
    div.style.justifyContent = "center";
    div.style.alignItems = "center";

    foreignObject.addEventListener("click", (e) => {
      e.stopPropagation();
      const event = new CustomEvent("note-click", {
        detail: { noteId: note.id },
        bubbles: true,
      });
      this.svgElement.dispatchEvent(event);
    });

    this.svgElement.appendChild(foreignObject);
    foreignObject.appendChild(div);

    if (note.value === "bar") {
      const barLine = document.createElement("div");
      barLine.style.position = "absolute";
      barLine.style.width = "1px";
      barLine.style.height = "100%";
      barLine.style.backgroundColor = "#000";
      div.appendChild(barLine);

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
      noteValue.style.fontSize = `${this.config.noteFontSize}px`;
      div.appendChild(noteValue);

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
      noteValue.style.fontSize = `${this.config.noteFontSize}px`;
      noteValue.style.color = noteColor;
      div.appendChild(noteValue);

      const beatLines = this.getBeatLines(note.type);
      if (note.duration < 1) {
        for (let i = 0; i < beatLines; i++) {
          const line = document.createElement("div");
          line.style.position = "absolute";
          line.style.width = "20px";
          line.style.height = "1.5px";
          line.style.backgroundColor = "#000";
          line.style.top = `${totalHeight / 2 + 14 + i * 6}px`;
          line.style.left = "50%";
          line.style.transform = "translateX(-50%)";
          div.appendChild(line);
        }
      } else {
        for (let i = 0; i < beatLines; i++) {
          const line = document.createElement("div");
          line.style.position = "absolute";
          line.style.width = "6px";
          line.style.height = "1.5px";
          line.style.backgroundColor = "#000";
          line.style.top = "50%";
          line.style.left = `${50 + 12 + i * 8}px`;
          line.style.transform = "translateY(-50%)";
          div.appendChild(line);
        }
      }

      if (note.octave !== 0) {
        const radius = this.config.dotRadius;
        const offset = this.config.octaveDotOffset;
        if (note.octave > 0) {
          for (let i = 0; i < note.octave; i++) {
            const dot = document.createElement("div");
            dot.style.position = "absolute";
            dot.style.width = `${radius * 1.3}px`;
            dot.style.height = `${radius * 1.3}px`;
            dot.style.borderRadius = "50%";
            dot.style.backgroundColor = "#000";
            dot.style.top = `calc(50% - ${offset + i * (radius * 2 + 2)}px)`;
            dot.style.left = "50%";
            dot.style.transform = "translate(-50%, -50%)";
            div.appendChild(dot);
          }
        } else {
          for (let i = 0; i < Math.abs(note.octave); i++) {
            const dot = document.createElement("div");
            dot.style.position = "absolute";
            dot.style.width = `${radius * 1.3}px`;
            dot.style.height = `${radius * 1.3}px`;
            dot.style.borderRadius = "50%";
            dot.style.backgroundColor = "#000";
            dot.style.top = `calc(50% + ${offset + i * (radius * 2 + 2)}px)`;
            dot.style.left = "50%";
            dot.style.transform = "translate(-50%, -50%)";
            div.appendChild(dot);
          }
        }
      }

      if (note.dotted) {
        const dotted = document.createElement("div");
        dotted.style.position = "absolute";
        dotted.style.width = `${this.config.dotRadius * 1.3}px`;
        dotted.style.height = `${this.config.dotRadius * 1.3}px`;
        dotted.style.borderRadius = "50%";
        dotted.style.backgroundColor = "#000";
        dotted.style.top = "calc(50% + 6px)";
        dotted.style.left = "calc(50% + 8px)";
        dotted.style.transform = "translate(-50%, -50%)";
        div.appendChild(dotted);
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

  private getNotesPerRow(): number {
    const parentElement = this.svgElement.parentElement;
    if (!parentElement) return 10;
    const containerWidth = parentElement.clientWidth;
    const availableWidth = containerWidth - 80;
    const notesPerRow = Math.floor(availableWidth / this.config.noteSpacing);
    return Math.max(1, notesPerRow);
  }

  /**
   * 渲染整首乐谱
   */

  /**
   * 渲染整首乐谱
   */
  render(selectedNoteId: number | null = null): void {
    if (!this.score) return;

    // 清空SVG元素
    while (this.svgElement.firstChild) {
      this.svgElement.removeChild(this.svgElement.firstChild);
    }

    const { noteSpacing, lineSpacing } = this.config;
    const startX = 50;

    this.noteInfos = [];
    let currentX = startX;
    let currentRow = 0;
    let beatDuration = 0;

    const parentRect = this.svgElement.parentElement?.getBoundingClientRect();
    const containerWidth = parentRect?.width || 1200;
    const availableWidth = containerWidth - 100;

    const notes = this.score.notes;

    // ==============================
    // 【终极正确换行逻辑】
    // 整小节处理，绝不拆拍、绝不拆小节
    // ==============================
    let i = 0;
    while (i < notes.length) {
      const note = notes[i];

      // 1. 遇到小节线，直接渲染，不做换行判断
      if (note.value === "bar") {
        const rowY =
          lineSpacing * 0.5 + currentRow * lineSpacing - this.scrollY;
        this.renderNote(note, currentX, rowY, currentRow);
        currentX += noteSpacing;
        beatDuration = 0;
        i++;
        continue;
      }

      // 2. 截取【当前小节】所有音符（直到下一个小节线或末尾）
      const barStart = i;
      let barEnd = barStart;
      let totalBarWidth = 0;
      let tempBeat = 0;

      // 计算整个小节总宽度
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

      // 3. 判断：当前行剩余位置能不能放下【整个小节】
      const remainingWidth = availableWidth - currentX;
      const needWrap = totalBarWidth > remainingWidth && currentX !== startX;

      if (needWrap) {
        // 放不下 → 整！个！小！节！换！行！
        currentRow++;
        currentX = startX;
        beatDuration = 0;
      }

      // 4. 渲染整个小节（保证不拆拍、不拆音）
      tempBeat = 0;
      for (let j = barStart; j <= barEnd; j++) {
        const n = notes[j];
        const rowY =
          lineSpacing * 0.5 + currentRow * lineSpacing - this.scrollY;
        this.renderNote(n, currentX, rowY, currentRow);

        tempBeat += n.duration;
        currentX += noteSpacing;

        if (tempBeat >= 1) {
          currentX += noteSpacing * 0.5;
          tempBeat = 0;
        }
      }

      beatDuration = tempBeat;
      i = barEnd + 1;
    }

    // 保持你原来的尺寸设置 不动
    const totalHeight = Math.max(
      lineSpacing,
      (currentRow + 1) * lineSpacing + 50,
    );

    this.svgElement.setAttribute("width", "100%");
    this.svgElement.setAttribute("height", "100%");
    this.svgElement.style.width = "100%";
    this.svgElement.style.height = "100%";

    if (selectedNoteId !== null) {
      this.selectNote(selectedNoteId);
    }
  }

  selectNote(noteId: number | null): void {
    const prevSelected = this.svgElement.querySelector(".note-group.selected");
    if (prevSelected) {
      prevSelected.classList.remove("selected");
    }
    if (noteId !== null) {
      const noteGroup = this.svgElement.getElementById(`note-${noteId}`);
      if (noteGroup) {
        noteGroup.classList.add("selected");
      }
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
