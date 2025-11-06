import streamlit as st
import numpy as np
import plotly.express as px
from utils import clean_seq, chunk_lines
from align import compute_alignment, alignment_stats

# ---------------- Streamlit App ----------------
st.set_page_config(page_title="Pairwise Sequence Aligner", layout="wide")
st.title("Pairwise Sequence Aligner")

st.markdown(
    "Paste two sequences below (DNA, RNA, or protein). "
    "Then choose **global** (Needleman–Wunsch) or **local** (Smith–Waterman) alignment and see the result."
)

# ---------------- Sidebar controls ----------------
st.sidebar.header("Input & Settings")

seq1_text = st.sidebar.text_area(
    "Sequence 1", height=120, placeholder="PASTE SEQUENCE 1 (ACGT... or amino acids)"
)
seq2_text = st.sidebar.text_area(
    "Sequence 2", height=120, placeholder="PASTE SEQUENCE 2"
)

mode = st.sidebar.radio(
    "Alignment type", ["Global (Needleman–Wunsch)", "Local (Smith–Waterman)"]
)

with st.sidebar.expander("Advanced scoring", expanded=False):
    match = st.number_input("Match score", value=2.0, step=0.5, format="%.2f")
    mismatch = st.number_input("Mismatch penalty", value=-1.0, step=0.5, format="%.2f")
    gap_open = st.number_input("Gap open penalty", value=-5.0, step=0.5, format="%.2f")
    gap_extend = st.number_input(
        "Gap extend penalty", value=-1.0, step=0.5, format="%.2f"
    )
param_dict = {
    "match": match,
    "mismatch": mismatch,
    "gap_open": gap_open,
    "gap_extend": gap_extend,
    "mode": mode,
}

# ---------------- Load sequences ----------------
seqA = clean_seq(seq1_text)
seqB = clean_seq(seq2_text)

st.write(
    "**Loaded sequences:**",
    f"Seq1 length = `{len(seqA)}` | Seq2 length = `{len(seqB)}`",
)

align_clicked = st.button("▶️ Align sequences", type="primary")

if align_clicked:
    if not (seqA and seqB):
        st.warning("Please paste two sequences before aligning.")
    else:
        try:
            alnA, alnB, score, start, end = compute_alignment(seqA, seqB)
            stats = alignment_stats(alnA, alnB)

            # Metrics
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Alignment length", f"{len(alnA):,}")
            c2.metric("% Identity (no gaps)", f"{stats['pid_nogap']:.2f}%")
            c3.metric("% Identity (with gaps)", f"{stats['pid']:.2f}%")
            c4.metric("Gaps", f"{stats['gaps']:,}")
            c5.metric("Score", f"{score:.2f}")

            # Alignment text block
            st.subheader("Alignment")
            text_block = "\n".join(
                chunk_lines(alnA, stats["match_line"], alnB, width=80)
            )
            st.code(text_block, language="text")

            # Match profile plot
            st.subheader("Match profile (1=match, 0=mismatch; gaps omitted)")
            vals = [v for v in stats["perpos"] if not np.isnan(v)]
            if len(vals) > 0:
                fig = px.line(
                    y=vals,
                    labels={
                        "x": "Aligned position (non-gap)",
                        "y": "Match (1) / Mismatch (0)",
                    },
                    title="Per-position match profile",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No comparable (non-gap) positions to plot.")

            # Download
            out_text = (
                f">seq1_aligned\n{alnA}\n>seq2_aligned\n{alnB}\n# score={score}\n"
            )
            st.download_button(
                "💾 Download aligned sequences (FASTA-like)",
                data=out_text.encode("utf-8"),
                file_name="alignment.txt",
                mime="text/plain",
            )
        except Exception as e:
            st.error(f"Alignment failed: {e}")
            st.exception(e)

st.markdown("---")
st.markdown("© 2025 BIOS270-AU25 Course")
