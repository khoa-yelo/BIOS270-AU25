#!/bin/bash
#SBATCH --job-name=rnaseq_pipeline
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --array=0-7
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=04:00:00

RAW_DATA="/farmshare/home/classes/bios/270/data/SRP624837"
#PROCESSED_DATA="/farmshare/user_data/$USER/processed_data"
SAMPLE_LIST=(SRR35560560 SRR35560561 SRR35560562 SRR35560563 SRR35560564 SRR35560565)
SALMON_INDEX="/farmshare/user_data/khoang99/bios270/data/processed_data/indexes/ecoli_transcripts_index"
NUM_SAMPLES=${#SAMPLE_LIST[@]}

for (( sample_index=0; sample_index<NUM_SAMPLES; sample_index++ )); do
    # Assign tasks based on array index
    if (( sample_index % SLURM_ARRAY_TASK_COUNT != SLURM_ARRAY_TASK_ID )); then
        continue
    fi

    SAMPLE=${SAMPLE_LIST[sample_index]}
    echo "Processing sample: $SAMPLE"
    mkdir -p $PROCESSED_DATA/$SAMPLE/fastqc_outs
    mkdir -p $PROCESSED_DATA/$SAMPLE/trim_galore_outs
    mkdir -p $PROCESSED_DATA/$SAMPLE/salmon_outs
    # Quality control with FastQC
    $RUN fastqc -o $PROCESSED_DATA/$SAMPLE/fastqc_outs $RAW_DATA/$SAMPLE/${SAMPLE}_1.fastq $RAW_DATA/$SAMPLE/${SAMPLE}_2.fastq
    # Trimming with Trim Galore
    $RUN trim_galore --quality 20 --length 20 --paired --output_dir $PROCESSED_DATA/$SAMPLE/trim_galore_outs $RAW_DATA/$SAMPLE/${SAMPLE}_1.fastq $RAW_DATA/$SAMPLE/${SAMPLE}_2.fastq
    # Quantification with Salmon
    $RUN salmon quant -i $SALMON_INDEX -l A \
            -1 $PROCESSED_DATA/$SAMPLE/trim_galore_outs/${SAMPLE}_1_val_1.fq \
            -2 $PROCESSED_DATA/$SAMPLE/trim_galore_outs/${SAMPLE}_2_val_2.fq \
            -p 8 --validateMappings -o $PROCESSED_DATA/$SAMPLE/salmon_outs
done