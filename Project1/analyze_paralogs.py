#!/usr/bin/env python3
"""
Analyze protein clustering results to identify paralogs.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def parse_faa(faa_file):
    """
    Parse protein FASTA file to extract protein IDs and names.
    Returns dict: {protein_id: protein_name}
    """
    protein_names = {}
    
    with open(faa_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                # Example header: >ABCDEF_00001 hypothetical protein
                parts = line[1:].strip().split(None, 1)
                protein_id = parts[0]
                protein_name = parts[1] if len(parts) > 1 else "unknown"
                protein_names[protein_id] = protein_name
    
    return protein_names


def analyze_clusters(cluster_file, protein_names):
    """
    Analyze clustering results to find paralogs.
    Returns DataFrame with protein_id, protein_name, copy_number
    """
    # Read clustering results
    df = pd.read_csv(cluster_file, sep='\t', header=None, 
                     names=['cluster_id', 'protein_id'])
    
    # Count cluster sizes
    cluster_sizes = df.groupby('cluster_id').size().reset_index(name='copy_number')
    
    # Filter for paralogs (clusters with >1 member)
    paralogs = cluster_sizes[cluster_sizes['copy_number'] > 1].copy()
    
    # Add protein names
    paralogs['protein_name'] = paralogs['cluster_id'].map(protein_names)
    
    # Rename cluster_id to protein_id for output
    paralogs = paralogs.rename(columns={'cluster_id': 'protein_id'})
    
    # Sort by copy number descending
    paralogs = paralogs.sort_values('copy_number', ascending=False)
    
    return paralogs


def create_visualization(paralogs_df, output_png, top_n=10):
    """
    Create bar plot of top N paralogs.
    """
    # Get top N
    top_paralogs = paralogs_df.head(top_n)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create bar plot
    bars = ax.barh(range(len(top_paralogs)), top_paralogs['copy_number'])
    
    # Customize
    ax.set_yticks(range(len(top_paralogs)))
    ax.set_yticklabels(top_paralogs['protein_name'], fontsize=10)
    ax.set_xlabel('Copy Number', fontsize=12)
    ax.set_title(f'Top {top_n} Most Frequent Paralogs', fontsize=14, fontweight='bold')
    ax.invert_yaxis()  # Highest at top
    
    # Add value labels on bars
    for i, (idx, row) in enumerate(top_paralogs.iterrows()):
        ax.text(row['copy_number'] + 0.1, i, str(row['copy_number']), 
                va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    print(f"Visualization saved: {output_png}")


def main():
    parser = argparse.ArgumentParser(description='Analyze protein paralogs')
    parser.add_argument('--faa', required=True, help='Protein FASTA file')
    parser.add_argument('--cluster', required=True, help='Cluster TSV file')
    parser.add_argument('--output-tsv', required=True, help='Output TSV file')
    parser.add_argument('--output-png', required=True, help='Output PNG file')
    parser.add_argument('--top-n', type=int, default=10, help='Top N paralogs to plot')
    
    args = parser.parse_args()
    
    print("=== Paralog Analysis ===")
    print(f"Protein file: {args.faa}")
    print(f"Cluster file: {args.cluster}")
    
    # Parse protein names
    print("\nParsing protein names...")
    protein_names = parse_faa(args.faa)
    print(f"Found {len(protein_names)} proteins")
    
    # Analyze clusters
    print("\nAnalyzing clusters...")
    paralogs = analyze_clusters(args.cluster, protein_names)
    print(f"Found {len(paralogs)} paralogous proteins")
    
    # Save TSV
    print(f"\nSaving results to: {args.output_tsv}")
    paralogs.to_csv(args.output_tsv, sep='\t', index=False)
    
    # Create visualization
    print(f"\nCreating visualization...")
    create_visualization(paralogs, args.output_png, args.top_n)
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total paralogous proteins: {len(paralogs)}")
    print(f"Highest copy number: {paralogs['copy_number'].max()}")
    print(f"\nTop 5 paralogs:")
    print(paralogs[['protein_id', 'protein_name', 'copy_number']].head())
    
    print("\nDone!")


if __name__ == "__main__":
    main()
