from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------
# Define example sequences
# --------------------------
records = [
    SeqRecord(Seq("ATGCGTACGTAGCTAGCTAG"), id="seq1"),
    SeqRecord(Seq("ATGCGTAGCTAGCTAGCTAGCTAGCTA"), id="seq2"),
    SeqRecord(Seq("ATGCGTACGTA"), id="seq3"),
    SeqRecord(Seq("ATGGGCCCTTAACCGG"), id="seq4"),
]

# --------------------------
# Compute GC content
# --------------------------
data = []
for rec in records:
    seq = rec.seq
    gc = float(seq.count("G") + seq.count("C")) / len(seq) * 100
    data.append({"ID": rec.id, "GC_content": gc})

df = pd.DataFrame(data)

# --------------------------
# Plot GC content
# --------------------------
plt.figure(figsize=(6, 4))
sns.barplot(x="ID", y="GC_content", data=df)
plt.ylabel("GC Content (%)")
plt.title("GC Content of Sequences")
plt.ylim(0, 100)
plt.savefig("python_example_plot.png", dpi=300)
plt.show()
