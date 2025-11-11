import sys
import os
from os.path import join, basename, dirname
from glob import glob
import logging
import argparse
import time

import numpy as np
import pandas as pd
import sqlite3

from BCBio import GFF


os.environ["PYTHONUNBUFFERED"] = "1"
logging.basicConfig(
    level=logging.INFO,                    
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  
    ]
)

def parse_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", type=str, required=True)
    parser.add_argument("--gff_table_name", type=str, default="gff")
    parser.add_argument("--gff_path", type=str, default="/farmshare/home/classes/bios/270/data/bacteria/*/*gff")
    parser.add_argument("--max_retries", type=int, default=20)
    args = parser.parse_args()
    return args


def gff2df(path):
    results = []
    assembly_id = basename(dirname(path))
    with open(path) as in_handle:
        for record in GFF.parse(in_handle):
            for feat in record.features:
                fstart = int(feat.location.start)
                fend   = int(feat.location.end)
                protein_id = None
                biotype = None
                if feat.type == "gene":
                    if feat.sub_features:
                        subfeat_qualifiers = feat.sub_features[0].qualifiers
                        protein_id = subfeat_qualifiers.get("protein_id", [None])[0]
                    biotype = feat.qualifiers["gene_biotype"][0]
                results.append({
                    "assembly_id": assembly_id,
                    "record_id": record.id,
                    "feature_id": feat.id,
                    "start": fstart,
                    "end": fend,
                    "length": fend - fstart,
                    "strand": feat.location.strand,
                    "type": feat.type,
                    "biotype": biotype,
                    "protein_id": protein_id,
                })
    df = pd.DataFrame(results)
    return df

def insert_data(conn, df, args):
    assembly_id = df["assembly_id"].iloc[0]
    gff_table_name = args.gff_table_name
    max_retries = args.max_retries
    try_num = 0
    while try_num < max_retries:
        try_num +=1
        try:
            df.to_sql(gff_table_name, conn, if_exists="append", index=False)
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
    gff_files = glob(args.gff_path)
    gff_file_dict = {basename(dirname(file)): file for file in gff_files}
    logging.info(f"Total number of assemblies: {len(gff_file_dict)}")
    
    n = -1
    for assembly_id, file in gff_file_dict.items():
        n += 1
        if SLURM_ARRAY_TASK_ID != -1 and SLURM_ARRAY_TASK_COUNT != 1:
            if n % SLURM_ARRAY_TASK_COUNT != SLURM_ARRAY_TASK_ID:
                continue
        insert_data(conn, gff2df(file), args)
        logging.info(f"Finished inserting {assembly_id}")

    conn.close()

if __name__ == "__main__":
    main()
