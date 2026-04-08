import json
import sys

if len(sys.argv) < 2:
    print("用法: python check_rhythm.py <每小节拍数>")
    sys.exit(1)

beats_per_bar = float(sys.argv[1])

with open('qmx_output/三六_merged.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_rows = len(data['rows'])
print(f'总行数: {total_rows}')
print()

errors = []
for row_idx, row in enumerate(data['rows']):
    accumulated_value = ''
    accumulated_duration = 0.0

    for note in row['notes']:
        value = note['value']
        duration = note['duration']

        accumulated_value += ' ' +value
        accumulated_duration += duration

        if value == 'bar':
            # 检查每小节的时长
            if abs(accumulated_duration - beats_per_bar) > 0.01:
                errors.append(f'行{row_idx}: 累计时长={accumulated_duration}, 期望={beats_per_bar}, 内容={accumulated_value[:50]}...')
            print(f'行{row_idx}: duration累计={accumulated_duration}, value={accumulated_value}')
            accumulated_value = ''
            accumulated_duration = 0.0

    # 行结束时如果还有累计（最后没有bar的情况）
    if accumulated_duration > 0:
        print(f'行{row_idx} (末尾): duration累计={accumulated_duration}, value={accumulated_value[:30]}...')

print()
if errors:
    print(f'发现 {len(errors)} 个问题:')
    for e in errors:
        print(e)
else:
    print('校验完成，未发现问题')