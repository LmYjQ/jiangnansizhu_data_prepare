import json
import os
import sys
from collections import defaultdict


def note_to_key(note):
    """Convert note to a string key based on value + octave + duration."""
    return f"{note['value']}_{note['octave']}_{note['duration']}"


def get_beat_words(notes):
    """Return list of (beat_position, list_of_note_keys) for each beat."""
    words = []
    duration_cumulative = 0.0
    beat_notes = []
    beat_position = 0.0

    for note in notes:
        if note['value'] in ['bar', 'space']:
            continue
        beat_notes.append(note_to_key(note))
        duration_cumulative += note['duration']
        beat_position += note['duration']

        if abs(duration_cumulative % 1.0) < 0.001:
            words.append((beat_position, beat_notes))
            duration_cumulative = 0.0
            beat_notes = []

    if beat_notes:
        words.append((beat_position, beat_notes))

    return words


def analyze_ngram(json_file, n=2):
    """Return list of (ngram_tuple, end_position, notes_list) for each n-gram in the file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    notes = data['notes']
    ngrams = []
    words = get_beat_words(notes)

    for i in range(len(words) - n + 1):
        # Each beat's notes joined into a string
        beat_strs = tuple(' '.join(words[i + j][1]) for j in range(n))
        end_pos = words[i + n - 1][0]
        # Collect all notes in this ngram
        ngram_notes = []
        for j in range(n):
            ngram_notes.extend(words[i + j][1])
        ngrams.append((beat_strs, end_pos, json_file, ngram_notes))

    return ngrams


if __name__ == '__main__':
    N = 5

    if len(sys.argv) > 1:
        dataset_dir = sys.argv[1]
    else:
        dataset_dir = 'D:/code/music/qmx_reader/dataset_final8'
    suffix = os.path.basename(dataset_dir)
    all_ngrams = []

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            ngrams = analyze_ngram(json_path, n=N)
            all_ngrams.extend(ngrams)

    result = defaultdict(lambda: {"count": 0, "occurrences": []})

    for beat_strs, beat_pos, filepath, ngram_notes in all_ngrams:
        key = " | ".join(beat_strs)
        result[key]["count"] += 1
        result[key]["occurrences"].append({
            "file": os.path.basename(filepath),
            "beat": round(beat_pos, 3),
            "notes": ngram_notes
        })

    sorted_result = {k: v for k, v in sorted(result.items(), key=lambda x: -x[1]["count"]) if v["count"] > 1}

    output_path = f"transition_{N}gram_{suffix}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_result, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}, total {N}-grams: {len(sorted_result)}")
