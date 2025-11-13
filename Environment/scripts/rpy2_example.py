import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from rpy2 import robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr

# --------------------------
# Import R packages
# --------------------------
DESeq2 = importr("DESeq2")
base = importr("base")

# --------------------------
# Simulate toy count data (50 genes x 6 samples)
# --------------------------
np.random.seed(123)
n_genes = 50
n_samples = 6
n_sig = 10  # number of truly DE genes

# Base counts
base_counts = np.random.poisson(100, n_genes)
fold = np.array([5] * n_sig + [1] * (n_genes - n_sig))  # first 10 genes are DE

# Generate counts matrix: 3 Control samples, 3 Treatment samples
control_counts = np.column_stack(
    [
        np.random.negative_binomial(n=20, p=20 / (20 + base_counts), size=n_genes)
        for _ in range(3)
    ]
)
treat_counts = np.column_stack(
    [
        np.random.negative_binomial(
            n=20, p=20 / (20 + base_counts * fold), size=n_genes
        )
        for _ in range(3)
    ]
)
counts = np.column_stack([control_counts, treat_counts])  # shape = (50, 6)

counts_df = pd.DataFrame(
    counts,
    index=[f"Gene{i+1}" for i in range(n_genes)],
    columns=[f"Sample{i+1}" for i in range(n_samples)],
)

# Sample metadata
coldata = pd.DataFrame(
    {"condition": ["Control"] * 3 + ["Treatment"] * 3}, index=counts_df.columns
)

# --------------------------
# Convert pandas DataFrames to R objects (new API)
# --------------------------
with localconverter(ro.default_converter + pandas2ri.converter):
    r_counts = ro.conversion.py2rpy(counts_df)
    r_coldata = ro.conversion.py2rpy(coldata)

# --------------------------
# Create DESeqDataSet and run DESeq2
# --------------------------
design = ro.Formula("~ condition")
dds = DESeq2.DESeqDataSetFromMatrix(
    countData=r_counts, colData=r_coldata, design=design
)

dds = DESeq2.DESeq(dds, fitType="mean")
res = DESeq2.results(dds)

# --------------------------
# Convert DESeq2 results (S4) to pandas DataFrame
# --------------------------
res_df_r = base.as_data_frame(res)  # R data.frame
with localconverter(ro.default_converter + pandas2ri.converter):
    res_df = ro.conversion.rpy2py(res_df_r)  # pandas DataFrame

res_df["gene"] = counts_df.index
res_df["significant"] = res_df["padj"] < 0.05

# --------------------------
# Volcano plot
# --------------------------
plt.figure(figsize=(7, 5))
sns.scatterplot(
    data=res_df,
    x="log2FoldChange",
    y=-np.log10(res_df["pvalue"]),
    hue="significant",
    palette={True: "red", False: "steelblue"},
    legend=False,
)
plt.xlabel("Log2 Fold Change")
plt.ylabel("-log10(p-value)")
plt.title("Volcano Plot from DESeq2 (rpy2)")
plt.axhline(-np.log10(0.05), color="grey", linestyle="--")  # significance threshold
plt.tight_layout()
plt.savefig("r2py_example_plots.png", dpi=300)
