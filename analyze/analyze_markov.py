import json
import os
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


def extract_pitch(note, mode='full'):
    """Extract pitch from a note.
    mode='full': returns (value, octave) tuple
    mode='value': returns just value string
    """
    if mode == 'full':
        return (note['value'], note['octave'])
    else:
        return note['value']


def analyze_note_2gram(json_file, mode='full'):
    """Return list of (prev_pitch, next_pitch, file, prev_note, next_note) for each consecutive note pair."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pairs = []
    notes = data['notes']
    prev_pitch = None
    prev_note = None

    for note in notes:
        if note['value'] == 'bar':
            continue
        pitch = extract_pitch(note, mode)

        if prev_pitch is not None:
            pairs.append((prev_pitch, pitch, json_file, prev_note, note))
        prev_pitch = pitch
        prev_note = note

    return pairs


if __name__ == '__main__':
    # Parse mode from command line argument
    mode = 'full'
    if len(sys.argv) > 1:
        if sys.argv[1] == 'value':
            mode = 'value'
    print(f"Running in mode: {mode}")

    dataset_dir = 'D:/code/music/qmx_reader/dataset_da'
    all_pairs = []

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json') and filename != 'transition_pattern.json':
            json_path = os.path.join(dataset_dir, filename)
            print(f"Analyzing: {filename}")
            pairs = analyze_note_2gram(json_path, mode)
            all_pairs.extend(pairs)

    # Build Markov transition count matrix with (value, octave) as pitch keys
    count_matrix = defaultdict(lambda: defaultdict(int))
    occurrences = defaultdict(list)

    for prev, nxt, filepath, prev_note, next_note in all_pairs:
        count_matrix[prev][nxt] += 1
        occurrences[(prev, nxt)].append({
            "file": os.path.basename(filepath),
            "prev_note": prev_note,
            "next_note": next_note
        })

    # Get all unique pitches
    all_pitches = set()
    for prev in count_matrix:
        all_pitches.add(prev)
        for nxt in count_matrix[prev]:
            all_pitches.add(nxt)
    pitches = sorted(all_pitches, key=lambda x: (x[0], x[1]) if isinstance(x, tuple) else (x, ''))

    # Compute probability matrix
    prob_dict = {}
    total = defaultdict(int)
    for prev in pitches:
        total[prev] = sum(count_matrix[prev][nxt] for nxt in count_matrix[prev])

    for prev in pitches:
        prob_dict[prev] = {}
        for nxt in pitches:
            prob_dict[prev][nxt] = count_matrix[prev][nxt] / total[prev] if total[prev] > 0 else 0.0

    def pitch_label(p):
        return f"{p[0]}_{p[1]}" if isinstance(p, tuple) else str(p)

    json_output = {
        "mode": mode,
        "pitches": pitches,
        "count": {str(p): {str(q): count_matrix[p][q] for q in pitches} for p in pitches},
        "prob": {str(p): {str(q): prob_dict[p][q] for q in pitches} for p in pitches},
        "occurrences": {f"{pitch_label(p)}|{pitch_label(q)}": occurrences[(p, q)] for p in pitches for q in pitches if count_matrix[p][q] > 0}
    }
    output_path = f"transition_prob_{mode}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_path}")

    prob_matrix = np.array([[prob_dict[p][q] for q in pitches] for p in pitches[::-1]])

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(prob_matrix, cmap='YlOrRd', aspect='auto', vmin=0.0, vmax=1.0)
    ax.set_xticks(range(len(pitches)))
    ax.set_yticks(range(len(pitches)))
    ax.set_xticklabels([pitch_label(p) for p in pitches])
    ax.set_yticklabels([pitch_label(p) for p in pitches[::-1]])
    ax.set_xlabel('Next Pitch')
    ax.set_ylabel('Current Pitch')
    ax.set_title(f'Markov Pitch Transition Probability Matrix (mode={mode})')

    for i in range(len(pitches)):
        for j in range(len(pitches)):
            val = prob_matrix[i, j]
            color = 'white' if val > 0.5 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=8)

    plt.colorbar(im, ax=ax, label='Probability')
    plt.tight_layout()
    plt.savefig(f"transition_prob_{mode}.png", dpi=150)
    print(f"Output: transition_prob_{mode}.png")
