# protparam_offline

Offline, **ProtParam-style** physicochemical analysis of protein sequences.

Computes molecular weight, theoretical pI, instability index, GRAVY,
aromaticity, aliphatic index, Boman index, Wimley–White, Eisenberg and
Hopp–Woods scales, net charge at a chosen pH, and extinction coefficients —
**without making any network requests**.

Input  : `.csv`, `.tsv`/`.txt`, `.xlsx`/`.xls`, or `.fasta`
Output : multi-sheet Excel workbook (`.xlsx`)

---

## Installation

From the package directory:

```bash
pip install .
```

Or install the dependencies only and run the package as a module:

```bash
pip install -r requirements.txt
python -m protparam_offline
```

## Quick start (interactive)

Just run it — it will ask you for everything:

```bash
protparam-offline
```

Sample session:

```
================================================================
  protparam_offline — local ProtParam-style protein analysis
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

## Non-interactive / scripted use

```bash
protparam-offline -i candidates.csv -o results.xlsx -s sequence --ph 7.4 --non-interactive
```

## As a library

```python
from protparam_offline import ProteinAnalyzer, run

# 1) one sequence at a time
pa = ProteinAnalyzer("MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQ", protein_id="demo")
print(pa.summary())

# 2) full pipeline
run(input_path="candidates.csv",
    output_path="results.xlsx",
    sequence_column="sequence",
    pH=7.4,
    interactive=False)
```

## Output workbook

| Sheet              | Contents                                    |
|--------------------|---------------------------------------------|
| Original_Data      | Your input, untouched                       |
| Calculated_Results | One row per sequence with all metrics       |
| Summary            | Mean/min/max/std of each numeric metric     |
| Warnings           | Skipped or problematic rows (if any)        |

## Metrics computed

- Length, Molecular Weight (Da)
- Theoretical pI, Net charge at chosen pH
- Instability Index + Stable/Unstable classification
- Aliphatic Index (Ikai 1980)
- GRAVY (Kyte–Doolittle) + hydrophilic/hydrophobic class
- Aromaticity (mole fraction of F+W+Y)
- Boman Index (Radzicka & Wolfenden 1988)
- Wimley–White interfacial hydrophobicity (1996)
- Eisenberg consensus hydrophobicity (1984)
- Hopp–Woods hydrophilicity (1981)
- Extinction coefficient at 280 nm (reduced and with disulfides)

## License

MIT
