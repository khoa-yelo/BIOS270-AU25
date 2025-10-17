# Pairwise Sequence Aligner (Simple)

A tiny Streamlit app that performs **pairwise sequence alignment** (global or local) using **Biopython** and visualizes the result.

## Features
- Upload a FASTA with exactly **two sequences** or paste sequences
- Choose **Global (Needleman–Wunsch)** or **Local (Smith–Waterman)** alignment
- Download aligned sequences

## Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Sample FASTA
See `sample_data/two_seqs.fa` for a quick test.

### Submission

**Paste the URL**

**Read the app.py code and answer the following questions**

What event triggers the alignment run, and why is st.button(...) used?

How does the app choose between the uploaded FASTA and the pasted sequences before aligning?

How are the alignment metrics shown side-by-side using st.columns and st.metric?

What data is passed to Plotly for the “Match profile” line chart, and how are gaps handled?

Where are the scoring parameters read from the sidebar used in the call to pairwise2.align.*?