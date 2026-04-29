import json
import os
from collections import defaultdict


def get_beat_words(row):
    """Return list of beat words (space-joined note values) for a row."""
    words = []
    duration_cumulative = 0.0
    beat_notes = []
    beat_position = 0.0

    for note in row['notes']:
        if note['value'] == 'bar':
            continue
        if 'token_dict' in note:
            beat_notes.append(note['token_dict']['main_value'])
        else:
            beat_notes.append(note['value'])
        duration_cumulative += note['duration']
        beat_position += note['duration']

        if abs(duration_cumulative % 1.0) < 0.001:
            words.append((beat_position, ' '.join(beat_notes)))
            duration_cumulative = 0.0
            beat_notes = []

    # Handle partial beat at end
    if beat_notes:
        words.append((beat_position, ' '.join(beat_notes) + ' [partial]'))

    return words


def analyze_ngram(json_file, n=2):
    """Return list of (ngram_tuple, end_position, row_idx) for each n-gram in the file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    ngrams = []
    for row_idx, row in enumerate(data['rows']):
        words = get_beat_words(row)
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i + j][1] for j in range(n))
            end_pos = words[i + n - 1][0]
            ngrams.append((ngram, end_pos, row_idx + 1, json_file))
    return ngrams


if __name__ == '__main__':
    # 可配置 n-gram 大小
    N = 12

    dataset_dir = 'dataset'
    all_ngrams = []

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            ngrams = analyze_ngram(json_path, n=N)
            all_ngrams.extend(ngrams)

    # Aggregate by n-gram key
    result = defaultdict(lambda: {"count": 0, "occurrences": []})

    for ngram, beat_pos, row_no, filepath in all_ngrams:
        key = " | ".join(ngram)
        result[key]["count"] += 1
        result[key]["occurrences"].append({
            "file": os.path.basename(filepath),
            "row": row_no,
            "beat": round(beat_pos, 3)
        })

    sorted_result = {k: v for k, v in sorted(result.items(), key=lambda x: -x[1]["count"]) if v["count"] > 1}

    output_path = f"transition_{N}gram.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_result, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}, total {N}-grams: {len(sorted_result)}")
