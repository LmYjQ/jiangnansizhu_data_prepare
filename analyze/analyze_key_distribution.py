import json
import sys
from collections import Counter

if len(sys.argv) < 2:
    print("用法: python analyze_key_distribution.py <json文件名>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

part_counts = Counter()
outliers = {}

for k in data.keys():
    n = len(k.split('|'))
    part_counts[n] += 1
    if n >= 5:
        outliers[n] = (k, data[k]['count'])

print(f'文件: {filename}')
print(f'总key数: {len(data)}')
print()
print('段数分布:')
for n in sorted(part_counts.keys()):
    print(f'  {n}段: {part_counts[n]}个key')

print()
print('>=5段的key:')
for n in sorted(outliers.keys()):
    k, cnt = outliers[n]
    display = k[:100] + '...' if len(k) > 100 else k
    print(f'  {n}段 (count={cnt}): {display}')