/**
 * 简谱音符数据结构
 *
 * 音符类型:
 * - "1"-"7": 音符
 * - "0": 休止符
 * - "bar": 小节线
 * - "space": 空格
 */
export interface Note {
  id: number; // 唯一标识
  value: string; // 音符音名: "0"-"7", "bar", "space"
  octave: number; // 八度调整，正数=高音，负数=低音
  type: number | null; // 音符类型 (按照音符的时值分类，99=全音符, 2=二分音符, 1=四分音符, 0.5=八分音符, 0.25=十六分音符,null=未知)
  duration: number; // 时值，实际时值=type * (1 + (dotted ? 0.5 : 0))，单位为拍
  dotted: boolean; // 是否附点
  ban: number; // 板眼：板=强拍 (0=无, 1=板)
  yan: number; // 板眼：眼=弱拍 (0=无, 1=眼)
  lineBreak: boolean; // 手动分页符（在该音符后换行）
}

/**
 * 乐曲数据
 */
export interface Score {
  title: string; // 曲名
  tempo: number; // 速度（BPM）
  beatsPerBar: number; // 每小节拍数
  notes: Note[]; // 音符列表
}

/**
 * 音符渲染信息
 */
export interface NoteRenderInfo {
  id: number; // 音符ID
  x: number; // x坐标
  y: number; // y坐标（音符基线）
  width: number; // 宽度
  height: number; // 高度
  row: number; // 行号
  type: number | null; // 音符类型（按照时值分类，99=全音符, 2=二分音符, 1=四分音符, 0.5=八分音符, 0.25=十六分音符,null=未知）
  value: string; // 音符音名
  octave: number; // 八度
  duration: number; // 时值
  dotted: boolean; // 附点
  beatLines: number; // 拍线条数
  lineBreak: boolean; // 分页符
}

/**
 * 渲染配置
 */
export interface RenderConfig {
  noteFontSize: number; // 音符字体大小
  lineSpacing: number; // 行间距
  noteSpacing: number; // 音符间距
  beatLineHeight: number; // 拍线高度
  dotRadius: number; // 点半径
  octaveDotOffset: number; // 八度点偏移
}

export const DEFAULT_CONFIG: RenderConfig = {
  noteFontSize: 24,
  lineSpacing: 80,
  noteSpacing: 20,
  beatLineHeight: 20,
  dotRadius: 3,
  octaveDotOffset: 12,
};
