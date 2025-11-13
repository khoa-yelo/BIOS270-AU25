import sys
import os
from os.path import join, basename, dirname
import logging
import argparse
import time

import numpy as np
import pandas as pd
import sqlite3



os.environ["PYTHONUNBUFFERED"] = "1"
logging.basicConfig(
    level=logging.INFO,                    
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),]
)

def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", type=str, required=True)
    parser.add_argument("--cluster_table_name", type=str, default="protein_cluster")
    parser.add_argument("--cluster_path", type=str, default="/farmshare/home/classes/bios/270/data/bacteria_supp/clusters_mmseqclust_id03_c08.tsv")
    parser.add_argument("--max_retries", type=int, default=20)
    args = parser.parse_args()
    return args


def insert_data(conn, df, args):
    max_retries = args.max_retries
    try_num = 0
    while try_num < max_retries:
        try_num +=1
        try:
            df.to_sql(args.cluster_table_name, conn, if_exists="replace", index=False)
            break
        except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
            if "database is locked" in str(e):
                logging.info(f"Database is locked, retrying {try_num}/{max_retries}")
                time.sleep(1)
            else:
                raise e

def main():
    SLURM_ARRAY_TASK_ID = int(os.environ.get("SLURM_ARRAY_TASK_ID", -1))
    SLURM_ARRAY_TASK_COUNT = int(os.environ.get("SLURM_ARRAY_TASK_COUNT", 1))
    logging.info(f"SLURM_ARRAY_TASK_ID: {SLURM_ARRAY_TASK_ID}")
    logging.info(f"SLURM_ARRAY_TASK_COUNT: {SLURM_ARRAY_TASK_COUNT}")
    args = parse_args()

    conn = sqlite3.connect(args.database_path)  
    df = pd.read_csv(args.cluster_path, sep="\t", header=None)
    df.columns = ["cluster_id", "protein_id"] 
    size_map = df.groupby("cluster_id").size()
    df["cluster_size"] = df.cluster_id.map(size_map)
    if SLURM_ARRAY_TASK_ID <= 0:
        insert_data(conn, df, args)
        logging.info(f"Finished inserting {args.cluster_table_name}")
    conn.close()

if __name__ == "__main__":
    main()
