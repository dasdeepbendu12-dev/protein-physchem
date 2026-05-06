"""
protparam_offline
=================

Offline, ProtParam-style physicochemical analysis of protein sequences.

Public API
----------
ProteinAnalyzer
    Per-sequence analyzer with all metrics.
analyze_dataframe
    Apply the analyzer to every row of a pandas DataFrame.
read_input_file, write_excel_output
    Format-agnostic file I/O (CSV, TSV, Excel, FASTA in; Excel out).
run
    Top-level pipeline used by both the CLI and library callers.
"""

from .analysis import (
    ProteinAnalyzer,
    clean_sequence,
    aliphatic_index,
    scale_average,
    net_charge_at_pH,
    amino_acid_composition_percent,
)
from .io_handler import (
    read_input_file,
    write_excel_output,
    detect_sequence_column,
    detect_id_column,
    analyze_dataframe,
)
from .cli import run, main

__version__ = "0.1.0"
__all__ = [
    "ProteinAnalyzer",
    "clean_sequence",
    "aliphatic_index",
    "scale_average",
    "net_charge_at_pH",
    "amino_acid_composition_percent",
    "read_input_file",
    "write_excel_output",
    "detect_sequence_column",
    "detect_id_column",
    "analyze_dataframe",
    "run",
    "main",
]
