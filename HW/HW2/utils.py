"""
Utility functions for sequence alignment app."""


def chunk_lines(seqA: str, match: str, seqB: str, width: int = 70):
    """
    Yield chunks of the alignment for display.
    """
    for i in range(0, len(seqA), width):
        yield seqA[i : i + width]
        yield match[i : i + width]
        yield seqB[i : i + width]
        yield ""


def clean_seq(s: str) -> str:
    """Remove FASTA headers, spaces, and newlines."""
    lines = []
    for line in s.splitlines():
        line = line.strip()
        if not line or line.startswith(">"):
            continue
        lines.append(line)
    return "".join(lines).upper()
