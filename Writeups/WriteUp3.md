How many tables will be created in the database?
- 3 Tables: GFF, Protein Cluster, Metadata

In the insert_gff_table.py script you submitted, explain the logic of using try and except. Why is this necessary?
- This was neccessary To catch “database is locked” errors caused by multiple Slurm tasks writing to SQLite at the same time. Ie It retries the write operation instead of failing

Record the runtime - if it takes too long, you may stop the session early.
- Stopped the session early

Then, uncomment db.index_record_ids() and note how the runtime changes.
What do you observe, and why do you think this happens?
- The runtime was a lot quicker. This is because SQLite uses the B-tree index to perform logarithmic-time seeks rather than linear scans

Examine the upload_bigquery.py script.
Explain the role of CHUNK_SIZE and why it is necessary:
- CHUNK_SIZE sets how many rows are uploaded to BigQuery at a time.
  It is necessary since it prevents memory overload and upload failures by splitting large data into smaller, manageable parts.

Explain why the following chunk configuration makes sense
- This means each chunk stores 1,000 proteins, with all of their associated feature values

what kind of data access pattern is expected
- Accessing proteins in small batches (like 1,000 at a time).

why does this align with biological use cases?
- Bio data is often processed in groups of proteins, not all at once, making batch reading faster and memory-efficient.





