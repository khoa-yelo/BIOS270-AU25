# Data

Today, we’ll learn how to manage your data effectively with GCP, SQL database, and HDF5 data format.

>*"The dataset is too big to load..." - sighed by generations of grad students moments before their laptops crashed.*

## Resource 

[rclone](https://rclone.org/docs/)

## Setup

For this exercise, you'll need to forward port `53682` in addition to any usual port you specified for code-server/jupyter lab.
This allows `rclone` authentication. For example,

```bash
ssh -L 53682:localhost:53682 -L 23000:localhost:23000 <SUNetID>@login.farmshare.stanford.edu
```

Add `source /farmshare/home/classes/bios/270/setup.sh` into your `~/.bashrc` and run `source ~/.bashrc`

### Google Cloud

Follow these steps to authenticate (`project-id` is the id of project `BIOS270` you created in `Setup.md`).

`gcloud` command is available in `bioinformatics_latest.sif` container

```
gcloud auth login
gcloud config set project <project-id>

gcloud auth application-default login
gcloud auth application-default set-quota-project <project-id>
```

### Google Cloud Storage (GCS)

On GCS, create a new `Bucket` named `bacteria-<sunetid>`

On Farmshare, set up GCS remote using `rclone config` -> `New remote`
(`rclone` is available in `bioinformatics_latest.sif` container)

Answer `true` when prompted 

```
Enter a boolean value (true or false). Press Enter for the default ("false").
bucket_policy_only>
```

### Google Drive

On Farmshare, set up Drive remote using `rclone config` -> `New remote`

### Google BigQuery

On BigQuery, create a new `Dataset` named `bacteria`

---

## Dataset Overview

We will be working with a dataset containing approximately 2,000 annotated bacterial long-read assemblies. Such a dataset can inspire many biological questions. For example, How many proteins does a typical bacterium encode? or How conserved are proteins across species? However, exploring these questions directly from the raw data is inconvenient and inefficient.

To enable efficient querying, analysis, and future machine-learning applications, we will first convert the dataset into more suitable formats: an SQL database and an HDF5 file.


`/farmshare/home/classes/bios/270/data/bacteria` contains long-read assemblies (`*.fna`), annotations (`genomic.gff`), predicted protein sequences (`protein.faa`) of 1958 bacteria isolates.

`/farmshare/home/classes/bios/270/data/bacteria_supp` contains a metadata file containing information on each assembly (`assembly_data_report.jsonl`) and [`mmseqs2`](https://github.com/soedinglab/MMseqs2) clustering output of all proteins predicted from 1958 bacteria isolates (`clusters_mmseqclust_id03_c08.tsv`)

`/farmshare/home/classes/bios/270/data/protein_data/` contains protein embeddings (in batches of 10,000) of all predicted proteins in 1958 isolates. Protein embeddings are vector representations of protein sequences - proteins that are similar in sequence or structure are expected to have more similar embeddings


---

## Database

### 1. Create a Local SQL Database

Submit the script `create_bacteria_db.sh` as a Slurm job to create a local SQLite database named `bacteria.db`.

```bash
sbatch create_bacteria_db.sh
```

While the job is running, answer the following questions:

- Examine `create_bacteria_db.sh`, how many tables will be created in the database?  
- In the `insert_gff_table.py` script you submitted, explain the logic of using `try` and `except`. Why is this necessary?

```python
while try_num < max_retries:
    try_num += 1
    try:
        df.to_sql(gff_table_name, conn, if_exists="append", index=False)
        break
    except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
        if "database is locked" in str(e):
            logging.info(f"Database is locked, retrying {try_num}/{max_retries}")
            time.sleep(1)
        else:
            raise e
```

After the database has been created, use `rclone copy` to copy the output `bacteria.db` to your `bacteria-<sunetid>` bucket on `GCS` and a dedicated folder on `Drive`.

---

### 2. Query the Created Database

Complete the `TODO` sections in `query_bacteria_db.py`. You may want to examine the `gff2df` function in `insert_gff_table.py` to understand the columns in `gff` table.

Then, run `query_bacteria_db.py` (using `bioinformatics_latest.sif` container)

```bash
python query_bacteria_db.py --database_path <path to the bacteria.db created in Section 1>
```

Record the runtime. You may stop the session early if it takes too long and only record the runtime of the first few iterations.

Then, uncomment `db.index_record_ids()` in `query_bacteria_db.py` and note how the runtime changes.  
Why do you think this is the case?

---

### 3. Upload to Google BigQuery

The dataset you are handling is relatively small. However, for larger datasets or collaborative access, uploading to **Google BigQuery** is a practical approach.

Examine the `upload_bigquery.py` script.  
Explain the role of `CHUNK_SIZE` and why it is necessary:

```python
df = pd.read_sql_query(
    f"SELECT * FROM {table} LIMIT {CHUNK_SIZE} OFFSET {offset}",
    conn
)
```
Run the `upload_bigquery.py` script (using `bioinformatics_latest.sif` container)

```bash
python upload_bigquery.py --local_database_path <path to the bacteria.db created in Section 1> --project_id <GCP project-id> --dataset_id bacteria
```

Once your dataset has been uploaded, create a query on BigQuery that involves at least **two tables** from the dataset.  
Export the query results as a **CSV file** to **GCS**.

---

### 4. HDF5 Data

Review the `create_protein_h5.sh` and `create_protein_h5.py` scripts.  
Make sure you understand their functionality. You won't need to run these scripts as they take a few hours to complete.

Explain why the following chunk configuration makes sense - what kind of data access pattern is expected, and why does this align with biological use cases?

```python
chunk_size = 1000
chunks = (chunk_size, n_features)
```

---

### 5. Practice – Combining SQL and HDF5

For this exercise, use data from `/farmshare/home/classes/bios/270/data/processed_bacteria_data`

Write a Python script that 
- reads in `bacteria.db` and `protein_embeddings.h5`
- takes a `record id` and `metric` (either `mean` or `mean_mid`) as input params
- outputs the corresponding protein embeddings **matrix** with shape `(N, D)`, where:

    - `N` = number of protein IDs in the record  
    - `D` = embedding dimension (164)

Save the resulting matrix as a `.npy` file.

**Hints:**
- You may import classes and functions from `query_bacteria_db.py`.
- Consider creating a **dictionary** mapping between protein IDs and their indices in h5 dataset to avoid repeated lookups using `list.index()`.
