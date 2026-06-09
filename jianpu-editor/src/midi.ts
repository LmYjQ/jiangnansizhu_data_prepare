import { Score } from './types';

/**
 * MIDI导出器
 * 将简谱转换为MIDI格式
 */
export class MidiExporter {
  private score: Score;

  constructor(score: Score) {
    this.score = score;
  }

  /**
   * 简谱数字转MIDI音符
   * 简谱1=C4(60)，简谱2=D4(62)，以此类推
   * octave是正数表示高音，负数表示低音
   */
  private noteToMidi(value: string, octave: number): number {
    if (value === '0') return -1; // 休止符

    const noteNum = parseInt(value);
    if (isNaN(noteNum) || noteNum < 1 || noteNum > 7) return -1;

    // 简谱1-7对应C4-D4，即MIDI 60-72
    // 简谱1=C, 2=D, 3=E, 4=F, 5=G, 6=A, 7=B
    // C=0, D=2, E=4, F=5, G=7, A=9, B=11
    const pitchOffsets = [0, 0, 2, 4, 5, 7, 9, 11];
    const baseNote = 60 + pitchOffsets[noteNum]; // C4 = 60

    // 调整八度
    return baseNote + (octave + 1) * 12;
  }

  /**
   * 时值转ticks
   * 假设480 ticks per quarter note
   */
  private durationToTicks(duration: number): number {
    const quarterTicks = 480;
    return Math.round(quarterTicks / duration);
  }

  /**
   * 生成MIDI文件
   */
  generate(): Uint8Array {
    const ticksPerQuarter = 480;
    let tick = 0;
    const events: Array<{ type: number; tick: number; data: number[] }> = [];

    // 设置速度事件
    const tempo = Math.round(60000000 / this.score.tempo);
    events.push({ type: 0x51, tick: 0, data: [tempo] });

    // 音轨结束事件
    let lastTick = 0;

    for (const note of this.score.notes) {
      // 跳过小节线和空格
      if (note.value === 'bar' || note.value === 'space') continue;

      if (note.value === '0') {
        tick += this.durationToTicks(note.duration);
        continue;
      }

      const midiNote = this.noteToMidi(note.value, note.octave);
      if (midiNote < 0) continue;

      // 计算实际时值（包括附点）
      const actualDuration = note.dotted ? note.duration * 1.5 : note.duration;
      const noteTicks = this.durationToTicks(actualDuration);

      // Note On事件 (90 = note on in track 1)
      events.push({ type: 0x90, tick: tick, data: [midiNote, 64] });
      // Note Off事件
      events.push({ type: 0x80, tick: tick + noteTicks, data: [midiNote, 0] });

      tick += noteTicks;
      lastTick = tick;
    }

    // 添加结束事件
    events.push({ type: 0xFF, tick: lastTick, data: [0x2F, 0] });

    return this.buildMidiFile(events, ticksPerQuarter);
  }

  /**
   * 构建MIDI文件
   */
  private buildMidiFile(events: Array<{ type: number; tick: number; data: number[] }>, ticksPerQuarter: number): Uint8Array {
    // MIDI文件头: MThd
    const header: number[] = [0x4D, 0x54, 0x68, 0x64];
    // 格式0，1 track，480 ticks/quarter
    header.push(0, 1, 0, 1);
    header.push((ticksPerQuarter >> 8) & 0xFF, ticksPerQuarter & 0xFF);

    // 音轨头: MTrk
    const track: number[] = [0x4D, 0x54, 0x72, 0x6B];

    const trackData: number[] = [];

    for (const event of events) {
      // 写入delta time（变长格式）
      const deltaTime = event.tick;
      trackData.push(...this.writeVarLen(deltaTime));

      // 写入事件
      if (event.type === 0x51) {
        // Tempo
        trackData.push(0xFF, 0x51, 0x03, ...event.data);
      } else if (event.type === 0xFF) {
        // End of Track
        trackData.push(0xFF, 0x2F, 0x00);
      } else if (event.type === 0x90 || event.type === 0x80) {
        // Note On/Off
        trackData.push(event.type, ...event.data);
      }
    }

    // 写入音轨长度
    track.push((trackData.length >> 24) & 0xFF, (trackData.length >> 16) & 0xFF, (trackData.length >> 8) & 0xFF, trackData.length & 0xFF);
    track.push(...trackData);

    return new Uint8Array([...header, ...track]);
  }

  /**
   * 写入变长数字
   */
  private writeVarLen(value: number): number[] {
    const result: number[] = [];
    let v = value;
    result.push(v & 0x7F);
    while (v > 0x7F) {
      v >>= 7;
      result.unshift((v & 0x7F) | 0x80);
    }
    return result;
  }

  /**
   * 保存为MIDI文件
   */
  async save(filename: string): Promise<void> {
    const data = this.generate();
    const blob = new Blob([data], { type: 'audio/midi' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = filename;
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
  }

  /**
   * 导出为Data URL
   */
  toDataUrl(): string {
    const data = this.generate();
    let binary = '';
    for (let i = 0; i < data.length; i++) {
      binary += String.fromCharCode(data[i]);
    }
    return 'data:audio/midi;base64,' + btoa(binary);
  }
}