How could you add a differential expression analysis (DESeq2) step to the rnaseq_pipeline_array_depend.sh script so that it runs only after all salmon jobs have finished? (No code required - describe conceptually)


- To make DESeq2 run only after all Salmon jobs finish, I would submit the DESeq2 step as a separate Slurm 
job that depends on the entire Salmon job array. Then I would submit the DESeq2 job using a dependency flag: 
sbatch --dependency=afterok:<SALMON_ARRAY_JOBID> deseq2.sh
This tells Slurm: only start DESeq2 after every task in the Salmon array finishes successfully. 
This way, DESeq2 won’t run early and only begins once all the quantification results are available.
