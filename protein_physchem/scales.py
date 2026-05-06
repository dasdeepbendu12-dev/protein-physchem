"""
Amino acid scales used for physicochemical property calculations.

All scales are stored as plain dictionaries so the package has no
dependency on any online resource.
"""

# Boman Index scale (Radzicka & Wolfenden, 1988)
# Sum of the free energies of transfer from water to cyclohexane.
BOMAN_SCALE = {
    'A': -1.81, 'R':  9.15, 'N':  6.64, 'D':  7.46, 'C': -1.28,
    'Q':  5.54, 'E':  7.00, 'G': -0.94, 'H':  4.66, 'I': -4.92,
    'L': -4.92, 'K':  5.55, 'M': -2.35, 'F': -2.98, 'P':  0.00,
    'S':  3.40, 'T':  2.50, 'W': -2.33, 'Y':  0.14, 'V': -4.04,
}

# Wimley-White whole residue interfacial hydrophobicity scale (1996)
WIMLEY_WHITE_SCALE = {
    'A':  0.17, 'R':  0.81, 'N':  0.42, 'D':  1.23, 'C': -0.24,
    'Q':  0.58, 'E':  2.02, 'G':  0.01, 'H':  0.96, 'I': -0.31,
    'L': -0.56, 'K':  0.99, 'M': -0.23, 'F': -1.13, 'P':  0.45,
    'S':  0.13, 'T':  0.14, 'W': -2.09, 'Y': -0.71, 'V':  0.07,
}

# Kyte-Doolittle hydropathy scale (1982) — used for GRAVY calculation
KYTE_DOOLITTLE_SCALE = {
    'A':  1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C':  2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I':  4.5,
    'L':  3.8, 'K': -3.9, 'M':  1.9, 'F':  2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V':  4.2,
}

# Eisenberg consensus hydrophobicity scale (1984)
EISENBERG_SCALE = {
    'A':  0.62, 'R': -2.53, 'N': -0.78, 'D': -0.90, 'C':  0.29,
    'Q': -0.85, 'E': -0.74, 'G':  0.48, 'H': -0.40, 'I':  1.38,
    'L':  1.06, 'K': -1.50, 'M':  0.64, 'F':  1.19, 'P':  0.12,
    'S': -0.18, 'T': -0.05, 'W':  0.81, 'Y':  0.26, 'V':  1.08,
}

# Hopp-Woods hydrophilicity scale (1981) — used for antigenicity prediction
HOPP_WOODS_SCALE = {
    'A': -0.5, 'R':  3.0, 'N':  0.2, 'D':  3.0, 'C': -1.0,
    'Q':  0.2, 'E':  3.0, 'G':  0.0, 'H': -0.5, 'I': -1.8,
    'L': -1.8, 'K':  3.0, 'M': -1.3, 'F': -2.5, 'P':  0.0,
    'S':  0.3, 'T': -0.4, 'W': -3.4, 'Y': -2.3, 'V': -1.5,
}

# Standard one-letter amino acid alphabet
STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")

# Ambiguous / non-standard residues that ProtParam-style calculations cannot use
AMBIGUOUS_AA = set("XBZUO*")
