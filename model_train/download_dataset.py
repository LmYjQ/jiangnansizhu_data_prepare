from music21 import corpus, note, chord

# ==========================================
# 辅助函数：将 music21 的音符流转换为数字序列
# ==========================================
def extract_pitch_sequence(part):
    """
    遍历音轨，提取 MIDI 音高。休止符用 -1 表示。
    """
    sequence = []
    # flatten() 将嵌套的小节展平，notesAndRests 过滤掉拍号、谱号等非音符元素
    for element in part.flatten().notesAndRests:
        if isinstance(element, note.Note):
            sequence.append(element.pitch.midi) # 获取 MIDI 数字 (如中音Do = 60)
        elif isinstance(element, chord.Chord):
            # 如果遇到和弦，取最高音作为旋律音
            sequence.append(element.sortAscending()[-1].pitch.midi)
        elif isinstance(element, note.Rest):
            sequence.append(-1) # -1 代表休止符
    return sequence



print("\n====== 测试 2: 巴赫众赞歌 (用于 IOHMM 的骨肉双轨提取) ======")
# 获取所有巴赫众赞歌
bach_chorales = corpus.chorales.Iterator()
# 拿第一首来测试
bach_piece = next(bach_chorales)
# 巴赫众赞歌标准为4个声部 (Soprano高音, Alto中音, Tenor次中音, Bass低音)
# 我们提取 Soprano 作为“加花/肉”(Output Y)
soprano_part = bach_piece.parts[0] 
# 我们提取 Bass 作为“骨干/背景约束”(Input X)
bass_part = bach_piece.parts[3]

melody_y = extract_pitch_sequence(soprano_part)
bone_x = extract_pitch_sequence(bass_part)

print(f"【巴赫曲名】: BWV {bach_piece.metadata.number}")
print(f"【高音旋律 Y (肉) (前20个音)】: \n{melody_y[:20]}")
print(f"【低音骨干 X (骨) (前20个音)】: \n{bone_x[:20]}")
print("-" * 50)

# 导出乐谱为 musicxml 文件（可用 MuseScore 等打开）
import os
os.makedirs('output', exist_ok=True)
xml_path = 'output/bach_chorale_BWV{}.xml'.format(bach_piece.metadata.number)
bach_piece.write('musicxml', fp=xml_path)
print(f"【乐谱已导出】: {xml_path}")
print("【提示】请用 MuseScore 或其他乐谱软件打开 XML 文件查看可视化效果")

# ==========================================
# 进阶提示：如何对齐它们？
# ==========================================
print("\n[对齐提示]: 在机器学习中，需要保证 X 和 Y 长度一致。")
print(f"当前旋律音符数: {len(melody_y)}, 低音音符数: {len(bone_x)}")
print("注意：因为高音经常唱 8分音符，低音唱 4分音符，所以它们直接提取出来的列表长度可能不同。")
print("在真正构建 IOHMM 时，你需要按时间网格（如每 16分音符 截取一次）来对齐这两个列表。")