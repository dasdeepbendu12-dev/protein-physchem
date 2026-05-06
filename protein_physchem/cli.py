"""
Interactive command-line interface for protparam_offline.

Run with:
    python -m protparam_offline
or, after installation:
    protparam-offline
"""

from __future__ import annotations
import os
import sys
import argparse
from typing import Optional

from .io_handler import (
    read_input_file,
    detect_sequence_column,
    detect_id_column,
    analyze_dataframe,
    write_excel_output,
)


# ---------- pretty printing helpers -----------------------------------

def _print_banner() -> None:
    print("=" * 64)
    print("  protparam_offline — local ProtParam-style protein analysis")
    print("=" * 64)


def _ask(prompt: str, default: Optional[str] = None) -> str:
    """Prompt the user; return stripped input or `default` if input was empty."""
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("  ↳ A value is required, please try again.")


def _resolve_input_path(user_input: str) -> str:
    """
    Try to resolve a file the user typed:
      1. Exact path (absolute or relative to CWD).
      2. Same name in CWD.
      3. With common extensions appended.
    """
    if os.path.isfile(user_input):
        return os.path.abspath(user_input)

    cwd_candidate = os.path.join(os.getcwd(), user_input)
    if os.path.isfile(cwd_candidate):
        return cwd_candidate

    base, ext = os.path.splitext(user_input)
    if not ext:
        for try_ext in (".csv", ".tsv", ".txt", ".xlsx", ".xls", ".fasta", ".fa"):
            candidate = os.path.join(os.getcwd(), user_input + try_ext)
            if os.path.isfile(candidate):
                return candidate

    raise FileNotFoundError(user_input)


def _prompt_input_file() -> str:
    """Loop until the user gives us a real, existing file path."""
    print("\nThe input may be CSV, TSV, Excel (.xlsx/.xls) or FASTA.")
    print(f"Current working directory: {os.getcwd()}")
    while True:
        raw = _ask("Enter input file name (if in this folder) or full path")
        try:
            return _resolve_input_path(os.path.expanduser(raw))
        except FileNotFoundError:
            print(f"  ⚠️  Could not find '{raw}'. Try again or press Ctrl+C to quit.")


def _prompt_output_file(input_path: str) -> str:
    """Ask for output file name; default = <input_basename>_protparam.xlsx in CWD."""
    base = os.path.splitext(os.path.basename(input_path))[0]
    default_name = f"{base}_protparam.xlsx"
    name = _ask("Enter output Excel file name", default=default_name)
    if not name.lower().endswith(".xlsx"):
        name += ".xlsx"
    # If the user typed only a name, drop it in CWD
    if not os.path.dirname(name):
        name = os.path.join(os.getcwd(), name)
    return name


def _prompt_sequence_column(columns: list, autodetected: Optional[str]) -> str:
    print("\nColumns found in input:")
    for i, c in enumerate(columns, 1):
        print(f"  [{i}] {c}")
    if autodetected:
        choice = _ask(
            f"Which column holds the protein sequences? (number or name)",
            default=autodetected,
        )
    else:
        choice = _ask("Which column holds the protein sequences? (number or name)")

    if choice.isdigit() and 1 <= int(choice) <= len(columns):
        return columns[int(choice) - 1]
    if choice in columns:
        return choice
    # Case-insensitive match
    for c in columns:
        if c.lower() == choice.lower():
            return c
    raise ValueError(f"Column '{choice}' not found among {columns}")


# ---------- main routine ----------------------------------------------

def run(
    input_path: Optional[str] = None,
    output_path: Optional[str] = None,
    sequence_column: Optional[str] = None,
    id_column: Optional[str] = None,
    pH: float = 7.0,
    interactive: bool = True,
) -> str:
    """
    Programmatic entry point. Returns the path of the Excel file written.
    """
    _print_banner()

    # --- input file
    if input_path is None:
        if not interactive:
            raise ValueError("input_path is required in non-interactive mode")
        input_path = _prompt_input_file()
    else:
        input_path = os.path.abspath(os.path.expanduser(input_path))
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"\n📂 Reading: {input_path}")
    df = read_input_file(input_path)
    print(f"   Loaded {len(df)} rows × {len(df.columns)} columns.")

    # --- sequence column
    auto_seq = detect_sequence_column(df)
    if sequence_column is None:
        if auto_seq and not interactive:
            sequence_column = auto_seq
        elif interactive:
            sequence_column = _prompt_sequence_column(list(df.columns), auto_seq)
        else:
            raise ValueError("Could not auto-detect sequence column; pass sequence_column=...")
    print(f"   Sequence column: '{sequence_column}'")

    # --- ID column (optional)
    if id_column is None:
        id_column = detect_id_column(df)
        if id_column:
            print(f"   ID column     : '{id_column}'")

    # --- output path
    if output_path is None:
        if interactive:
            output_path = _prompt_output_file(input_path)
        else:
            base = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(os.getcwd(), f"{base}_protparam.xlsx")
    else:
        output_path = os.path.abspath(os.path.expanduser(output_path))
        if not output_path.lower().endswith(".xlsx"):
            output_path += ".xlsx"

    # --- analyze
    print("\n🔬 Analyzing sequences ...")
    results_df, warnings = analyze_dataframe(
        df, sequence_column=sequence_column, id_column=id_column, pH=pH,
    )
    print(f"   Successful: {len(results_df)} / {len(df)}")
    if warnings:
        print(f"   Warnings  : {len(warnings)} (see 'Warnings' sheet)")

    # --- write
    write_excel_output(output_path, df, results_df, warnings)
    print(f"\n✅ Done. Results written to:\n   {output_path}\n")
    return output_path


# ---------- argparse wrapper ------------------------------------------

def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="protparam-offline",
        description="Offline ProtParam-style protein analysis. "
                    "Run with no arguments for an interactive prompt.",
    )
    parser.add_argument("-i", "--input",  help="Input CSV/TSV/Excel/FASTA file.")
    parser.add_argument("-o", "--output", help="Output .xlsx file.")
    parser.add_argument("-s", "--seq-col", dest="sequence_column",
                        help="Name of the column holding sequences.")
    parser.add_argument("--id-col", dest="id_column",
                        help="Name of the column holding identifiers.")
    parser.add_argument("--ph", type=float, default=7.0,
                        help="pH at which to compute net charge (default: 7.0).")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Disable prompts; --input is then required.")
    args = parser.parse_args(argv)

    try:
        run(
            input_path=args.input,
            output_path=args.output,
            sequence_column=args.sequence_column,
            id_column=args.id_column,
            pH=args.ph,
            interactive=not args.non_interactive,
        )
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"\n❌ {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
