#!/usr/bin/env python3
import argparse
import json
import sys
import os
import h5py
import numpy as np
from collections import defaultdict
from glob import glob
import logging
import tqdm


os.environ["PYTHONUNBUFFERED"] = "1"
logging.basicConfig(
    level=logging.INFO,                   
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout), 
    ]
)

def main():
    parser = argparse.ArgumentParser(description="Create and populate an HDF5 file of protein embeddings.")
    parser.add_argument("--output", required=True, help="Output HDF5 file path.")
    parser.add_argument("--protein_ids", required=True, help="Path to a file containing all protein IDs (one per line).")
    parser.add_argument("--protein_data", default="/farmshare/home/classes/bios/270/data/protein_data/*.json", help="Glob pattern for JSON input files.")
    args = parser.parse_args()

    # Load protein IDs
    with open(args.protein_ids) as prot_file:
        all_protein_ids = [line.strip() for line in prot_file if line.strip()]

    n_samples = len(all_protein_ids)
    n_features = 164
    chunk_size = 1000

    # Build index map
    index_map = defaultdict(list)
    for i, id in enumerate(all_protein_ids):
        index_map[id].append(i)
    
    logging.info("Creating HDF5 file...")
    # Create a new HDF5 file
    with h5py.File(args.output, "w") as f:
        f.create_dataset(
            "mean_embeddings",
            shape=(n_samples, n_features),
            dtype=np.float32,
            chunks=(chunk_size, n_features)
        )
        f.create_dataset(
            "mean_mid_embeddings",
            shape=(n_samples, n_features),
            dtype=np.float32,
            chunks=(chunk_size, n_features)
        )
        dt = h5py.string_dtype(encoding='utf-8')
        f.create_dataset("protein_ids", data=all_protein_ids, shape=(n_samples,), dtype=dt)

    logging.info("Populating HDF5 file...")
    # Populate HDF5
    with h5py.File(args.output, "r+") as h5_file:
        for batch in tqdm.tqdm(glob(args.protein_data)):
            with open(batch) as batch_file:
                data = json.load(batch_file)
                for key, val in data.items():
                    idx = index_map[key]
                    val_mean_broadcasted = np.tile(val["mean"], (len(idx), 1))
                    val_mean_mid_broadcasted = np.tile(val["mean_mid"], (len(idx), 1))
                    h5_file["mean_embeddings"][idx, :] = val_mean_broadcasted
                    h5_file["mean_mid_embeddings"][idx, :] = val_mean_mid_broadcasted

    logging.info("Done.")

if __name__ == "__main__":
    main()
