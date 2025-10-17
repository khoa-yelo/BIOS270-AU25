import numpy as np
from Bio import pairwise2


def compute_alignment(a: str, b: str, param_dict: dict = None):
    """Compute pairwise alignment using Biopython's pairwise2.
    Returns the best alignment (alnA, alnB, score, start, end).
    """
    param_dict = param_dict or {}
    match = param_dict.get("match", 2)
    mismatch = param_dict.get("mismatch", -1)
    gap_open = param_dict.get("gap_open", -5)
    gap_extend = param_dict.get("gap_extend", -1)
    mode = param_dict.get("mode", "global")
    if "Global" in mode:
        aln = pairwise2.align.globalms(
            a, b, match, mismatch, gap_open, gap_extend, one_alignment_only=True
        )[0]
    else:
        aln = pairwise2.align.localms(
            a, b, match, mismatch, gap_open, gap_extend, one_alignment_only=True
        )[0]
    # aln: (seqA, seqB, score, start, end)
    return aln


def alignment_stats(alnA: str, alnB: str):
    matches = mismatches = gaps = 0
    match_marks = []
    perpos = []  # 1=match, 0=mismatch, np.nan=gap
    for x, y in zip(alnA, alnB):
        if x == "-" or y == "-":
            gaps += 1
            match_marks.append(" ")
            perpos.append(np.nan)
        elif x == y:
            matches += 1
            match_marks.append("|")
            perpos.append(1)
        else:
            mismatches += 1
            match_marks.append(".")
            perpos.append(0)
    denom = matches + mismatches
    pid_nogap = (matches / denom * 100.0) if denom else 0.0
    pid = (matches / (denom + gaps) * 100.0) if (denom + gaps) else 0.0
    return {
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "pid_nogap": pid_nogap,
        "pid": pid,
        "match_line": "".join(match_marks),
        "perpos": perpos,
    }
