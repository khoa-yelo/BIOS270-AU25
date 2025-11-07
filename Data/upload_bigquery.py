import pandas as pd
import sqlite3
from google.cloud import bigquery
from tqdm import tqdm
import argparse

CHUNK_SIZE = 500_000

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local_database_path", type=str, required=True)
    parser.add_argument("--project_id", type=str, required=True)
    parser.add_argument("--dataset_id", type=str, required=True)
    args = parser.parse_args()
    return args


def upload_bq(args):
    # get tables from local database
    conn = sqlite3.connect(args.local_database_path)
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    tables = [table[0] for table in tables]
    # upload to bigquery
    client = bigquery.Client(project=args.project_id)
    for table in tables:
        print(f"\nUploading table: {table}")
        table_id = f"{args.project_id}.{args.dataset_id}.{table}"
        total_rows = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        offset = 0
        with tqdm(total=total_rows, desc=f"{table}") as pbar:
            while True:
                df = pd.read_sql_query(
                    f"SELECT * FROM {table} LIMIT {CHUNK_SIZE} OFFSET {offset}",
                    conn
                )
                if df.empty:
                    break
                job = client.load_table_from_dataframe(
                    df,
                    table_id,
                    job_config=bigquery.LoadJobConfig(
                        write_disposition="WRITE_APPEND"
                    )
                )
                job.result()  # wait for the job to complete
                offset += len(df) 
                pbar.update(len(df))
        print(f"Finished uploading {table}")
    conn.close()


if __name__ == "__main__":
    args = parse_args()
    upload_bq(args)