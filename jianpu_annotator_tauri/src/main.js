/**
 * 简谱标注器 - 主入口
 * Ported from main_window.py
 */

import { JianpuRenderer, CELL_WIDTH, CELL_HEIGHT } from './renderer.js';
import { NoteAnnotation, AnnotationProject, MultiRowAnnotationProject, loadParsedNotesCsv } from './annotation.js';
import { open, save } from '@tauri-apps/plugin-dialog';
import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs';

// Application state
const state = {
  project: null,
  selectedIdx: -1,
  selectedRow: 0,
  scrollX: 0,
  csvData: [],
  csvPath: '',
  viewMode: 'single',  // 'single' or 'all'
  allProjects: [],       // Array of projects for "all" mode
  rowRenderers: []       // Array of renderers, one per row in "all" mode
};

// DOM elements
const elements = {
  csvPath: document.getElementById('csv-path'),
  lineNumber: document.getElementById('line-number'),
  beatsPerMeasure: document.getElementById('beats-per-measure'),
  zoomLevel: document.getElementById('zoom-level'),
  zoomDisplay: document.getElementById('zoom-display'),
  viewMode: document.getElementById('view-mode'),
  btnBrowse: document.getElementById('btn-browse'),
  btnLoadLine: document.getElementById('btn-load-line'),
  btnImport: document.getElementById('btn-import'),
  btnExport: document.getElementById('btn-export'),
  canvasScroll: document.getElementById('canvas-scroll'),
  singleRowView: document.getElementById('single-row-view'),
  allRowsView: document.getElementById('all-rows-view'),
  canvas: document.getElementById('jianpu-canvas'),
  selectedInfo: document.getElementById('selected-info'),
  statusText: document.getElementById('status-text')
};

// Initialize renderer
const renderer = new JianpuRenderer(elements.canvas);
renderer.resize(1);

// Event handlers
async function onPickCsv() {
  try {
    const selected = await open({
      title: '选择 parsed_notes.csv',
      filters: [{ name: 'CSV', extensions: ['csv'] }]
    });

    if (selected) {
      elements.csvPath.value = selected;
      state.csvPath = selected;

      const content = await readTextFile(selected);
      state.csvData = loadParsedNotesCsv(content);

      if (!state.csvData.length) {
        setStatus('CSV 文件无有效数据');
        return;
      }

      // Auto load all rows in multi-row mode
      state.allProjects = state.csvData.map((row) => {
        const rowNotes = row.notes.map((v, i) => new NoteAnnotation(i, v, 0, 0, 0));
        return new AnnotationProject(row.source, rowNotes);
      });

      state.viewMode = 'all';
      elements.viewMode.value = 'all';
      state.project = state.allProjects[0];
      state.selectedRow = 0;
      state.selectedIdx = -1;
      state.scrollX = 0;

      const zoomScale = parseInt(elements.zoomLevel.value, 10) / 100;
      renderer.setZoom(zoomScale);
      setupAllRowsView();
      redrawCanvas();

      setStatus(`加载成功，共 ${state.csvData.length} 行`);
    }
  } catch (err) {
    setStatus(`加载失败: ${err}`);
  }
}

async function onLoadLine() {
  if (!state.csvData.length) {
    setStatus('请先加载 CSV 文件');
    return;
  }

  const lineNum = parseInt(elements.lineNumber.value, 10);
  if (isNaN(lineNum) || lineNum < 1) {
    setStatus('请输入有效的行号');
    return;
  }

  const rowData = state.csvData.find(d => d.line === lineNum);
  if (!rowData) {
    setStatus(`行 ${lineNum} 无有效数据`);
    return;
  }

  // Create annotation project
  const notes = rowData.notes.map((v, i) => new NoteAnnotation(i, v, 0, 0, 0));
  state.project = new AnnotationProject(rowData.source, notes);
  state.selectedIdx = -1;
  state.selectedRow = 0;
  state.scrollX = 0;

  // Prepare all projects for "all" mode
  state.allProjects = state.csvData.map((row, idx) => {
    const rowNotes = row.notes.map((v, i) => new NoteAnnotation(i, v, 0, 0, 0));
    return new AnnotationProject(row.source, rowNotes);
  });

  // Resize canvas
  const zoomScale = parseInt(elements.zoomLevel.value, 10) / 100;
  renderer.setZoom(zoomScale);

  if (state.viewMode === 'all') {
    setupAllRowsView();
  } else {
    renderer.resize(notes.length);
  }
  redrawCanvas();
  setStatus(`加载第 ${lineNum} 行，共 ${notes.length} 个音符`);
}

// Setup multiple rows for "all" mode
function setupAllRowsView() {
  elements.singleRowView.style.display = 'none';
  elements.allRowsView.style.display = 'flex';

  // Clear existing
  elements.allRowsView.innerHTML = '';
  state.rowRenderers = [];

  const zoomScale = parseInt(elements.zoomLevel.value, 10) / 100;

  // Create a row for each project
  state.allProjects.forEach((project, rowIdx) => {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'canvas-row';

    const label = document.createElement('span');
    label.className = 'row-label';
    label.textContent = `行${rowIdx + 1}`;
    rowDiv.appendChild(label);

    const canvas = document.createElement('canvas');
    // Use a fixed base height that will be scaled, but canvas-row takes remaining space
    canvas.height = 100;
    rowDiv.appendChild(canvas);

    const scrollDiv = document.createElement('div');
    scrollDiv.className = 'canvas-scroll-inner';
    scrollDiv.style.overflowX = 'auto';
    scrollDiv.style.width = '100%';
    scrollDiv.style.flex = '1';
    scrollDiv.appendChild(canvas);
    rowDiv.appendChild(scrollDiv);

    elements.allRowsView.appendChild(rowDiv);

    // Create renderer for this row
    const rowRenderer = new JianpuRenderer(canvas);
    rowRenderer.setZoom(zoomScale);
    rowRenderer.resize(project.notes.length);
    state.rowRenderers.push({ renderer: rowRenderer, scrollEl: scrollDiv, canvas: canvas });

    // Bind scroll event
    scrollDiv.addEventListener('scroll', () => {
      const scrollX = scrollDiv.scrollLeft;
      rowRenderer.draw(project.notes, state.selectedRow === rowIdx ? state.selectedIdx : -1, scrollX);
    });

    // Bind click event
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const idx = rowRenderer.hitTest(x, scrollDiv.scrollLeft);

      if (idx >= 0 && idx < project.notes.length) {
        state.project = project;
        state.selectedRow = rowIdx;
        state.selectedIdx = idx;
        redrawCanvas();
        updateSelectedInfo();
        setStatus(`选中行${rowIdx + 1} 音符${idx + 1}: ${project.notes[idx].value}`);
      }
    });
  });
}

async function onImport() {
  try {
    const selected = await open({
      title: '选择 JSON 文件',
      filters: [{ name: 'JSON', extensions: ['json'] }]
    });

    if (selected) {
      const content = await readTextFile(selected);
      const data = JSON.parse(content);

      if (data.type === 'multi-row') {
        // Import multi-row project
        const multiProject = MultiRowAnnotationProject.fromDict(data);
        state.allProjects = multiProject.projects;
        state.viewMode = 'all';
        elements.viewMode.value = 'all';
        state.project = state.allProjects[0];
        state.selectedRow = 0;
        setupAllRowsView();
        setStatus(`导入成功，共 ${state.allProjects.length} 行`);
      } else {
        // Import single-row project
        state.project = AnnotationProject.fromDict(data);
        state.viewMode = 'single';
        elements.viewMode.value = 'single';
        state.allProjects = [];
      }
      state.selectedIdx = -1;
      state.scrollX = 0;

      const zoomScale = parseInt(elements.zoomLevel.value, 10) / 100;
      renderer.setZoom(zoomScale);

      if (state.viewMode === 'all') {
        setupAllRowsView();
      } else {
        renderer.resize(state.project.notes.length);
      }
      redrawCanvas();
      setStatus(`导入成功，共 ${state.viewMode === 'all' ? state.allProjects.length + '行' : state.project.notes.length + '个音符'}`);
    }
  } catch (err) {
    setStatus(`导入失败: ${err}`);
  }
}

async function onExport() {
  if (!state.project && state.viewMode !== 'all') {
    setStatus('请先加载或导入简谱');
    return;
  }

  try {
    const savePath = await save({
      title: '保存 JSON 文件',
      defaultPath: 'jianpu_annotation.json',
      filters: [{ name: 'JSON', extensions: ['json'] }]
    });

    if (savePath) {
      let jsonContent;
      if (state.viewMode === 'all' && state.allProjects.length > 0) {
        const multiProject = new MultiRowAnnotationProject(state.allProjects);
        jsonContent = multiProject.toJson();
      } else {
        jsonContent = state.project.toJson();
      }
      await writeTextFile(savePath, jsonContent);
      setStatus(`导出成功: ${savePath}`);
    }
  } catch (err) {
    setStatus(`导出失败: ${err}`);
  }
}

// Single-row canvas click handler
function onSingleCanvasClick(e) {
  if (!state.project || state.viewMode === 'all') return;

  const rect = elements.canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;

  const idx = renderer.hitTest(x, state.scrollX);
  if (idx >= 0 && idx < state.project.notes.length) {
    state.selectedIdx = idx;
    state.selectedRow = 0;
    redrawCanvas();
    updateSelectedInfo();
    setStatus(`选中音符 ${idx + 1}: ${state.project.notes[idx].value}`);
  }
}

function onCanvasScroll(e) {
  state.scrollX = e.target.scrollLeft;
  redrawCanvas();
}

function onKeyDown(e) {
  if (!state.project || state.selectedIdx < 0) return;

  const key = e.key.toUpperCase();
  const note = state.project.notes[state.selectedIdx];

  switch (key) {
    case 'B':
      note.toggleBan();
      redrawCanvas();
      updateSelectedInfo();
      setStatus(`音符 ${state.selectedIdx + 1}: 板=${note.ban ? '是' : '否'}`);
      e.preventDefault();
      break;
    case 'Y':
      note.toggleYan();
      redrawCanvas();
      updateSelectedInfo();
      setStatus(`音符 ${state.selectedIdx + 1}: 眼=${note.yan ? '是' : '否'}`);
      e.preventDefault();
      break;
    case 'G':
      note.toggleGuGan();
      redrawCanvas();
      updateSelectedInfo();
      setStatus(`音符 ${state.selectedIdx + 1}: 骨干音=${note.guGan ? '是' : '否'}`);
      e.preventDefault();
      break;
    case 'ARROWLEFT':
      if (state.selectedIdx > 0) {
        state.selectedIdx--;
        redrawCanvas();
        updateSelectedInfo();
      }
      e.preventDefault();
      break;
    case 'ARROWRIGHT':
      if (state.selectedIdx < state.project.notes.length - 1) {
        state.selectedIdx++;
        redrawCanvas();
        updateSelectedInfo();
      }
      e.preventDefault();
      break;
  }
}

function redrawCanvas() {
  renderer.beatsPerMeasure = parseInt(elements.beatsPerMeasure.value, 10) || 4;
  const zoomScale = parseInt(elements.zoomLevel.value, 10) / 100;
  renderer.setZoom(zoomScale);

  if (state.viewMode === 'all' && state.allProjects.length > 0) {
    // Switch view if needed
    if (elements.singleRowView.style.display !== 'none') {
      elements.singleRowView.style.display = 'none';
    }
    if (elements.allRowsView.style.display === 'none') {
      setupAllRowsView();
    }

    // Update all row renderers
    state.rowRenderers.forEach((rowData, rowIdx) => {
      rowData.renderer.beatsPerMeasure = renderer.beatsPerMeasure;
      rowData.renderer.setZoom(zoomScale);

      rowData.renderer.resize(state.allProjects[rowIdx].notes.length);

      const scrollX = rowData.scrollEl.scrollLeft;
      const selectedIdx = (state.selectedRow === rowIdx) ? state.selectedIdx : -1;
      rowData.renderer.draw(state.allProjects[rowIdx].notes, selectedIdx, scrollX);
    });
  } else if (state.project) {
    // Single row mode
    if (elements.allRowsView.style.display !== 'none') {
      elements.allRowsView.style.display = 'none';
      elements.singleRowView.style.display = 'block';
    }
    renderer.resize(state.project.notes.length);
    renderer.draw(state.project.notes, state.selectedIdx, state.scrollX);
  } else {
    renderer.clear();
  }
}

function updateSelectedInfo() {
  if (!state.project || state.selectedIdx < 0) {
    elements.selectedInfo.textContent = '无选中音符';
    return;
  }

  const note = state.project.notes[state.selectedIdx];
  elements.selectedInfo.textContent =
    `音符: ${note.value}\n` +
    `板: ${note.ban ? '是' : '否'}\n` +
    `眼: ${note.yan ? '是' : '否'}\n` +
    `骨干音: ${note.guGan ? '是' : '否'}`;
}

function setStatus(msg) {
  elements.statusText.textContent = msg;
}

// Bind events
elements.btnBrowse.addEventListener('click', onPickCsv);
elements.btnLoadLine.addEventListener('click', onLoadLine);
elements.btnImport.addEventListener('click', onImport);
elements.btnExport.addEventListener('click', onExport);
elements.canvas.addEventListener('click', onSingleCanvasClick);
elements.canvasScroll.addEventListener('scroll', onCanvasScroll);
elements.beatsPerMeasure.addEventListener('change', redrawCanvas);

// Zoom control
elements.zoomLevel.addEventListener('input', () => {
  elements.zoomDisplay.textContent = elements.zoomLevel.value + '%';
  redrawCanvas();
});

// View mode toggle
elements.viewMode.addEventListener('change', () => {
  state.viewMode = elements.viewMode.value;
  state.selectedIdx = -1;
  state.selectedRow = 0;
  state.scrollX = 0;
  redrawCanvas();
  setStatus(state.viewMode === 'all' ? '切换到全部模式' : '切换到单行模式');
});

document.addEventListener('keydown', onKeyDown);

// Initial status
setStatus('就绪');
