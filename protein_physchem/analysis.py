"""
Core protein analysis functions.

Provides a `ProteinAnalyzer` class that wraps Biopython's `ProteinAnalysis`
and adds several scale-based indices (Aliphatic, Boman, Wimley-White, etc.).

Everything runs locally — no network calls are made at any point.
"""

from __future__ import annotations
from typing import Dict, Optional

from Bio.SeqUtils.ProtParam import ProteinAnalysis

from .scales import (
    BOMAN_SCALE,
    WIMLEY_WHITE_SCALE,
    KYTE_DOOLITTLE_SCALE,
    EISENBERG_SCALE,
    HOPP_WOODS_SCALE,
    AMBIGUOUS_AA,
)


def clean_sequence(sequence: str) -> str:
    """Uppercase a sequence and strip ambiguous residues that break ProtParam."""
    if sequence is None:
        return ""
    seq = str(sequence).upper().strip()
    # Remove whitespace and gap characters first
    seq = "".join(seq.split())
    seq = seq.replace("-", "").replace(".", "").replace("*", "")
    # Strip ambiguous residues
    return "".join(aa for aa in seq if aa not in AMBIGUOUS_AA)


def aliphatic_index(sequence: str) -> float:
    """
    Aliphatic Index (Ikai, 1980).

    AI = 100 * (X_A + 2.9 * X_V + 3.9 * (X_I + X_L)) / length
    where X_aa is the count (not mole fraction) of that residue.
    """
    n = len(sequence)
    if n == 0:
        return 0.0
    a = sequence.count("A")
    v = sequence.count("V")
    i = sequence.count("I")
    l = sequence.count("L")
    return (100.0 / n) * (a + 2.9 * v + 3.9 * (i + l))


def scale_average(sequence: str, scale: Dict[str, float]) -> float:
    """Return the mean per-residue value of `sequence` under the given scale."""
    n = len(sequence)
    if n == 0:
        return 0.0
    return sum(scale.get(aa, 0.0) for aa in sequence) / n


def net_charge_at_pH(sequence: str, pH: float = 7.0) -> float:
    """
    Net charge of the protein at the given pH using Biopython's
    IsoelectricPoint helper (Henderson-Hasselbalch with EMBOSS pKa values).
    """
    if not sequence:
        return 0.0
    from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint
    return IsoelectricPoint(sequence).charge_at_pH(pH)


def amino_acid_composition_percent(sequence: str) -> Dict[str, float]:
    """Percent composition of each standard residue (0-100)."""
    n = len(sequence)
    if n == 0:
        return {}
    return {aa: (sequence.count(aa) / n) * 100 for aa in "ACDEFGHIKLMNPQRSTVWY"}


class ProteinAnalyzer:
    """
    Analyze a single protein sequence.

    Parameters
    ----------
    sequence : str
        Protein sequence (any case). Ambiguous residues (X, B, Z, U, O, *)
        and gaps/whitespace are stripped automatically.
    protein_id : str, optional
        Identifier carried through to result dictionaries.
    """

    def __init__(self, sequence: str, protein_id: Optional[str] = None):
        self.protein_id = protein_id
        self.sequence = clean_sequence(sequence)
        if self.sequence:
            self._pa = ProteinAnalysis(self.sequence)
        else:
            self._pa = None

    # --- individual properties -----------------------------------------

    @property
    def length(self) -> int:
        return len(self.sequence)

    def molecular_weight(self) -> float:
        return self._pa.molecular_weight() if self._pa else 0.0

    def isoelectric_point(self) -> float:
        return self._pa.isoelectric_point() if self._pa else 0.0

    def instability_index(self) -> float:
        return self._pa.instability_index() if self._pa else 0.0

    def gravy(self) -> float:
        """Grand Average of Hydropathy (Kyte-Doolittle)."""
        return self._pa.gravy() if self._pa else 0.0

    def aromaticity(self) -> float:
        """Mole fraction of aromatic residues (F + W + Y)."""
        return self._pa.aromaticity() if self._pa else 0.0

    def aliphatic_index(self) -> float:
        return aliphatic_index(self.sequence)

    def boman_index(self) -> float:
        return scale_average(self.sequence, BOMAN_SCALE)

    def wimley_white_hydrophobicity(self) -> float:
        return scale_average(self.sequence, WIMLEY_WHITE_SCALE)

    def eisenberg_hydrophobicity(self) -> float:
        return scale_average(self.sequence, EISENBERG_SCALE)

    def hopp_woods_hydrophilicity(self) -> float:
        return scale_average(self.sequence, HOPP_WOODS_SCALE)

    def net_charge(self, pH: float = 7.0) -> float:
        return net_charge_at_pH(self.sequence, pH)

    def extinction_coefficient(self) -> tuple:
        """
        Returns (reduced, with_disulfides) extinction coefficients at 280 nm
        in units of M^-1 cm^-1.
        """
        if not self._pa:
            return (0, 0)
        return self._pa.molar_extinction_coefficient()

    def stability_classification(self) -> str:
        """ExPASy convention: II <= 40 → 'Stable', otherwise 'Unstable'."""
        return "Stable" if self.instability_index() <= 40 else "Unstable"

    def gravy_classification(self) -> str:
        g = self.gravy()
        if g > 0:
            return "Hydrophobic"
        if g < 0:
            return "Hydrophilic"
        return "Neutral"

    # --- batch summary -------------------------------------------------

    def summary(self, pH: float = 7.0) -> Dict[str, object]:
        """Return all metrics as an ordered dictionary."""
        if not self.sequence:
            return {
                "Protein_ID": self.protein_id,
                "Sequence": "",
                "Length": 0,
                "Note": "Empty or invalid sequence",
            }
        ext_red, ext_ox = self.extinction_coefficient()
        return {
            "Protein_ID": self.protein_id,
            "Sequence": self.sequence,
            "Length": self.length,
            "Molecular_Weight_Da": round(self.molecular_weight(), 3),
            "Theoretical_pI": round(self.isoelectric_point(), 3),
            f"Net_Charge_at_pH_{pH}": round(self.net_charge(pH), 3),
            "Instability_Index": round(self.instability_index(), 3),
            "Stability": self.stability_classification(),
            "Aliphatic_Index": round(self.aliphatic_index(), 3),
            "GRAVY": round(self.gravy(), 4),
            "GRAVY_Class": self.gravy_classification(),
            "Aromaticity": round(self.aromaticity(), 4),
            "Boman_Index": round(self.boman_index(), 4),
            "Wimley_White_Hydrophobicity": round(self.wimley_white_hydrophobicity(), 4),
            "Eisenberg_Hydrophobicity": round(self.eisenberg_hydrophobicity(), 4),
            "Hopp_Woods_Hydrophilicity": round(self.hopp_woods_hydrophilicity(), 4),
            "Ext_Coeff_Reduced_M-1cm-1": ext_red,
            "Ext_Coeff_Cystines_M-1cm-1": ext_ox,
        }
