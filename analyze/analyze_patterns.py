import json
import os
from collections import defaultdict

def analyze_patterns(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_patterns = defaultdict(list)  # pattern -> list of (file, row_index, pattern_no)

    for row_idx, row in enumerate(data['rows']):
        notes = row['notes']
        duration_cumulative = 0.0  # within current pattern, resets to 0 when reaching 1.0
        pattern_no = 0  # cumulative pattern count within the row
        pattern_notes = []

        for note in notes:
            pattern_notes.append(note['value'])
            duration_cumulative += note['duration']

            # When accumulated reaches 1, record this pattern
            if abs(duration_cumulative - 1.0) < 0.001:
                if duration_cumulative != 1.0:
                    print(f"WARNING: duration_cumulative={duration_cumulative}, diff={duration_cumulative - 1.0}, pattern={pattern_notes}")
                pattern_no += 1
                pattern_key = ' '.join(pattern_notes)
                all_patterns[pattern_key].append((json_file, row_idx + 1, pattern_no))
                # Reset for next pattern
                duration_cumulative = 0.0
                pattern_notes = []

        # Handle leftover (partial beat at end)
        if pattern_notes:
            pattern_key = ' '.join(pattern_notes) + ' [partial]'
            all_patterns[pattern_key].append((json_file, row_idx + 1, pattern_no + 1))

    return all_patterns

def generate_markdown(all_patterns, title):
    md = f"# Pattern Analysis: {title}\n\n"
    md += f"Total unique patterns: {len(all_patterns)}\n\n"

    # Sort by frequency
    sorted_patterns = sorted(all_patterns.items(), key=lambda x: -len(x[1]))

    md += "## Pattern Summary (sorted by frequency)\n\n"
    md += "| Pattern | Count | Locations (file, row, pattern_no) |\n"
    md += "|---------|-------|---------------------------|\n"

    for pattern, locations in sorted_patterns:
        loc_str = '; '.join([f"{f}({r},p{s})" for f,r,s in locations[:10]])  # Limit to first 10
        # if len(locations) > 10:
        #     loc_str += f" ... (+{len(locations)-10} more)"
        md += f"| `{pattern}` | {len(locations)} | {loc_str} |\n"

    # Detailed breakdown
    md += "\n## Detailed Locations\n\n"
    for pattern, locations in sorted_patterns:  # 全部
        md += f"### `{pattern}` ({len(locations)} occurrences)\n\n"
        md += "```\n"
        for file, row_idx, pattern_no in locations:
                md += f"{os.path.basename(file)} Row {row_idx}, pattern {pattern_no}\n"
        # if len(locations) > 20:
        #     md += f"... and {len(locations) - 20} more\n"
        md += "```\n\n"

    return md

if __name__ == '__main__':
    dataset_dir = 'dataset'
    all_patterns = defaultdict(list)

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            patterns = analyze_patterns(json_path)
            for pattern, locations in patterns.items():
                all_patterns[pattern].extend(locations)

    md = generate_markdown(all_patterns, "All Files")
    output_path = os.path.join(dataset_dir, f"all_patterns.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Output: {output_path}")