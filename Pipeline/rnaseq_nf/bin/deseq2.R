#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(optparse)
  library(tximport)
  library(DESeq2)
  library(readr)
  library(ggplot2)
})

option_list <- list(
  make_option(c("-s", "--samplesheet"), type = "character", help = "CSV with columns: sample,read1,read2,condition"),
  make_option(c("-q", "--quant_paths"), type = "character", help = "CSV mapping sample,quant_path"),
  make_option(c("-o", "--outdir"), type = "character", default = "results", help = "Output directory [default: results]")
)
opt <- parse_args(OptionParser(option_list = option_list))
if (is.null(opt$samplesheet) || !file.exists(opt$samplesheet))
  stop("Missing --samplesheet")
if (is.null(opt$quant_paths) || !file.exists(opt$quant_paths))
  stop("Missing --quant_paths")

dir.create(opt$outdir, showWarnings = FALSE, recursive = TRUE)

# ---- Read data ----
ss <- read_csv(opt$samplesheet, show_col_types = FALSE)
qp <- read_csv(opt$quant_paths, show_col_types = FALSE)
qp <- qp[match(ss$sample, qp$sample), ]

req <- c("sample", "condition")
if (!all(req %in% names(ss))) stop("Samplesheet must have columns: sample,condition")
if (!all(c("sample", "quant_path") %in% names(qp))) stop("Quant paths file must have columns: sample,quant_path")

# Align and validate
ss <- ss[ss$sample %in% qp$sample, ]
quant_paths <- setNames(qp$quant_path, qp$sample)
missing <- quant_paths[!file.exists(quant_paths)]
if (length(missing) > 0) stop("Missing quant.sf files: ", paste(names(missing), collapse = ", "))

# ---- DESeq2 ----
txi <- tximport(quant_paths, type = "salmon", txOut = TRUE)
coldata <- data.frame(row.names = ss$sample, condition = factor(ss$condition))
dds <- DESeqDataSetFromTximport(txi, colData = coldata, design = ~condition)
dds <- DESeq(dds)

conds <- levels(coldata$condition)
res <- results(dds, contrast = c("condition", conds[2], conds[1]))

out_csv <- file.path(opt$outdir, paste0("DESeq2_results_", conds[2], "_vs_", conds[1], ".csv"))
write.csv(as.data.frame(res), out_csv)
message("Saved: ", out_csv)

# ---- Volcano Plot ----
res_df <- as.data.frame(res)
res_df$gene <- rownames(res_df)
res_df$significant <- ifelse(!is.na(res_df$padj) & res_df$padj < 0.05 &
                             !is.na(res_df$log2FoldChange) & abs(res_df$log2FoldChange) > 1,
                             "Yes", "No")

p <- ggplot(res_df, aes(log2FoldChange, -log10(padj), color = significant)) +
  geom_point(alpha = 0.5) +
  scale_color_manual(values = c("No" = "grey", "Yes" = "red")) +
  theme_minimal(base_size = 14) +
  labs(title = paste("Volcano:", conds[2], "vs", conds[1]),
       x = "Log2 Fold Change", y = "-Log10 Adjusted P-value")

out_png <- file.path(opt$outdir, paste0("Volcano_", conds[2], "_vs_", conds[1], ".png"))
ggsave(out_png, p, width = 8, height = 6, dpi = 150)
message("Saved: ", out_png)