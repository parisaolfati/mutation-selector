# Mutation Selector

A clean Python utility to process mutation scanning summaries, extract numerical positions, filter the optimal mutation per position based on the lowest `DeltaDeltaG_binding`, and export a structured Excel report.

## Features

- Supports both Excel (`.xlsx`) and CSV input files.
- Robust regex extraction of numeric residue positions.
- Automatically groups by position and extracts the top mutation minimizing binding energy changes.
- Exports a clean, sorted summary report.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run with default filenames (`all_positions_summary.xlsx` -> `best_mutations_from_all.xlsx`):
```bash
python select_best_mutations.py
```

Or specify custom input and output paths:
```bash
python select_best_mutations.py custom_input.xlsx -o custom_output.xlsx
```
