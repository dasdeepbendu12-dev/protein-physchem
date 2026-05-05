"""
Example: programmatic use of protparam_offline.

Run from the package root after installing the dependencies:
    python examples/example_usage.py
"""

from protparam_offline import ProteinAnalyzer, analyze_dataframe
import pandas as pd

# ---- single-sequence analysis ----
pa = ProteinAnalyzer(
    "MKWVTFISLLLLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPF",
    protein_id="BSA_fragment",
)
print("Single-sequence summary:")
for k, v in pa.summary(pH=7.4).items():
    print(f"  {k:35s} {v}")

# ---- batch analysis from a DataFrame ----
df = pd.DataFrame({
    "rank": [1, 2, 3],
    "sequence": [
        "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQ",
        "GIGAVLKVLTTGLPALISWIKRKRQQ",          # Melittin (cationic AMP)
        "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPD",
    ],
})

results, warnings = analyze_dataframe(df, sequence_column="sequence", pH=7.0)
print("\nBatch results:")
print(results)
if warnings:
    print("\nWarnings:")
    for w in warnings:
        print(" -", w)
