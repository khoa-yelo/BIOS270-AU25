#!/usr/bin/env python3
"""
Script to extract protein embeddings for a specific record_id from HDF5 file.
Combines SQL database queries with HDF5 array access.
"""

import argparse
import numpy as np
import h5py
import sys
from query_bacteria_db import BacteriaDatabase


def parse_args():
    parser = argparse.ArgumentParser(
        description='Extract protein embeddings for a record from bacteria database'
    )
    parser.add_argument(
        '--database_path',
        type=str,
        required=True,
        help='Path to bacteria.db SQLite database'
    )
    parser.add_argument(
        '--h5_path',
        type=str,
        required=True,
        help='Path to protein_embeddings.h5 file'
    )
    parser.add_argument(
        '--record_id',
        type=str,
        required=True,
        help='Record ID (chromosome/contig) to extract proteins from'
    )
    parser.add_argument(
        '--metric',
        type=str,
        choices=['mean', 'mean_mid'],
        required=True,
        help='Embedding metric to use (mean or mean_mid)'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default=None,
        help='Output .npy file path (default: {record_id}_{metric}.npy)'
    )
    return parser.parse_args()


def create_protein_id_to_index_map(h5_file):
    """
    Create a dictionary mapping protein_id -> index in HDF5 dataset.
    This avoids slow repeated list.index() lookups.
    
    Args:
        h5_file: Open h5py.File object
        
    Returns:
        dict: {protein_id: index}
    """
    protein_ids = h5_file['protein_ids'][:]
    
    # Decode if bytes (HDF5 sometimes stores strings as bytes)
    if protein_ids.dtype.kind == 'S' or protein_ids.dtype.kind == 'O':
        protein_ids = [pid.decode('utf-8') if isinstance(pid, bytes) else pid 
                      for pid in protein_ids]
    
    # Create mapping: protein_id -> index
    protein_id_to_idx = {pid: idx for idx, pid in enumerate(protein_ids)}
    
    return protein_id_to_idx


def get_embeddings_for_record(db, h5_file, record_id, metric):
    """
    Extract embeddings for all proteins in a specific record.
    
    Args:
        db: BacteriaDatabase object
        h5_file: Open h5py.File object
        record_id: Record ID to query
        metric: 'mean' or 'mean_mid'
        
    Returns:
        numpy.ndarray: Protein embeddings with shape (N, 164)
    """
    # Step 1: Get protein IDs from SQL database
    print(f"Querying protein IDs for record: {record_id}")
    protein_ids = db.get_protein_ids_from_record_id(record_id)
    
    if not protein_ids:
        print(f"Warning: No proteins found for record {record_id}")
        return np.array([])
    
    print(f"Found {len(protein_ids)} proteins")
    
    # Step 2: Create protein ID to index mapping (efficient lookup)
    print("Creating protein ID to index mapping...")
    protein_id_to_idx = create_protein_id_to_index_map(h5_file)
    
    # Step 3: Get indices for our protein IDs
    indices = []
    missing_proteins = []
    
    for pid in protein_ids:
        if pid in protein_id_to_idx:
            indices.append(protein_id_to_idx[pid])
        else:
            missing_proteins.append(pid)
    
    if missing_proteins:
        print(f"Warning: {len(missing_proteins)} proteins not found in HDF5 file")
        print(f"First few missing: {missing_proteins[:5]}")
    
    if not indices:
        print("Error: No matching proteins found in HDF5 file")
        return np.array([])
    
    print(f"Found {len(indices)} matching proteins in HDF5")
    
    # Step 4: Extract embeddings from HDF5
    print(f"Extracting embeddings using metric: {metric}")
    embeddings_dataset = h5_file[metric]
    
    # Get embeddings for all indices at once (efficient!)
    embeddings = embeddings_dataset[indices, :]
    
    print(f"Extracted embeddings shape: {embeddings.shape}")
    
    return embeddings


def main():
    args = parse_args()
    
    # Set default output path
    if args.output_path is None:
        # Clean record_id for filename (replace slashes, spaces, etc.)
        clean_record_id = args.record_id.replace('/', '_').replace(' ', '_')
        args.output_path = f"{clean_record_id}_{args.metric}.npy"
    
    print(f"=== Protein Embedding Extraction ===")
    print(f"Database: {args.database_path}")
    print(f"HDF5 file: {args.h5_path}")
    print(f"Record ID: {args.record_id}")
    print(f"Metric: {args.metric}")
    print(f"Output: {args.output_path}\n")
    
    # Open database
    print("Opening database...")
    db = BacteriaDatabase(args.database_path)
    
    # Open HDF5 file
    print("Opening HDF5 file...")
    with h5py.File(args.h5_path, 'r') as h5_file:
        # Extract embeddings
        embeddings = get_embeddings_for_record(
            db, h5_file, args.record_id, args.metric
        )
        
        if embeddings.size == 0:
            print("No embeddings extracted. Exiting.")
            sys.exit(1)
        
        # Save to .npy file
        print(f"\nSaving embeddings to: {args.output_path}")
        np.save(args.output_path, embeddings)
        
        print(f"✓ Successfully saved {embeddings.shape[0]} protein embeddings")
        print(f"  Shape: {embeddings.shape}")
        print(f"  Dtype: {embeddings.dtype}")
    
    # Close database
    db.close()
    print("\nDone!")


if __name__ == "__main__":
    main()