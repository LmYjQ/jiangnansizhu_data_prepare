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
  // 不再触发重新渲染，而是直接设置滚动位置
  if (this.svgElement.parentElement) {
    this.svgElement.parentElement.scrollTop = this.scrollY;
  }
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
  // 不再触发重新渲染，而是直接设置滚动位置
  if (this.svgElement.parentElement) {
    this.svgElement.parentElement.scrollLeft = this.scrollX;
  }
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
    if (!this.score || this.score.notes.length === 0) return 1200; // 默认宽度
    return this.noteInfos.length > 0
      ? this.noteInfos[this.noteInfos.length - 1].x +
          this.config.noteSpacing * 2
      : 1200;
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
  private getBeatLines(type: number | null): number {
    if (type === null) return 0; // 未知类型
    if (type >= 99)
      return this.score?.beatsPerBar ? this.score.beatsPerBar - 1 : 3; // 全音符根据拍数决定线条数
    if (type >= 2) return 1;
    if (type >= 1) return 0;
    if (type >= 0.5) return 1;
    if (type >= 0.25) return 2;
    return 3;
  }

  /**
   * 渲染单个音符，返回渲染信息
   */
  renderNote(note: Note, x: number, y: number, row: number): NoteRenderInfo {
    const width = this.config.noteSpacing;
    const height = this.config.noteFontSize;

    // 计算所需的总高度，包括八度点和时值线
    // 基础高度为音符字体大小
    let totalHeight = height;

    // 如果有高八度点，需要额外空间
    if (note.octave > 0) {
      const radius = this.config.dotRadius;
      const offset = this.config.octaveDotOffset;
      totalHeight += offset + note.octave * (radius * 2 + 2);
    }

    // 如果有低八度点或时值线，需要额外空间
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

    // 创建一个foreignObject元素作为音符的容器
    const foreignObject = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "foreignObject",
    );
    foreignObject.setAttribute("id", `note-${note.id}`);
    foreignObject.setAttribute("class", "note-group");
    // 调整foreignObject的位置和大小
    foreignObject.setAttribute("x", (x - width / 2).toString());
    foreignObject.setAttribute("y", (y - totalHeight / 2).toString());
    foreignObject.setAttribute("width", width.toString());
    foreignObject.setAttribute("height", totalHeight.toString());

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
      // 空格，不渲染但占位
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
      // 休止符
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
      // 设置音符颜色
      let noteColor = "#000"; // 默认黑色
      if (note.yan) {
        noteColor = "blue";
      } else if (note.ban) {
        noteColor = "orange";
      }
      // 普通音符 1-7
      const noteValue = document.createElement("div");
      noteValue.textContent = note.value;
      noteValue.style.fontFamily = "Songti, SimSun, serif";
      noteValue.style.fontSize = `${this.config.noteFontSize}px`;
      noteValue.style.color = noteColor;
      div.appendChild(noteValue);

      // 画时值线：短于1拍画在下方，长于1拍画在右侧
      const beatLines = this.getBeatLines(note.type);
      if (note.duration < 1) {
        // 在下方画线
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
            dot.style.top = `calc(50% + ${offset + i * (radius * 2 + 2)}px)`;
            dot.style.left = "50%";
            dot.style.transform = "translate(-50%, -50%)";
            div.appendChild(dot);
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

/**
 * 计算每行能容纳的音符数
 */
private getNotesPerRow(): number {
  // 获取SVG父容器的宽度，而不是SVG元素本身的宽度
  const parentElement = this.svgElement.parentElement;
  if (!parentElement) return 10; // 默认值

  const containerWidth = parentElement.clientWidth;
  const availableWidth = containerWidth - 80; // 减去左右边距
  const notesPerRow = Math.floor(availableWidth / this.config.noteSpacing);
  
  console.log(`容器宽度: ${containerWidth}, 可用宽度: ${availableWidth}, 每行音符数: ${notesPerRow}`);
  
  return Math.max(1, notesPerRow); // 确保至少返回1
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

  console.log(`每行可容纳音符数: ${notesPerRow}`);

  // 重置音符信息
  this.noteInfos = [];

  let currentX = startX;
  let currentRow = 0;
  let noteIndex = 0;
  let beatDuration = 0; // 当前拍的累计时长

  // 获取父容器的宽度
  const parentRect = this.svgElement.parentElement?.getBoundingClientRect();
  const containerWidth = parentRect?.width || 1200;
  const availableWidth = containerWidth - 100; // 减去左右边距

  console.log(`容器宽度: ${containerWidth}, 可用宽度: ${availableWidth}`);

  // 渲染每个音符
  for (const note of this.score.notes) {
    // 检查是否需要换行：当前音符位置加上音符宽度超过可用宽度
    const noteWidth = noteSpacing;
    const noteRightEdge = currentX + noteWidth / 2;
    
    // 如果音符的右边缘超过可用宽度，且不是第一个音符，则换行
    if (noteRightEdge > availableWidth && currentX > startX) {
      console.log(`音符 ${noteIndex} 触发换行，当前X: ${currentX}, 音符右边缘: ${noteRightEdge}`);
      currentRow++;
      currentX = startX;
      beatDuration = 0; // 换行时重置拍时长
    }

    // 移除滚动偏移，让音符保持在固定位置
    const rowY = lineSpacing * 0.5 + currentRow * lineSpacing;
    const x = currentX;

    // 渲染音符（统一调用renderNote处理所有类型）
    this.renderNote(note, x, rowY, currentRow);

    // 更新拍时长（只计算音符和空格，不计算小节线）
    if (note.value !== "bar") {
      beatDuration += note.duration;

      // 如果拍时长达到或超过1，添加额外间距
      if (beatDuration >= 1) {
        currentX += noteSpacing * 0.5; // 添加半倍间距
        beatDuration = 0; // 重置拍时长
      }
    }

    currentX += noteSpacing;
    noteIndex++;
  }

  // 计算实际需要的尺寸
  // 宽度：设置为100%，让它自适应外部div
  // 高度：根据实际行数计算，确保能够显示所有内容
  const totalHeight = Math.max(
    lineSpacing,
    (currentRow + 1) * lineSpacing + 50,
  );

  console.log(
    `SVG总尺寸: 宽度=100%, 高度=${totalHeight}, 总行数=${currentRow + 1}`,
  );

  // 设置SVG的尺寸属性
  this.svgElement.setAttribute("width", "100%");
  this.svgElement.setAttribute("height", totalHeight.toString());

  // 同时设置样式，确保SVG元素能够正确显示
  this.svgElement.style.width = "100%";
  this.svgElement.style.height = `${totalHeight}px`;

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
}
