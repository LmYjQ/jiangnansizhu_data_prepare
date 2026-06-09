import json
from collections import defaultdict

def compute_markov_matrix(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 统计外层键 -> 内层键 的总次数
    outer_to_inner_counts = defaultdict(lambda: defaultdict(int))
    total_outer_counts = defaultdict(int)

    for outer_key, inner_dict in data.items():
        for inner_key, patterns in inner_dict.items():
            for pattern, occurrences in patterns.items():
                cnt = len(occurrences)
                outer_to_inner_counts[outer_key][inner_key] += cnt
                total_outer_counts[outer_key] += cnt

    # 收集所有内层键（作为列）
    all_inner_keys = sorted(set(
        inner for outer_dict in outer_to_inner_counts.values() for inner in outer_dict.keys()
    ), key=int)  # 按数值排序

    # 输出矩阵（行：外层键，列：内层键，值：概率）
    print("马尔可夫链矩阵（外层键 → 内层键 转移概率）\n")
    header = "\t" + "\t".join(all_inner_keys)
    print(header)
    for outer_key in sorted(outer_to_inner_counts.keys(), key=int):
        row = []
        total = total_outer_counts[outer_key]
        for inner_key in all_inner_keys:
            cnt = outer_to_inner_counts[outer_key].get(inner_key, 0)
            prob = cnt / total if total > 0 else 0
            row.append(f"{prob:.4f}")
        print(f"{outer_key}\t" + "\t".join(row))

if __name__ == "__main__":
    compute_markov_matrix("transition_pattern_agg.json")