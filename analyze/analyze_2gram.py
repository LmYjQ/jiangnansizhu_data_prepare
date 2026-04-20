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


def analyze_2gram(json_file):
    """Return list of (prev_word, next_word, beat_position, row_idx) for each consecutive beat pair in the file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pairs = []
    for row_idx, row in enumerate(data['rows']):
        words = get_beat_words(row)
        for i in range(len(words) - 1):
            pos1, word1 = words[i]
            pos2, word2 = words[i + 1]
            pairs.append((word1, word2, pos2, row_idx + 1, json_file))
    return pairs


if __name__ == '__main__':
    dataset_dir = 'dataset'
    all_pairs = []

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            pairs = analyze_2gram(json_path)
            all_pairs.extend(pairs)

    # Aggregate by 2-gram key
    result = defaultdict(lambda: {"count": 0, "occurrences": []})

    for word1, word2, beat_pos, row_no, filepath in all_pairs:
        key = f"{word1} | {word2}"
        result[key]["count"] += 1
        result[key]["occurrences"].append({
            "file": os.path.basename(filepath),
            "row": row_no,
            "beat": round(beat_pos, 3)
        })

    sorted_result = dict(sorted(result.items(), key=lambda x: -x[1]["count"]))

    output_path = "transition_2gram.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_result, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}, total 2-grams: {len(sorted_result)}")
