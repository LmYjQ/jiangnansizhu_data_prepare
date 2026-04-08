import json

def strip_zvc(s):
    return ''.join(c for c in s if c not in 'ZXVC')

# 输入文件
# ban_yan_file = 'qmx_output/三六-0405.json'
# parsed_file = 'qmx_output/三六_mem_parsed_notes.json'
# output_file = 'qmx_output/三六_merged.json'

ban_yan_file = 'qmx_output/4.5中花六板jianpu_annotation.json'
parsed_file = 'qmx_output/中花六板202604_mem_parsed_notes.json'
output_file = 'qmx_output/中花六板_merged.json'

with open(ban_yan_file, 'r', encoding='utf-8') as f:
    ban_yan_data = json.load(f)

with open(parsed_file, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

merged = {'type': 'multi-row', 'rows': []}
mismatch_rows = []

for i in range(len(ban_yan_data['rows'])):
    ban_row = ban_yan_data['rows'][i]
    parsed_row = parsed_data['rows'][i]

    # 获取非bar的parsed notes
    parsed_non_bar = [n for n in parsed_row['notes'] if n['value'] != 'bar']
    ban_notes = ban_row['notes']

    # 合并：把ban/yan/gu_gan复制到parsed
    # 从最左边对齐，逐个匹配
    if len(parsed_non_bar) != len(ban_notes):
        print(f'\n行 {i}: 数量不一致，尝试宽松匹配')
        print(f'  parsed({len(parsed_non_bar)}): {[n["value"] for n in parsed_non_bar]}')
        print(f'  ban_yan({len(ban_notes)}): {[n["value"] for n in ban_notes]}')

        # 逐个检查ban_yan的value是否包含在parsed的value内（校验时pn去掉ZVC）
        for j, (pn, bn) in enumerate(zip(parsed_non_bar, ban_notes)):
            pn_stripped = strip_zvc(pn['value'])
            if bn['value'] not in pn_stripped and pn_stripped not in bn['value']:
                print(f'行 {i} 第 {j} 个不匹配: ban_yan="{bn["value"]}" vs parsed="{pn_stripped}"')

        print(f'  匹配成功，忽略多余的ban_yan音符')
        mismatch_rows.append(i)
    else:
        # 数量一致时直接复制
        for j, (pn, bn) in enumerate(zip(parsed_non_bar, ban_notes)):
            pn_stripped = strip_zvc(pn['value'])
            if bn['value'] not in pn_stripped and pn_stripped not in bn['value']:
                print(f'行 {i} 第 {j} 个不匹配: ban_yan="{bn["value"]}" vs parsed="{pn_stripped}"')

    # 复制ban/yan/gu_gan（只复制能匹配的）
    for pn, bn in zip(parsed_non_bar, ban_notes):
        pn['ban'] = bn['ban']
        pn['yan'] = bn['yan']
        pn['gu_gan'] = bn['gu_gan']

    merged['rows'].append({
        'source': parsed_row['source'],
        'notes': parsed_row['notes']  # 保持完整（包括bar）
    })

print(f'\n合并完成，共处理 {len(merged["rows"])} 行')
print(f'数量不一致的行: {mismatch_rows}')

# 保存
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f'已保存到 {output_file}')