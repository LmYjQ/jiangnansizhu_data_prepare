import json
import os
from collections import defaultdict

def analyze_patterns(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_patterns = defaultdict(list)  # pattern -> list of (file, row, beat, pattern_no)

    for row_idx, row in enumerate(data['rows']):
        notes = row['notes']
        duration_cumulative = 0.0  # within current pattern, resets to 0 when reaching 1.0
        pattern_no = 0  # cumulative pattern count within the row
        pattern_notes = []
        beat_position = 0.0  # from start of row
        for note in notes:
            pattern_notes.append(note['value'])
            duration_cumulative += note['duration']

            beat_position += note['duration']

            # When accumulated reaches 1, record this pattern
            if abs(duration_cumulative % 1.0) < 0.001:
                pattern_no += 1
                pattern_key = ' '.join(pattern_notes)
                print((pattern_key, json_file, row_idx + 1, beat_position, pattern_no))
                all_patterns[pattern_key].append((json_file, row_idx + 1, beat_position, pattern_no))
                # Reset for next pattern
                duration_cumulative = 0.0
                pattern_notes = []


        # Handle leftover (partial beat at end)
        if pattern_notes:
            pattern_key = ' '.join(pattern_notes) + ' [partial]'
            all_patterns[pattern_key].append((json_file, row_idx + 1, beat_position, pattern_no + 1))

    return all_patterns

def extract_digit(note):
    """Extract the first digit 1-7 from a note value."""
    for char in note:
        if char.isdigit() and '1' <= char <= '7':
            return char
    return None

def generate_json(all_patterns):
    result = {}

    for pattern, locations in all_patterns.items():
        notes = pattern.split()

        first = None
        second = None
        for note in notes:
            digit = extract_digit(note)
            if digit and '1' <= digit <= '7':
                if first is None:
                    first = digit
                elif second is None:
                    second = digit
                    break

        if not first or not second:
            continue

        if first not in result:
            result[first] = {}
        if second not in result[first]:
            result[first][second] = []

        for file, row, beat, pattern_no in locations:
            result[first][second].append({
                "pattern": pattern,
                "file": os.path.basename(file),
                "row": row,
                "beat": round(beat, 3)
            })

    return result

if __name__ == '__main__':
    dataset_dir = 'dataset'
    all_patterns = defaultdict(list)

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            patterns = analyze_patterns(json_path)
            for pattern, locations in patterns.items():
                all_patterns[pattern].extend(locations)

    json_output = generate_json(all_patterns)
    output_path = os.path.join(dataset_dir, f"transition_pattern.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}")