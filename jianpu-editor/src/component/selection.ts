import { JianpuSVGRenderer } from "../renderer";

// 框选管理器类
export class SelectionManager {
  private svgElement: SVGSVGElement;
  private renderer: JianpuSVGRenderer;
  
  // 框选状态
  private isDragging = false;
  private dragStartX = 0;
  private dragStartY = 0;
  private selectionRect: SVGRectElement | null = null;
  
  // 音符元素缓存
  private allNoteIds: number[] = [];
  private allNoteElements: { id: number; element: Element; rect: DOMRect }[] = [];
  
  // 选中的音符ID
  private multiSelectedIds: number[] = [];
  private selectedNoteId: number | null = null;
  
  // 状态更新回调
  private onSelectionChange?: (selectedIds: number[]) => void;
  private onStatusUpdate?: (message: string) => void;
  private onNotePanelUpdate?: () => void;

  constructor(
    svgElement: SVGSVGElement,
    renderer: JianpuSVGRenderer,
    onSelectionChange?: (selectedIds: number[]) => void,
    onStatusUpdate?: (message: string) => void,
    onNotePanelUpdate?: () => void
  ) {
    this.svgElement = svgElement;
    this.renderer = renderer;
    this.onSelectionChange = onSelectionChange;
    this.onStatusUpdate = onStatusUpdate;
    this.onNotePanelUpdate = onNotePanelUpdate;
    
    this.initSelectionListeners();
  }

  // 更新音符ID列表
  updateNoteIds(noteIds: number[]): void {
    this.allNoteIds = noteIds;
  }

  // 获取当前选中的音符ID
  getSelectedNoteId(): number | null {
    return this.selectedNoteId;
  }

  // 获取批量选中的音符ID
  getMultiSelectedIds(): number[] {
    return this.multiSelectedIds;
  }

  // 设置单个选中的音符ID
  setSelectedNoteId(noteId: number | null): void {
    this.selectedNoteId = noteId;
  }

  // 设置批量选中的音符ID
  setMultiSelectedIds(ids: number[]): void {
    this.multiSelectedIds = ids;
    this.renderer.setMultiSelected(ids);
    if (this.onSelectionChange) {
      this.onSelectionChange(ids);
    }
  }

  // 清空选中状态
  clearSelection(): void {
    this.multiSelectedIds = [];
    this.selectedNoteId = null;
    this.renderer.clearAllHighlight();
  }

  // 缓存音符元素
  cacheNoteElements(): void {
    this.allNoteElements = [];
    const allElements = this.svgElement.querySelectorAll("*");
    allElements.forEach((el) => {
      const idMatch = el.id.match(/note[_-]?(\d+)/i);
      if (idMatch) {
        const id = parseInt(idMatch[1], 10);
        if (this.allNoteIds.includes(id)) {
          this.allNoteElements.push({
            id,
            element: el,
            rect: el.getBoundingClientRect(),
          });
        }
      }
    });
  }

  // 创建选框元素
  private createSelectionRect(): void {
    if (this.selectionRect) return;
    this.selectionRect = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "rect",
    );
    this.selectionRect.setAttribute("fill", "rgba(66, 133, 244, 0.2)");
    this.selectionRect.setAttribute("stroke", "#4285f4");
    this.selectionRect.setAttribute("stroke-width", "1");
    this.selectionRect.setAttribute("pointer-events", "none");
    this.svgElement.appendChild(this.selectionRect);
  }

  // 更新选框位置
  private updateSelectionRect(x1: number, y1: number, x2: number, y2: number): void {
    if (!this.selectionRect) return;
    const x = Math.min(x1, x2);
    const y = Math.min(y1, y2);
    const width = Math.abs(x2 - x1);
    const height = Math.abs(y2 - y1);
    this.selectionRect.setAttribute("x", x.toString());
    this.selectionRect.setAttribute("y", y.toString());
    this.selectionRect.setAttribute("width", width.toString());
    this.selectionRect.setAttribute("height", height.toString());
  }

  // 移除选框
  private removeSelectionRect(): void {
    if (this.selectionRect) {
      this.svgElement.removeChild(this.selectionRect);
      this.selectionRect = null;
    }
  }

  // 判断元素是否在选框内
  private isElementInRect(
    rect: DOMRect,
    x1: number,
    y1: number,
    x2: number,
    y2: number,
  ): boolean {
    const minX = Math.min(x1, x2);
    const maxX = Math.max(x1, x2);
    const minY = Math.min(y1, y2);
    const maxY = Math.max(y1, y2);
    return !(
      rect.right < minX ||
      rect.left > maxX ||
      rect.bottom < minY ||
      rect.top > maxY
    );
  }

  // 初始化选框相关的事件监听器
  private initSelectionListeners(): void {
    // 鼠标按下：开始框选
    this.svgElement.addEventListener(
      "mousedown",
      (e) => {
        // 只处理左键，排除右键菜单
        if (e.button !== 0) return;
        // 阻止Mac触摸板默认滚动行为
        e.preventDefault();
        e.stopPropagation();

        // 清空之前的选中和高亮
        this.clearSelection();

        // 记录起点坐标（SVG坐标系）
        const svgPoint = this.svgElement.createSVGPoint();
        svgPoint.x = e.clientX;
        svgPoint.y = e.clientY;
        const svgCoords = svgPoint.matrixTransform(
          this.svgElement.getScreenCTM()!.inverse(),
        );
        this.dragStartX = svgCoords.x;
        this.dragStartY = svgCoords.y;
        this.isDragging = true;

        // 创建选框
        this.createSelectionRect();
        this.updateSelectionRect(this.dragStartX, this.dragStartY, this.dragStartX, this.dragStartY);
      },
      { capture: true, passive: false },
    );

    // 鼠标移动：更新选框和选中状态
    this.svgElement.addEventListener(
      "mousemove",
      (e) => {
        if (!this.isDragging || !this.selectionRect) return;
        e.preventDefault();
        e.stopPropagation();

        // 更新选框坐标
        const svgPoint = this.svgElement.createSVGPoint();
        svgPoint.x = e.clientX;
        svgPoint.y = e.clientY;
        const svgCoords = svgPoint.matrixTransform(
          this.svgElement.getScreenCTM()!.inverse(),
        );
        this.updateSelectionRect(this.dragStartX, this.dragStartY, svgCoords.x, svgCoords.y);

        // 计算哪些音符在选框内
        const screenRect = this.selectionRect.getBoundingClientRect();
        const selectedIds: number[] = [];
        this.allNoteElements.forEach((note) => {
          if (
            this.isElementInRect(
              note.rect,
              screenRect.left,
              screenRect.top,
              screenRect.right,
              screenRect.bottom,
            )
          ) {
            selectedIds.push(note.id);
          }
        });

        // 更新选中状态和高亮
        this.setMultiSelectedIds([...new Set(selectedIds)]);
        if (this.onNotePanelUpdate) {
          this.onNotePanelUpdate();
        }
        if (this.onStatusUpdate) {
          this.onStatusUpdate(`已选中 ${this.multiSelectedIds.length} 个音符`);
        }
      },
      { capture: true, passive: false },
    );

    // 鼠标抬起：结束框选
    window.addEventListener(
      "mouseup",
      () => {
        if (!this.isDragging) return;
        this.isDragging = false;
        this.removeSelectionRect();

        if (this.multiSelectedIds.length > 0) {
          if (this.onStatusUpdate) {
            this.onStatusUpdate(`框选完成，共选中 ${this.multiSelectedIds.length} 个音符`);
          }
        }
      },
      { capture: true },
    );

    // 鼠标离开SVG：结束框选
    this.svgElement.addEventListener("mouseleave", () => {
      if (!this.isDragging) return;
      this.isDragging = false;
      this.removeSelectionRect();
    });
  }
}
