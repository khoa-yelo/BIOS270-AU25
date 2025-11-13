library(DESeq2)
library(ggplot2)

set.seed(123)

# --------------------------
# Parameters
# --------------------------
n_genes <- 50
n_samples <- 6    # 3 per group
n_sig <- 10       # number of truly DE genes

# --------------------------
# Simulate counts
# --------------------------
base <- rpois(n_genes, 100)          # baseline counts
fold <- c(rep(5, n_sig), rep(1, n_genes - n_sig))  # stronger fold change

counts <- sapply(1:n_samples, function(i) {
  if(i <= n_samples/2) {
    rnbinom(n_genes, mu = base, size = 1/0.1)    # Control (less dispersion)
  } else {
    rnbinom(n_genes, mu = base * fold, size = 1/0.1)  # Treatment
  }
})
counts <- matrix(counts, nrow = n_genes)
rownames(counts) <- paste0("Gene", 1:n_genes)
colnames(counts) <- paste0("Sample", 1:n_samples)

# --------------------------
# Sample metadata
# --------------------------
coldata <- data.frame(condition = rep(c("Control","Treatment"), each = n_samples/2))
rownames(coldata) <- colnames(counts)

# --------------------------
# DESeq2 analysis
# --------------------------
dds <- DESeqDataSetFromMatrix(counts, coldata, design = ~condition)
dds <- DESeq(dds, fitType = "mean")
res <- results(dds)
res_df <- as.data.frame(res)
res_df$gene <- rownames(res_df)

# --------------------------
# Volcano plot
# --------------------------
res_df$significant <- ifelse(res_df$padj < 0.05, "Yes", "No")

ggplot(res_df, aes(log2FoldChange, -log10(pvalue), color = significant)) +
  geom_point() +
  scale_color_manual(values = c("No"="steelblue","Yes"="red")) +
  theme_minimal() +
  labs(title = "DESeq2 Volcano Plot", x="Log2 Fold Change", y="-log10(p-value)")

# save plot
ggsave("r_example_plot.png", dpi=300)