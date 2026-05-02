import { JianpuSVGRenderer } from "../renderer";

// 框选管理器类
export class SelectionManager {
  private container: HTMLElement;
  private renderer: JianpuSVGRenderer;

  // 框选状态
  private isDragging = false;
  private dragStartX = 0;
  private dragStartY = 0;
  private selectionRectEl: HTMLElement | null = null;

  // 音符元素缓存
  private allNoteIds: number[] = [];
  private allNoteElements: { id: number; element: Element }[] = [];

  // 选中的音符ID
  private multiSelectedIds: number[] = [];
  private selectedNoteId: number | null = null;
  private dragJustFinished = false;

  // 状态更新回调
  private onSelectionChange?: (selectedIds: number[]) => void;
  private onStatusUpdate?: (message: string) => void;
  private onNotePanelUpdate?: () => void;

  constructor(
    container: HTMLElement,
    renderer: JianpuSVGRenderer,
    onSelectionChange?: (selectedIds: number[]) => void,
    onStatusUpdate?: (message: string) => void,
    onNotePanelUpdate?: () => void
  ) {
    this.container = container;
    this.renderer = renderer;
    this.onSelectionChange = onSelectionChange;
    this.onStatusUpdate = onStatusUpdate;
    this.onNotePanelUpdate = onNotePanelUpdate;

    this.initSelectionListeners();
  }

  updateNoteIds(noteIds: number[]): void {
    this.allNoteIds = noteIds;
  }

  getSelectedNoteId(): number | null {
    return this.selectedNoteId;
  }

  getMultiSelectedIds(): number[] {
    return this.multiSelectedIds;
  }

  setSelectedNoteId(noteId: number | null): void {
    this.selectedNoteId = noteId;
  }

  setMultiSelectedIds(ids: number[]): void {
    this.multiSelectedIds = ids;
    this.renderer.setMultiSelected(ids);
    if (this.onSelectionChange) {
      this.onSelectionChange(ids);
    }
  }

  clearSelection(): void {
    this.multiSelectedIds = [];
    this.selectedNoteId = null;
    this.renderer.clearAllHighlight();
  }

  consumeDragJustFinished(): boolean {
    const was = this.dragJustFinished;
    this.dragJustFinished = false;
    return was;
  }

  cacheNoteElements(): void {
    this.allNoteElements = [];
    const allElements = this.container.querySelectorAll("[id^='note-']");
    allElements.forEach((el) => {
      const idMatch = el.id.match(/note[_-]?(\d+)/i);
      if (idMatch) {
        const id = parseInt(idMatch[1], 10);
        if (this.allNoteIds.includes(id)) {
          this.allNoteElements.push({ id, element: el });
        }
      }
    });
  }

  // 创建选框div（position: fixed，跟随鼠标）
  private createSelectionRect(): void {
    if (this.selectionRectEl) return;
    this.selectionRectEl = document.createElement("div");
    this.selectionRectEl.style.cssText = `
      position: fixed;
      pointer-events: none;
      background: rgba(66, 133, 244, 0.15);
      border: 1px solid #4285f4;
      z-index: 1000;
      display: none;
    `;
    document.body.appendChild(this.selectionRectEl);
  }

  private updateSelectionRect(x1: number, y1: number, x2: number, y2: number): void {
    if (!this.selectionRectEl) return;
    const x = Math.min(x1, x2);
    const y = Math.min(y1, y2);
    const width = Math.abs(x2 - x1);
    const height = Math.abs(y2 - y1);
    this.selectionRectEl.style.left = `${x}px`;
    this.selectionRectEl.style.top = `${y}px`;
    this.selectionRectEl.style.width = `${width}px`;
    this.selectionRectEl.style.height = `${height}px`;
    this.selectionRectEl.style.display = "block";
  }

  private removeSelectionRect(): void {
    if (this.selectionRectEl) {
      document.body.removeChild(this.selectionRectEl);
      this.selectionRectEl = null;
    }
  }

  private isElementInRect(
    rect: DOMRect,
    minX: number,
    minY: number,
    maxX: number,
    maxY: number
  ): boolean {
    return !(
      rect.right < minX ||
      rect.left > maxX ||
      rect.bottom < minY ||
      rect.top > maxY
    );
  }

  private initSelectionListeners(): void {
    this.container.addEventListener(
      "mousedown",
      (e) => {
        if (e.button !== 0) return;
        e.preventDefault();
        e.stopPropagation();

        this.clearSelection();

        // 记录起点（屏幕坐标，与getBoundingClientRect一致）
        this.dragStartX = e.clientX;
        this.dragStartY = e.clientY;
        this.isDragging = true;

        this.createSelectionRect();
        this.updateSelectionRect(this.dragStartX, this.dragStartY, this.dragStartX, this.dragStartY);
      },
      { capture: true, passive: false }
    );

    this.container.addEventListener(
      "mousemove",
      (e) => {
        if (!this.isDragging || !this.selectionRectEl) return;
        e.preventDefault();
        e.stopPropagation();

        const curX = e.clientX;
        const curY = e.clientY;
        this.updateSelectionRect(this.dragStartX, this.dragStartY, curX, curY);

        const minX = Math.min(this.dragStartX, curX);
        const maxX = Math.max(this.dragStartX, curX);
        const minY = Math.min(this.dragStartY, curY);
        const maxY = Math.max(this.dragStartY, curY);

        // 实时计算元素位置（避免滚动后缓存失效）
        const selectedIds: number[] = [];
        this.allNoteElements.forEach((note) => {
          const rect = note.element.getBoundingClientRect();
          if (this.isElementInRect(rect, minX, minY, maxX, maxY)) {
            selectedIds.push(note.id);
          }
        });

        this.setMultiSelectedIds([...new Set(selectedIds)]);
        if (this.onNotePanelUpdate) this.onNotePanelUpdate();
        if (this.onStatusUpdate) {
          this.onStatusUpdate(`已选中 ${this.multiSelectedIds.length} 个音符`);
        }
      },
      { capture: true, passive: false }
    );

    window.addEventListener(
      "mouseup",
      () => {
        if (!this.isDragging) return;
        this.isDragging = false;
        this.removeSelectionRect();

        if (this.multiSelectedIds.length > 0) {
          this.dragJustFinished = true;
          if (this.onStatusUpdate) {
            this.onStatusUpdate(`框选完成，共选中 ${this.multiSelectedIds.length} 个音符`);
          }
        }
      },
      { capture: true }
    );

    this.container.addEventListener("mouseleave", () => {
      if (!this.isDragging) return;
      this.isDragging = false;
      this.removeSelectionRect();
    });
  }
}
