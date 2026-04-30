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
  private noteInfos: NoteRenderInfo[] = []; // 存储所有音符的渲染信息
  private scrollX: number = 0; // 横向滚动位置
  private scrollY: number = 0; // 纵向滚动位置

  constructor(svgElement: SVGSVGElement, config: Partial<RenderConfig> = {}) {
    this.svgElement = svgElement;
    this.config = { ...DEFAULT_CONFIG, ...config };
    // 设置SVG的基本属性
    this.svgElement.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    this.svgElement.style.width = "100%";
    this.svgElement.style.height = "100%";
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
    this.render(); // 重新渲染以应用滚动
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
    this.render(); // 重新渲染以应用滚动
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
    if (!this.score || this.score.notes.length === 0) return 500; // 默认高度
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
    if (!this.score || this.score.notes.length === 0) return 800; // 默认宽度
    return this.noteInfos.length > 0
      ? this.noteInfos[this.noteInfos.length - 1].x +
          this.config.noteSpacing * 2
      : 800;
  }

  /**
   * 获取每页行数
   */
  getRowsPerPage(): number {
    const svgRect = this.svgElement.getBoundingClientRect();
    return Math.floor(svgRect.height / this.config.lineSpacing);
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
   * 创建音符数字的SVG元素
   */
  private createNoteValueElement(
    value: string,
    x: number,
    y: number,
  ): SVGTextElement {
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", x.toString());
    text.setAttribute("y", y.toString());
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "middle");
    text.setAttribute("font-family", "Songti, SimSun, serif");
    text.setAttribute("font-size", this.config.noteFontSize.toString());
    text.setAttribute("fill", "#000");
    text.textContent = value;
    return text;
  }

  /**
   * 创建圆点（八度点或附点）的SVG元素
   */
  private createDotElement(
    x: number,
    y: number,
    radius: number = this.config.dotRadius,
  ): SVGCircleElement {
    const circle = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "circle",
    );
    circle.setAttribute("cx", x.toString());
    circle.setAttribute("cy", y.toString());
    circle.setAttribute("r", radius.toString());
    circle.setAttribute("fill", "#000");
    return circle;
  }

  /**
   * 创建时值线（音符下方的短线，用于1/2、1/4、1/8拍）的SVG元素
   */
  private createBeatLinesBelowElement(
    x: number,
    y: number,
    count: number,
  ): SVGLineElement[] {
    const lines: SVGLineElement[] = [];
    if (count <= 0) return lines;

    for (let i = 0; i < count; i++) {
      const lineY = y + 14 + i * 6;
      const line = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "line",
      );
      line.setAttribute("x1", (x - 10).toString());
      line.setAttribute("y1", lineY.toString());
      line.setAttribute("x2", (x + 10).toString());
      line.setAttribute("y2", lineY.toString());
      line.setAttribute("stroke", "#000");
      line.setAttribute("stroke-width", "1.5");
      lines.push(line);
    }
    return lines;
  }

  /**
   * 创建时值线（音符右侧的短线，用于2、3、4拍）的SVG元素
   */
  private createBeatLinesRightElement(
    x: number,
    y: number,
    count: number,
  ): SVGLineElement[] {
    const lines: SVGLineElement[] = [];
    if (count <= 0) return lines;

    for (let i = 0; i < count; i++) {
      const lineX = x + 12 + i * 8;
      const line = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "line",
      );
      line.setAttribute("x1", lineX.toString());
      line.setAttribute("y1", y.toString());
      line.setAttribute("x2", (lineX + 6).toString());
      line.setAttribute("y2", y.toString());
      line.setAttribute("stroke", "#000");
      line.setAttribute("stroke-width", "1.5");
      lines.push(line);
    }
    return lines;
  }

  /**
   * 创建八度加点的SVG元素
   */
  private createOctaveDotsElements(
    x: number,
    y: number,
    octave: number,
  ): SVGCircleElement[] {
    const dots: SVGCircleElement[] = [];
    if (octave === 0) return dots;

    const radius = this.config.dotRadius;
    const offset = this.config.octaveDotOffset;

    if (octave > 0) {
      // 高八度：上方加点
      for (let i = 0; i < octave; i++) {
        const dot = this.createDotElement(
          x,
          y - offset - i * (radius * 2 + 2),
          radius * 0.8,
        );
        dots.push(dot);
      }
    } else {
      // 低八度：下方加点（在拍线下方）
      for (let i = 0; i < Math.abs(octave); i++) {
        const dot = this.createDotElement(
          x,
          y + offset + 20 + i * (radius * 2 + 2),
          radius * 0.8,
        );
        dots.push(dot);
      }
    }
    return dots;
  }

  /**
   * 创建附点的SVG元素
   */
  private createDottedElement(x: number, y: number): SVGCircleElement {
    return this.createDotElement(x + 18, y + 6, this.config.dotRadius);
  }

  /**
   * 创建小节线的SVG元素
   */
  private createBarLineElement(
    x: number,
    _y: number,
    rowY: number,
  ): SVGLineElement {
    const height = this.config.lineSpacing * 0.8;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x.toString());
    line.setAttribute("y1", (rowY - height / 2).toString());
    line.setAttribute("x2", x.toString());
    line.setAttribute("y2", (rowY + height / 2).toString());
    line.setAttribute("stroke", "#000");
    line.setAttribute("stroke-width", "1");
    return line;
  }

  /**
   * 渲染单个音符，返回渲染信息
   */
  renderNote(note: Note, x: number, y: number, row: number): NoteRenderInfo {
    const width = this.config.noteSpacing;
    const height = this.config.noteFontSize;

    // 创建一个foreignObject元素作为音符的容器
    const foreignObject = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "foreignObject",
    );
    foreignObject.setAttribute("id", `note-${note.id}`);
    foreignObject.setAttribute("class", "note-group");
    foreignObject.setAttribute("x", (x - width / 2).toString());
    foreignObject.setAttribute("y", (y - height / 2).toString());
    foreignObject.setAttribute("width", width.toString());
    foreignObject.setAttribute("height", height.toString());

    // 创建一个div作为foreignObject的内容
    const div = document.createElement("div");
    div.style.width = "100%";
    div.style.height = "100%";
    div.style.position = "relative";
    div.style.display = "flex";
    div.style.justifyContent = "center";
    div.style.alignItems = "center";

    // 添加点击事件处理
    foreignObject.addEventListener("click", (e) => {
      e.stopPropagation(); // 阻止事件冒泡
      // 触发自定义事件，通知外部音符被点击
      const event = new CustomEvent("note-click", {
        detail: { noteId: note.id },
        bubbles: true,
      });
      this.svgElement.dispatchEvent(event);
    });

    this.svgElement.appendChild(foreignObject);
    foreignObject.appendChild(div);

    // 处理不同类型的音符
    if (note.value === "bar") {
      // 小节线
      const barLine = document.createElement("div");
      barLine.style.position = "absolute";
      barLine.style.width = "1px";
      barLine.style.height = "100%";
      barLine.style.backgroundColor = "#000";
      div.appendChild(barLine);

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
    } else if (note.value === "space") {
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
    } else if (note.value === "0") {
      // 休止符
      const noteValue = document.createElement("div");
      noteValue.textContent = "0";
      noteValue.style.fontFamily = "Songti, SimSun, serif";
      noteValue.style.fontSize = `${this.config.noteFontSize}px`;
      div.appendChild(noteValue);

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
      const noteValue = document.createElement("div");
      noteValue.textContent = note.value;
      noteValue.style.fontFamily = "Songti, SimSun, serif";
      noteValue.style.fontSize = `${this.config.noteFontSize}px`;
      div.appendChild(noteValue);

      // 画时值线：短于1拍画在下方，长于1拍画在右侧
      const beatLines = this.getBeatLines(note.duration);
      if (note.duration < 1) {
        // 在下方画线
        for (let i = 0; i < beatLines; i++) {
          const line = document.createElement("div");
          line.style.position = "absolute";
          line.style.width = "20px";
          line.style.height = "1.5px";
          line.style.backgroundColor = "#000";
          line.style.top = `${25 + i * 6}px`;
          line.style.left = "50%";
          line.style.transform = "translateX(-50%)";
          div.appendChild(line);
        }
      } else {
        // 在右侧画线
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

      // 画八度点
      if (note.octave !== 0) {
        if (note.octave !== 0) {
          const radius = this.config.dotRadius;
          const offset = this.config.octaveDotOffset;

          if (note.octave > 0) {
            // 高八度：上方加点
            for (let i = 0; i < note.octave; i++) {
              const dot = document.createElement("div");
              dot.style.position = "absolute";
              dot.style.width = `${radius * 1.3}px`;
              dot.style.height = `${radius * 1.3}px`;
              dot.style.borderRadius = "50%";
              dot.style.backgroundColor = "#000";
              // 使用百分比定位，50%是垂直居中
              dot.style.top = `calc(50% - ${offset + i * (radius * 2 + 2)}px)`;
              dot.style.left = "50%";
              dot.style.transform = "translate(-50%, -50%)";
              div.appendChild(dot);
            }
          } else {
            // 低八度：下方加点
            for (let i = 0; i < Math.abs(note.octave); i++) {
              const dot = document.createElement("div");
              dot.style.position = "absolute";
              dot.style.width = `${radius * 1.3}px`;
              dot.style.height = `${radius * 1.3}px`;
              dot.style.borderRadius = "50%";
              dot.style.backgroundColor = "#000";
              // 使用百分比定位，50%是垂直居中
              dot.style.top = `calc(50% + ${offset + i * (radius * 2 + 2)}px)`;
              dot.style.left = "50%";
              dot.style.transform = "translate(-50%, -50%)";
              div.appendChild(dot);
            }
          }
        }
      }

      // 画附点
      if (note.dotted) {
        const dotted = document.createElement("div");
        dotted.style.position = "absolute";
        dotted.style.width = `${this.config.dotRadius * 1.3}px`;
        dotted.style.height = `${this.config.dotRadius * 1.3}px`;
        dotted.style.borderRadius = "50%";
        dotted.style.backgroundColor = "#000";
        dotted.style.top = `${10 + 6}px`;
        dotted.style.left = `${10 + 18}px`;
        div.appendChild(dotted);
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
    const svgRect = this.svgElement.getBoundingClientRect();
    const availableWidth = svgRect.width - 80;
    return Math.floor(availableWidth / this.config.noteSpacing);
  }

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
    const notesPerRow = this.getNotesPerRow();

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
      if (
        x > -noteSpacing &&
        x < this.svgElement.getBoundingClientRect().width + noteSpacing
      ) {
        // 渲染音符（统一调用renderNote处理所有类型）
        this.renderNote(note, x, rowY, currentRow);
      }

      currentX += noteSpacing;
      noteIndex++;
    }

    // 如果有选中的音符，高亮显示
    if (selectedNoteId !== null) {
      this.selectNote(selectedNoteId);
    }
  }

  /**
   * 选择音符
   */
  selectNote(noteId: number | null): void {
    // 取消之前选中的音符
    const prevSelected = this.svgElement.querySelector(".note-group.selected");
    if (prevSelected) {
      prevSelected.classList.remove("selected");
    }

    // 如果noteId不为null，选中新音符
    if (noteId !== null) {
      const noteGroup = this.svgElement.getElementById(`note-${noteId}`);
      if (noteGroup) {
        noteGroup.classList.add("selected");
      }
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
   * 导出SVG为字符串
   */
  exportAsString(): string {
    return new XMLSerializer().serializeToString(this.svgElement);
  }

  /**
   * 导出SVG为文件
   */
  async saveAsFile(filename: string): Promise<void> {
    const svgString = this.exportAsString();
    const blob = new Blob([svgString], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.download = filename;
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
  }
}
