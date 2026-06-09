# 简谱编辑器 (jianpu-editor)

简谱编辑器是一个基于 Canvas + TypeScript 构建的 Web 乐谱编辑工具，支持简谱 1-7 音符的输入、编辑、渲染和导出。

## 项目结构

```
jianpu-editor/
├── index.html          # 主页面 HTML
├── package.json       # 项目配置
├── vite.config.ts     # Vite 构建配置
├── tsconfig.json      # TypeScript 配置
└── src/
    ├── main.ts        # 前端主逻辑（事件绑定、UI 交互）
    ├── editor.ts      # Editor 类（乐谱编辑、撤销/重做）
    ├── renderer.ts    # JianpuRenderer 类（Canvas 渲染）
    ├── midi.ts        # MidiExporter 类（MIDI 导出）
    ├── types.ts       # 类型定义和数据结构
    └── styles.css     # 样式文件
    └── component
        ├── slection.ts    # 批量选择
        ├── shortcuts.ts    # 快捷键操作
        ├── history.ts    # 历史记录

```

## 核心模块

### 1. types.ts — 数据结构

**Note（音符）**

```typescript
interface Note {
  id: number; // 唯一标识
  value: string; // 音符值: "1"-"7", "0"(休止), "bar"(小节线), "space"(空格)
  octave: number; // 八度调整，+1=高八度，-1=低八度
  duration: number; // 时值，四分音符=1
  dotted: boolean; // 是否附点
  ban: number; // 板眼：板=强拍 (0/1)
  yan: number; // 板眼：眼=弱拍 (0/1)
}
```

**Score（乐谱）**

```typescript
interface Score {
  title: string; // 曲名
  tempo: number; // 速度（BPM）
  beatsPerBar: number; // 每小节拍数
  notes: Note[]; // 音符列表
}
```

### 2. renderer.ts — 渲染引擎

`JianpuRenderer` 类负责将乐谱数据绘制到 Canvas 上。

**换行逻辑**：`render()` 方法中，每行能容纳的音符数由 `floor((canvas.width - 80) / noteSpacing)` 计算，固定数量换行而非按小节换行。

**拍线绘制**：根据时值决定拍线条数 — 全音符(≥1)无拍线，≥0.5 拍 1 条，≥0.25 拍 2 条，<0.25 拍 3 条。换行时拍线断开重绘。

**可见性裁剪**：只渲染 `x > -noteSpacing && x < width + noteSpacing` 范围内的音符。

**八度点**：高音点在音符上方，低音点在拍线下方。

### 3. editor.ts — 编辑器核心

`Editor` 类封装乐谱编辑操作，提供撤销/重做（最多 50 步历史）。

主要方法：`addNote`、`updateNote`、`deleteNote`、`importScore`、`exportScore`

### 4. midi.ts — MIDI 导出

`MidiExporter` 类将简谱转换为 MIDI 文件。

**音高映射**：简谱 1-7 → C4-D4 (MIDI 60-72)，八度调整通过 `±12` 实现。

**时值转 ticks**：`480 ticks / quarter` 为基准，`ticks = 480 / duration`。

### 5. main.ts — UI 交互层

事件绑定层，处理工具栏点击、键盘快捷键、鼠标拖动滚动等。

**快捷键一览**：

| 按键         | 功能                   |
| ------------ | ---------------------- |
| `0-7`        | 插入音符（编辑模式）   |
| `空格`       | 插入空格               |
| `x`          | 插入小节线             |
| `.`          | 切换附点（需选中音符） |
| `b`          | 切换板 / 插入小节线    |
| `y`          | 切换眼                 |
| `↑/↓`        | 调整八度（编辑模式）   |
| `←/→`        | 调整时值（编辑模式）   |
| `Shift+滚轮` | 横向滚动               |
| `Ctrl+Z`     | 撤销                   |
| `Ctrl+Y`     | 重做                   |
| `Delete`     | 删除选中音符           |

**编辑模式 vs 选择模式**：

- **编辑模式**：方向键调整选中音符的属性
- **选择模式**：方向键切换选中音符

## 数据流

```
用户操作 (键盘/鼠标/按钮)
    ↓
main.ts 事件处理
    ↓
Editor / 直接操作 score
    ↓
JianpuRenderer.render()
    ↓
Canvas 绘制
```

## 导出格式

- **JSON**：完整乐谱数据，含所有音符属性
- **PNG**：Canvas 截图
- **MIDI**：标准 MIDI Format 0，单音轨

## 快速开始

```powershell
cd jianpu-editor
npm install
npm run dev
```
