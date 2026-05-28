import json
import os
from collections import defaultdict

def note_to_key(note):
    """Convert note to a string key based on value + octave + duration."""
    return f"{note['value']}_{note['octave']}_{note['duration']}"


def get_beat_patterns(notes):
    """Return list of (beat_position, list_of_note_keys) for each beat."""
    words = []
    duration_cumulative = 0.0
    beat_notes = []
    beat_position = 0.0

    for note in notes:
        if note['value'] == 'bar':
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


def analyze_patterns(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_patterns = defaultdict(list)
    notes = data['notes']
    duration_cumulative = 0.0
    beat_position = 0.0
    pattern_notes = []

    for note in notes:
        if note['value'] == 'bar':
            continue
        pattern_notes.append(note)
        duration_cumulative += note['duration']
        beat_position += note['duration']

        if abs(duration_cumulative % 1.0) < 0.001:
            pattern_key = '|'.join(note_to_key(n) for n in pattern_notes)
            all_patterns[pattern_key].append({
                "file": os.path.basename(json_file),
                "beat": round(beat_position, 3),
                "notes": pattern_notes
            })
            duration_cumulative = 0.0
            pattern_notes = []

    if pattern_notes:
        pattern_key = '|'.join(note_to_key(n) for n in pattern_notes) + '|[partial]'
        all_patterns[pattern_key].append({
            "file": os.path.basename(json_file),
            "beat": round(beat_position, 3),
            "notes": pattern_notes
        })

    return all_patterns


def generate_json(all_patterns):
    result = {}
    for pattern_key, locations in all_patterns.items():
        result[pattern_key] = {
            "count": len(locations),
            "occurrences": locations
        }
    return result

if __name__ == '__main__':
    dataset_dir = 'D:/code/music/qmx_reader/dataset_da'
    all_patterns = defaultdict(list)

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            patterns = analyze_patterns(json_path)
            for pattern, locations in patterns.items():
                all_patterns[pattern].extend(locations)

    json_output = generate_json(all_patterns)
    output_path = f"transition_pattern_agg.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}, total patterns: {len(json_output)}")