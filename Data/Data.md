# Data

Today, we’ll learn how to manage your data effectively with GCP, SQL database, and HDF5 data format.

>*"The dataset is too big to load..." - sighed by generations of grad students moments before their laptops crashed.*

## Resource 

[rclone](https://rclone.org/docs/)

## Setup

### Google Cloud

Follow these steps to authenticate (`project-id` is the id of project `BIOS270` you created in `Setup` lecture )

```
gcloud auth login
gcloud config set project <project-id>

gcloud auth application-default login
gcloud auth application-default set-quota-project <project-id>
```

### Google Cloud Storage (GCS)

Create a new `Bucket` named `bacteria`

Set up GCS remote using `rclone config` -> `New remote`

### Google Drive

Set up Drive remote using `rclone config` -> `New remote`

### Google BigQuery

Create a new `Dataset` named `bacteria`

---

## Dataset Overview

`/farmshare/home/classes/bios/270/data/bacteria` contains long-read assemblies (`*.fna`), annotations (`genomic.gff`), predicted proteins sequence (`protein.faa`) of 1958 bacteria isolates.

`/farmshare/home/classes/bios/270/data/bacteria_supp` contains metadata file containing information on each assembly (`assembly_data_report.jsonl`) and clustering of all proteins predicted from 1958 bacteria isolates (`clusters_mmseqclust_id03_c08.tsv`)

`/farmshare/home/classes/bios/270/data/protein_data/` contains protein embeddings (in batch of 10,000) of all predicted proteins in 1958 isolates

In order to extract insights (and later build machine learning model) from this dataset, we will convert these data into SQL database and HDF5 data format.

---

## Database

### 1. Create a Local SQL Database

Submit the script `create_bacteria_db.sh` as a Slurm job to create a local SQLite database named `bacteria.db`.

While the job is running, answer the following questions:

- How many tables will be created in the database?  
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

Use `rclone copy` to copy the output `bacteria.db` to your `bacteria` bucket on GCS and your folder on Drive.

---

### 2. Query the Created Database

Complete the `TODO` section in `query_bacteria_db.py`.

Record the runtime - if it takes too long, you may stop the session early.

Then, uncomment `db.index_record_ids()` and note how the runtime changes.  
What do you observe, and why do you think this happens?

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

Once your dataset has been uploaded, create a query in BigQuery that joins at least **two tables** from the dataset.  
Export the query results as a **CSV file** to **Google Cloud Storage (GCS)**.

---

### 4. HDF5 Data

Review the `create_protein_h5.sh` and `create_protein_h5.py` scripts.  
Make sure you understand their functionality.  

Explain why the following chunk configuration makes sense - what kind of data access pattern is expected, and why does this align with biological use cases?

```python
chunk_size = 1000
chunks = (chunk_size, n_features)
```

---

### 5. Practice – Combining SQL and HDF5

Write a Python script that takes a `record id` and `metric` (either `mean` or `mean_mid`) as input and outputs the corresponding protein embeddings **matrix** with shape `(N, D)`, where:

- `N` = number of protein IDs in the record  
- `D` = embedding dimension (164)

Save the resulting matrix as a `.npy` file.
Since it takes a few hours to create h5 file from `create_protein_h5.sh`, use data from `/farmshare/home/classes/bios/270/data/processed_bacteria_data` for this exercise

**Hints:**
- You may import class and functions from `query_bacteria_db.py`.
- Consider creating a **dictionary** mapping between protein IDs and their indices in h5 dataset to avoid repeated lookups using `list.index()`.
