# -*- coding: utf-8 -*-
import argparse
from pathlib import Path
import pandas as pd


def process_mutations(input_file: Path, output_file: Path):
    """Load mutation summary, find the best mutation per position based on binding DeltaDeltaG, and export."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Load dataset
    if input_file.suffix.lower() == ".xlsx":
        df = pd.read_excel(input_file)
    elif input_file.suffix.lower() in [".csv", ".txt"]:
        df = pd.read_csv(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file.suffix}")

    # Validate required columns
    required_cols = {"Position", "Mutation", "DeltaDeltaG_binding", "DeltaG_binding", "DeltaG_mutation"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    # Extract numerical position safely
    df["Position"] = df["Position"].astype(str).str.extract(r"(\d+)").astype(int)

    # Select mutation with minimum DeltaDeltaG_binding per position
    best_mutants = df.loc[df.groupby("Position")["DeltaDeltaG_binding"].idxmin()].copy()

    # Sort by position
    best_mutants = best_mutants.sort_values(by="Position")

    # Filter key columns
    best_mutants = best_mutants[["Position", "Mutation", "DeltaG_binding", "DeltaDeltaG_binding", "DeltaG_mutation"]]

    # Save results
    if output_file.suffix.lower() == ".xlsx":
        best_mutants.to_excel(output_file, index=False, engine="openpyxl")
    else:
        best_mutants.to_csv(output_file, index=False)

    print(f"File created successfully: {output_file.resolve()}\n")
    print(best_mutants.to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter and select best mutations per position from screening summary data.")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="all_positions_summary.xlsx",
        type=Path,
        help="Path to the input summary file (default: all_positions_summary.xlsx)."
    .strip()
    )
    parser.add_argument(
        "-o", "--output",
        default="best_mutations_from_all.xlsx",
        type=Path,
        help="Path for the output filtered Excel file (default: best_mutations_from_all.xlsx)."
    )
    args = parser.parse_args()
    
    process_mutations(args.input_file, args.output)
