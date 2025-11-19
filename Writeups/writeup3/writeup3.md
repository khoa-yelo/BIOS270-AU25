# Write-up 3:

**Name:** Riley Juenemann       
**Student ID:** rjuene    
**Date:** 11/18/2025    

---

## 1. Create a Local SQL Database

Three tables will be created in the database (gff, protein cluser, and metadata).

The try-except clause is needed because the SLURM script creates multiple tasks that are all accessing the same file. So if one is writing to that file then
it might be locked temporarily. This is why it retries a little bit later rather than crashing.

## 2. Query the Created Database

Runtime: <>
Runtime after uncommenting `db.index_record_ids()`: <>
Why it changes:

## 3. Upload to Google BigQuery

Explain the role of CHUNK_SIZE and why it is necessary: <>

## 4. HDF5 Data

Explain why the following chunk configuration makes sense - what kind of data access pattern is expected, and why does this align with biological use cases?

<>

## 5. Practice – Combining SQL and HDF5

<Write python file>



