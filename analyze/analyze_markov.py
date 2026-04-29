import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


def extract_pitch(note_value):
    """Extract the first digit 0-7 from a note value as pitch."""
    for char in note_value:
        if '0' <= char <= '7':
            return char
    return None


def analyze_note_2gram(json_file):
    """Return list of (prev_pitch, next_pitch, row_idx) for each consecutive note pair."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pairs = []
    for row_idx, row in enumerate(data['rows']):
        prev_pitch = None
        for note in row['notes']:
            if note['value'] == 'bar':
                continue
            if 'token_dict' in note:
                pitch = extract_pitch(note['token_dict']['main_value'])
            else:
                pitch = extract_pitch(note['value'])

            if pitch is None:
                continue

            if prev_pitch is not None:
                pairs.append((prev_pitch, pitch, row_idx + 1, json_file))
            prev_pitch = pitch

    return pairs


if __name__ == '__main__':
    dataset_dir = 'dataset'
    all_pairs = []

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            pairs = analyze_note_2gram(json_path)
            all_pairs.extend(pairs)

    # Build Markov transition count matrix (pitches 0-7)
    pitches = [str(i) for i in range(8)]
    count_matrix = defaultdict(lambda: defaultdict(int))

    for prev, nxt, _, _ in all_pairs:
        count_matrix[prev][nxt] += 1

    # Convert to regular dict and compute probability matrix
    count_dict = {p: {q: count_matrix[p][q] for q in pitches} for p in pitches}
    total = defaultdict(int)
    for prev in pitches:
        for nxt in pitches:
            total[prev] += count_matrix[prev][nxt]

    prob_dict = {}
    for prev in pitches:
        prob_dict[prev] = {}
        for nxt in pitches:
            if total[prev] > 0:
                prob_dict[prev][nxt] = count_matrix[prev][nxt] / total[prev]
            else:
                prob_dict[prev][nxt] = 0.0

    # --- Numeric output ---
    json_output = {
        "pitches": pitches,
        "count": count_dict,
        "prob": prob_dict
    }
    output_path = "transition_prob.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}")

    # --- Heatmap image ---
    # Flip matrix vertically so pitch 0 is at bottom, 7 at top
    prob_matrix = np.array([[prob_dict[p][q] for q in pitches] for p in pitches[::-1]])

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(prob_matrix, cmap='YlOrRd', aspect='auto', vmin=0.0, vmax=1.0)
    ax.set_xticks(range(len(pitches)))
    ax.set_yticks(range(len(pitches)))
    ax.set_xticklabels(pitches)
    ax.set_yticklabels(pitches[::-1])
    ax.set_xlabel('Next Pitch')
    ax.set_ylabel('Current Pitch')
    ax.set_title('Markov Pitch Transition Probability Matrix')

    # Add text annotations
    for i in range(len(pitches)):
        for j in range(len(pitches)):
            val = prob_matrix[i, j]
            color = 'white' if val > 0.5 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=9)

    plt.colorbar(im, ax=ax, label='Probability')
    plt.tight_layout()
    plt.savefig("transition_prob.png", dpi=150)
    print("Output: transition_prob.png")
