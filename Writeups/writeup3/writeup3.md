# Write-up 3: Data

**Name:** Louise Lima  
**Student ID:** llima23  
**Date:** 12/01/2025  

---

##Workflow
1. ssh -L 53682:localhost:53682 -L 23000:localhost:23000 <SUNetID>@login.farmshare.stanford.edu
2. module load apptainer
3. singularity run -B /farmshare/user_data/$USER,/farmshare/home/classes/bios/270 /farmshare/home/classes/bios/270/envs/bioinformatics_latest.sif
4. gcloud project id: bios270-478122

#Database
1. create_bacteria_db.sh would create 3 tables, 1 per .py run file
2. because if the database is locked it lets the user know that the table was n>
3. query_bacteria_db.py
	runtime with db.index_record_ids(): 17.5seconds, total protein_ids: 16286240, record_ids:4100
	runtime without: 20.64seconds, same total protein_ids and record_ids	
	faster search - leverages a sorted data structure to quickly locate specific records, rather than scanning the entire database. 
4. Chunk_size: subsetting data to look at only smaller sections at a time to be able to analyze it
	determines batch size/how many rows are read at a time
5. 1000 batch size is reasonable for proteins as a good balance between speed, memory, and stability
6. Added combining.npy as my new code to combine bacteria.db and protein_embeddings.h5
