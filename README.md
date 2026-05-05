# protein-physchem

> **Offline, batch physicochemical characterization of protein sequences.** A local Python alternative to the ExPASy ProtParam web tool, designed for high-throughput screening workflows.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built on Biopython](https://img.shields.io/badge/built%20on-Biopython-green.svg)](https://biopython.org/)

Author: Deepbendu Das GitHub: @dasdeepbendu12-dev

`protein-physchem` computes the full ExPASy ProtParam metric set — molecular weight, theoretical pI, instability index, aliphatic index, GRAVY, aromaticity, extinction coefficient — alongside additional scale-based indices (Boman, Wimley–White, Eisenberg, Hopp–Woods) and net charge at any user-specified pH. Hand it a CSV, TSV, Excel, or FASTA file and get back a multi-sheet Excel report. No internet access, no rate limits.

---

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Command-line usage](#command-line-usage)
- [Library API](#library-api)
- [Input formats](#input-formats)
- [Output workbook](#output-workbook)
- [Metrics computed](#metrics-computed)
- [Project structure](#project-structure)
- [Citations](#citations)
- [License](#license)

---

## Features

- 🧬 **15+ physicochemical metrics** per sequence, including hydrophobicity scales not in standard ProtParam
- 📂 **Format-agnostic input** — CSV, TSV, Excel (`.xlsx`/`.xls`), or FASTA
- 📊 **Annotated Excel output** — original data, calculated results, descriptive statistics, and a warnings log on separate sheets
- 🖥️ **Interactive CLI** — prompts for the input file, sequence column, and output name, with sensible defaults
- ⚙️ **Scriptable** — full `argparse` interface for batch jobs and pipelines
- 📦 **Library API** — drop into Jupyter notebooks or larger Python projects
- 🔌 **Fully offline** — no web requests, no API keys, no rate limits
- 🧪 **Robust input handling** — auto-detects sequence column, strips ambiguous residues (X, B, Z, U, O), gaps, and whitespace
- ⚖️ **Net charge at any pH** — useful for buffer design and AMP screening

## Installation

### From source (recommended for now)

```bash
git clone https://github.com/<your-username>/protein-physchem.git
cd protein-physchem
pip install .
```

This registers the `protein-physchem` console command on your `PATH`.

### Without installing the package

Just install the dependencies and run as a module:

```bash
pip install -r requirements.txt
python -m protein_physchem
```

### Requirements

- Python ≥ 3.8
- `biopython` ≥ 1.79
- `pandas` ≥ 1.3
- `openpyxl` ≥ 3.0

## Quick start

The fastest way is to just run it — the tool will ask you for everything it needs:

```bash
protein-physchem
```

Sample session:

```text
================================================================
  protein-physchem — local physicochemical analysis of proteins
================================================================

The input may be CSV, TSV, Excel (.xlsx/.xls) or FASTA.
Current working directory: /home/you/work
Enter input file name (if in this folder) or full path: candidates.csv

📂 Reading: /home/you/work/candidates.csv
   Loaded 42 rows × 3 columns.

Columns found in input:
  [1] rank
  [2] sequence
  [3] notes
Which column holds the protein sequences? (number or name) [sequence]:

Enter output Excel file name [candidates_protparam.xlsx]:

🔬 Analyzing sequences ...
   Successful: 42 / 42

✅ Done. Results written to:
   /home/you/work/candidates_protparam.xlsx
```

## Command-line usage

For scripted / pipeline use, pass everything as flags and skip the prompts:

```bash
protein-physchem -i candidates.csv -o results.xlsx -s sequence --ph 7.4 --non-interactive
```

| Flag | Description |
|------|-------------|
| `-i`, `--input` | Input file (CSV / TSV / Excel / FASTA) |
| `-o`, `--output` | Output `.xlsx` file (default: `<input>_protparam.xlsx`) |
| `-s`, `--seq-col` | Column name holding sequences (auto-detected if omitted) |
| `--id-col` | Column name holding identifiers (auto-detected if omitted) |
| `--ph` | pH at which to compute net charge (default: `7.0`) |
| `--non-interactive` | Skip all prompts (requires `--input`) |

## Library API

```python
from protein_physchem import ProteinAnalyzer, analyze_dataframe, run
import pandas as pd

# 1) one sequence at a time
pa = ProteinAnalyzer(
    "MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPF",
    protein_id="BSA_fragment",
)
print(pa.summary(pH=7.4))

# 2) batch on a DataFrame you already have in memory
df = pd.DataFrame({
    "rank": [1, 2, 3],
    "sequence": [
        "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQ",
        "GIGAVLKVLTTGLPALISWIKRKRQQ",        # Melittin
        "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPD",
    ],
})
results, warnings = analyze_dataframe(df, sequence_column="sequence", pH=7.0)

# 3) full pipeline (file → analysis → Excel) without the CLI
run(input_path="candidates.csv",
    output_path="results.xlsx",
    sequence_column="sequence",
    pH=7.4,
    interactive=False)
```

### Per-metric access

If you want individual values rather than the full summary dict:

```python
pa = ProteinAnalyzer("MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQ")

pa.length                          # 33
pa.molecular_weight()              # Da
pa.isoelectric_point()             # theoretical pI
pa.instability_index()             # ProtParam II
pa.gravy()                         # Kyte-Doolittle GRAVY
pa.aromaticity()                   # mole fraction F+W+Y
pa.aliphatic_index()               # Ikai 1980
pa.boman_index()                   # Radzicka & Wolfenden 1988
pa.wimley_white_hydrophobicity()   # Wimley & White 1996
pa.eisenberg_hydrophobicity()      # Eisenberg 1984
pa.hopp_woods_hydrophilicity()     # Hopp & Woods 1981
pa.net_charge(pH=7.4)              # Henderson-Hasselbalch
pa.extinction_coefficient()        # (reduced, with disulfides) at 280 nm
```

## Input formats

| Extension | Format | Notes |
|-----------|--------|-------|
| `.csv` | Comma-separated | `pandas.read_csv` defaults |
| `.tsv`, `.txt` | Tab-separated | |
| `.xlsx`, `.xls` | Excel | First sheet by default |
| `.fasta`, `.fa`, `.faa`, `.fas` | FASTA | Parsed via `Bio.SeqIO` |

The tool auto-detects which column holds sequences by looking for common names (`sequence`, `seq`, `peptide`, `protein_sequence`, etc.) — you can override this with `-s` or pick from a numbered menu in interactive mode.

## Output workbook

Every run produces a single `.xlsx` file with these sheets:

| Sheet | Contents |
|-------|----------|
| `Original_Data` | Your input file, untouched |
| `Calculated_Results` | One row per sequence with all 15+ metrics |
| `Summary` | Mean / std / min / max / quartiles for every numeric metric |
| `Warnings` | Any rows that were skipped or had problems (only present if needed) |

Headers are bolded, columns are auto-sized, and the file is ready to share or open in Excel / LibreOffice / Google Sheets.

## Metrics computed

| Metric | Units | Reference |
|--------|-------|-----------|
| Length | residues | — |
| Molecular Weight | Da | average isotopic |
| Theoretical pI | — | EMBOSS pKa values |
| Net Charge at pH | e | Henderson–Hasselbalch |
| Instability Index | — | Guruprasad et al. 1990 |
| Stability class | Stable / Unstable | II ≤ 40 → Stable |
| Aliphatic Index | — | Ikai 1980 |
| GRAVY | — | Kyte & Doolittle 1982 |
| GRAVY class | Hydrophobic / Hydrophilic / Neutral | sign of GRAVY |
| Aromaticity | mole fraction | Lobry & Gautier 1994 |
| Boman Index | kcal/mol | Radzicka & Wolfenden 1988 |
| Wimley–White hydrophobicity | kcal/mol | Wimley & White 1996 |
| Eisenberg hydrophobicity | — | Eisenberg et al. 1984 |
| Hopp–Woods hydrophilicity | — | Hopp & Woods 1981 |
| Extinction coefficient (280 nm) | M⁻¹·cm⁻¹ | reduced and disulfide forms |

## Project structure

```
protein-physchem/
├── pyproject.toml              # pip-installable; registers the CLI command
├── setup.py                    # legacy fallback
├── requirements.txt
├── README.md
├── LICENSE
├── examples/
│   └── example_usage.py
└── protein_physchem/
    ├── __init__.py             # public API
    ├── __main__.py             # `python -m protein_physchem`
    ├── scales.py               # amino acid scales (Boman, Kyte-Doolittle, …)
    ├── analysis.py             # ProteinAnalyzer class
    ├── io_handler.py           # CSV/TSV/Excel/FASTA reading + Excel writing
    └── cli.py                  # interactive prompts + argparse
```

## Citations

If `protein-physchem` is useful in your work, please cite the underlying methods:

- **Biopython** — Cock PJA *et al.* (2009) *Bioinformatics* **25**(11): 1422–1423.
- **ProtParam / ExPASy** — Gasteiger E *et al.* (2005). In: *The Proteomics Protocols Handbook.*
- **Instability Index** — Guruprasad K, Reddy BVB, Pandit MW (1990) *Protein Eng.* **4**(2): 155–161.
- **Aliphatic Index** — Ikai A (1980) *J. Biochem.* **88**(6): 1895–1898.
- **GRAVY / Kyte–Doolittle** — Kyte J, Doolittle RF (1982) *J. Mol. Biol.* **157**(1): 105–132.
- **Boman Index** — Radzicka A, Wolfenden R (1988) *Biochemistry* **27**(5): 1664–1670.
- **Wimley–White scale** — Wimley WC, White SH (1996) *Nat. Struct. Biol.* **3**(10): 842–848.
- **Eisenberg consensus scale** — Eisenberg D *et al.* (1984) *J. Mol. Biol.* **179**(1): 125–142.
- **Hopp–Woods scale** — Hopp TP, Woods KR (1981) *Proc. Natl. Acad. Sci. USA* **78**(6): 3824–3828.

## Contributing

Issues and pull requests are welcome. For bug reports, please include:

1. Your Python version and OS
2. A minimal example input file
3. The full error output

## License

Copyright (c) 2026 STLAB at Indian Institute of Chemical Biology

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

