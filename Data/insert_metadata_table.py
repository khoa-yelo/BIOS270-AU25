import sys
import os
from os.path import join, basename, dirname
import logging
import argparse
import time
import json

import numpy as np
import pandas as pd
import sqlite3



os.environ["PYTHONUNBUFFERED"] = "1"
logging.basicConfig(
    level=logging.INFO,                
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout), ]
        
)

def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", type=str, required=True)
    parser.add_argument("--metadata_table_name", type=str, default="metadata")
    parser.add_argument("--metadata_path", type=str, default="/farmshare/home/classes/bios/270/data/bacteria_supp/assembly_data_report.jsonl")
    parser.add_argument("--max_retries", type=int, default=20)
    args = parser.parse_args()
    return args


def insert_data(conn, df, args):
    max_retries = args.max_retries
    try_num = 0
    while try_num < max_retries:
        try_num +=1
        try:
            df.to_sql(args.metadata_table_name, conn, if_exists="replace", index=False)
            break
        except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
            if "database is locked" in str(e):
                logging.info(f"Database is locked, retrying {try_num}/{max_retries}")
                time.sleep(1)
            else:
                raise e

def flatten_dict_columns(df, max_depth=5):
    """
    Recursively flattens dict columns in a DataFrame.
    Each nested key becomes a column with dot notation, e.g. 'meta.author.name'
    """
    for _ in range(max_depth): 
        dict_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, dict)).any()]
        if not dict_cols:
            break
        for col in dict_cols:
            expanded = pd.json_normalize(df[col]).add_prefix(f"{col}.")
            df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
    return df

def json_dump_column(df):
    def needs_dump(x):
        return isinstance(x, (list, dict, tuple, set, np.ndarray))
    for col in df.columns:
        # if column has any such object, convert all such entries to JSON strings
        if df[col].apply(lambda x: needs_dump(x)).any():
            df[col] = df[col].apply(lambda x: json.dumps(list(x)) if isinstance(x, (set, np.ndarray)) else (json.dumps(x) if isinstance(x, (list, dict, tuple)) else x))
    return df

def sanitize_column_names(df):
    """Replace invalid BigQuery characters in column names."""
    df.columns = (
        df.columns
        .str.replace(r"[^a-zA-Z0-9_]", "_", regex=True)  # replace invalid chars with underscore
        .str.replace(r"__+", "_", regex=True)            # collapse multiple underscores
        .str.strip("_")                                  # remove leading/trailing underscores
    )
    return df

def main():
    SLURM_ARRAY_TASK_ID = int(os.environ.get("SLURM_ARRAY_TASK_ID", -1))
    SLURM_ARRAY_TASK_COUNT = int(os.environ.get("SLURM_ARRAY_TASK_COUNT", 1))
    logging.info(f"SLURM_ARRAY_TASK_ID: {SLURM_ARRAY_TASK_ID}")
    logging.info(f"SLURM_ARRAY_TASK_COUNT: {SLURM_ARRAY_TASK_COUNT}")
    args = parse_args()

    conn = sqlite3.connect(args.database_path)  
    df_assembly = pd.read_json(args.metadata_path, lines=True)
    df_assembly = flatten_dict_columns(df_assembly)
    df_assembly = sanitize_column_names(df_assembly)
    df_assembly = json_dump_column(df_assembly)
    if SLURM_ARRAY_TASK_ID <= 0:
        insert_data(conn, df_assembly, args)
        logging.info(f"Finished inserting {args.metadata_table_name}")
    conn.close()

if __name__ == "__main__":
    main()
