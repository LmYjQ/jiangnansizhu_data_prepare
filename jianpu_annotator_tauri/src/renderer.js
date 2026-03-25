/**
 * 简谱 Canvas 渲染器
 * Ported from jianpu_renderer.py
 */

import { parseNoteValue } from './annotation.js';

// Renderer constants
const CELL_WIDTH = 60;
const CELL_HEIGHT = 100;
const NOTE_SIZE = 36;
const DOT_SIZE = 5;
const MARKER_SIZE = 8;
const LINE_WIDTH = 1.5;

// Colors
const COLOR_SELECTED_BG = "#E6F0FF";
const COLOR_BAN = "#FF6600";
const COLOR_YAN = "#00AA55";
const COLOR_GU_GAN = "#FF0000";
const COLOR_NOTE = "#000000";
const COLOR_DOT = "#666666";

class JianpuRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.beatsPerMeasure = 4;
    this.zoomScale = 1.0;
  }

  /**
   * Resize canvas based on number of notes
   */
  resize(noteCount, rowCount = 1) {
    const cellHeight = CELL_HEIGHT * this.zoomScale;
    const width = Math.max(noteCount * CELL_WIDTH * this.zoomScale, 800);
    const height = cellHeight * rowCount;
    this.canvas.width = width;
    this.canvas.height = height;
  }

  /**
   * Set zoom level
   */
  setZoom(scale) {
    this.zoomScale = scale;
  }

  /**
   * Clear the canvas
   */
  clear() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }

  /**
   * Calculate beats for a single note
   * Returns { beats, extendsHalf }
   */
  getNoteInfo(note) {
    const parsed = parseNoteValue(note.value);
    let beats = 1; // default

    // Handle prefix modifiers
    if (parsed.prefix.includes('z')) beats = 0.5;      // 八分
    else if (parsed.prefix.includes('x')) beats = 0.25; // 十六分
    else if (parsed.prefix.includes('c')) beats = 0.125; // 三十二分
    // N: handled in draw loop

    // Handle suffix modifiers
    if (parsed.suffix === ':') beats = 2; // 延长音

    console.log(`getNoteInfo: value="${note.value}", prefix="${parsed.prefix}", suffix="${parsed.suffix}", beats=${beats}, isN=${parsed.prefix.includes('N')}`);
    return { beats, isN: parsed.prefix.includes('N') };
  }

  /**
   * Draw all notes (single row mode)
   */
  draw(notes, selectedIdx, scrollX) {
    this.drawMultipleRows([notes], selectedIdx, 0, scrollX);
  }

  /**
   * Draw multiple rows (all mode)
   * @param {Array} allRows - Array of note arrays, one per row
   * @param {number} selectedIdx - Global selected note index across all rows
   * @param {number} selectedRow - Which row is selected
   * @param {number} scrollX - Horizontal scroll offset
   */
  drawMultipleRows(allRows, selectedIdx, selectedRow, scrollX) {
    this.clear();

    const scaledCellWidth = CELL_WIDTH * this.zoomScale;
    const scaledCellHeight = CELL_HEIGHT * this.zoomScale;

    for (let row = 0; row < allRows.length; row++) {
      const notes = allRows[row];
      const rowY = row * scaledCellHeight;
      let cumulativeBeats = 0;

      for (let idx = 0; idx < notes.length; idx++) {
        const x = idx * scaledCellWidth - scrollX;
        if (x < -scaledCellWidth || x > this.canvas.width) continue;

        const isSelected = (row === selectedRow && idx === selectedIdx);
        this.drawNote(notes[idx], x, rowY, isSelected);

        const { beats, isN } = this.getNoteInfo(notes[idx]);

        if (isN && idx > 0) {
          const prevInfo = this.getNoteInfo(notes[idx - 1]);
          cumulativeBeats += prevInfo.beats * 0.5;
        } else {
          cumulativeBeats += beats;
        }

        if (Math.abs(cumulativeBeats % this.beatsPerMeasure) < 0.001 && cumulativeBeats > 0) {
          const lineX = (idx + 1) * scaledCellWidth;
          const visualX = lineX - scrollX;
          if (visualX > -scaledCellWidth && visualX < this.canvas.width) {
            this.drawMeasureLine(visualX, rowY, scaledCellHeight);
          }
        }
      }
    }
  }

  drawMeasureLine(x, rowY, rowHeight) {
    this.ctx.strokeStyle = "#999999";
    this.ctx.lineWidth = 1;
    this.ctx.beginPath();
    this.ctx.moveTo(x, rowY);
    this.ctx.lineTo(x, rowY + rowHeight);
    this.ctx.stroke();
  }

  /**
   * Draw a single note
   */
  drawNote(note, x, rowY, selected) {
    const parsed = parseNoteValue(note.value);
    const scaledCellWidth = CELL_WIDTH * this.zoomScale;
    const scaledNoteSize = NOTE_SIZE * this.zoomScale;
    const scaledDotSize = DOT_SIZE * this.zoomScale;
    const scaledMarkerSize = MARKER_SIZE * this.zoomScale;

    const cx = x + scaledCellWidth / 2;
    const cy = rowY + CELL_HEIGHT * this.zoomScale / 2;

    // 1. Draw selected background
    if (selected) {
      this.drawSelectedBg(x, rowY, scaledCellWidth, CELL_HEIGHT * this.zoomScale);
    }

    // 2. High octave dot (directly above note center)
    if (parsed.isHighOctave) {
      this.drawDot(cx, cy - 30 * this.zoomScale, scaledDotSize);
    }

    // 3. Note number (colored by annotation)
    const noteColor = this.getNoteColor(note);
    this.drawNoteNumber(parsed.note || "?", cx, cy, noteColor, scaledNoteSize);

    // 4. Low octave dot (directly below note center)
    if (parsed.isLowOctave) {
      this.drawDot(cx, cy + 30 * this.zoomScale, scaledDotSize);
    }

    // 5. Beat lines below (6px spacing, scaled)
    if (parsed.beatLines > 0) {
      this.drawBeatLines(cx, cy + 32 * this.zoomScale, parsed.beatLines, this.zoomScale);
    }

    // 6. N modifier - small dot at lower right for extending previous note
    if (parsed.isN) {
      this.drawNDot(cx + 15 * this.zoomScale, cy + 10 * this.zoomScale, scaledDotSize * 0.7);
    }

    // 7. Suffix (to the right of note)
    if (parsed.suffix === ':') {
      this.drawSuffix(':', cx + 18 * this.zoomScale, cy, 16 * this.zoomScale);
    }
  }

  drawSelectedBg(x, y, width, height) {
    this.ctx.fillStyle = COLOR_SELECTED_BG;
    this.ctx.fillRect(x + 2 * this.zoomScale, y + 2 * this.zoomScale,
                      width - 4 * this.zoomScale, height - 4 * this.zoomScale);
  }

  drawMarkers(note, cx, y) {
    const markers = [];
    if (note.ban) markers.push({ label: '板', color: COLOR_BAN });
    if (note.yan) markers.push({ label: '眼', color: COLOR_YAN });
    if (note.guGan) markers.push({ label: '骨', color: COLOR_GU_GAN });

    if (markers.length === 0) return;

    const scaledMarkerSize = MARKER_SIZE * this.zoomScale;
    const startX = cx - (markers.length - 1) * 18 * this.zoomScale / 2;
    markers.forEach((marker, i) => {
      const mx = startX + i * 18 * this.zoomScale;
      this.drawMarkerCircle(mx, y, marker.color, scaledMarkerSize);
    });
  }

  drawMarkerCircle(x, y, color, size) {
    this.ctx.beginPath();
    this.ctx.arc(x, y, size, 0, Math.PI * 2);
    this.ctx.fillStyle = color;
    this.ctx.fill();
  }

  drawDot(x, y, size) {
    this.ctx.beginPath();
    this.ctx.arc(x, y, size, 0, Math.PI * 2);
    this.ctx.fillStyle = COLOR_DOT;
    this.ctx.fill();
  }

  // N modifier dot - smaller than octave dot
  drawNDot(x, y, size) {
    this.ctx.beginPath();
    this.ctx.arc(x, y, size, 0, Math.PI * 2);
    this.ctx.fillStyle = COLOR_DOT;
    this.ctx.fill();
  }

  drawNoteNumber(note, cx, cy, color = COLOR_NOTE, size = NOTE_SIZE) {
    this.ctx.font = `bold ${size}px sans-serif`;
    this.ctx.fillStyle = color;
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(note, cx, cy);
  }

  /**
   * Get color for note based on ban/yan/gu_gan annotations
   * Priority: gu_gan > yan > ban
   */
  getNoteColor(note) {
    if (note.guGan) return COLOR_GU_GAN;
    if (note.yan) return COLOR_YAN;
    if (note.ban) return COLOR_BAN;
    return COLOR_NOTE;
  }

  drawBeatLines(cx, y, count, scale) {
    this.ctx.strokeStyle = COLOR_DOT;
    this.ctx.lineWidth = LINE_WIDTH * scale;

    for (let i = 0; i < count; i++) {
      const ly = y + i * 6 * scale;
      this.ctx.beginPath();
      this.ctx.moveTo(cx - 12 * scale, ly);
      this.ctx.lineTo(cx + 12 * scale, ly);
      this.ctx.stroke();
    }
  }

  drawSuffix(suffix, x, y, fontSize = 16) {
    this.ctx.font = `${fontSize}px sans-serif`;
    this.ctx.fillStyle = COLOR_DOT;
    this.ctx.textAlign = 'left';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(suffix, x, y);
  }

  /**
   * Hit test - returns note index at given x position
   */
  hitTest(x, scrollX) {
    const scaledCellWidth = CELL_WIDTH * this.zoomScale;
    const idx = Math.floor((x + scrollX) / scaledCellWidth);
    return idx;
  }
}

export { JianpuRenderer, CELL_WIDTH, CELL_HEIGHT };
