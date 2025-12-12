#!/usr/bin/env python3
"""
Summarize and visualize protein paralogs from MMseqs2 clustering results.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def parse_faa_headers(faa_file):
    """Extract protein_id -> protein_name mapping from FASTA headers."""
    protein_names = {}
    with open(faa_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                parts = line[1:].strip().split(' ', 1)
                protein_id = parts[0]
                protein_name = parts[1] if len(parts) > 1 else "Unknown"
                protein_names[protein_id] = protein_name
    return protein_names


def parse_clusters(cluster_file):
    """Parse MMseqs2 cluster TSV file."""
    clusters = defaultdict(list)
    with open(cluster_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                cluster_id, protein_id = parts[0], parts[1]
                clusters[cluster_id].append(protein_id)
    return clusters


def find_paralogs(clusters, protein_names):
    """Identify clusters with >1 member (paralogs) and get their info."""
    paralogs = []
    for cluster_id, members in clusters.items():
        copy_number = len(members)
        if copy_number > 1:
            protein_name = protein_names.get(cluster_id, "Unknown")
            paralogs.append({
                'protein_id': cluster_id,
                'protein_name': protein_name,
                'copy_number': copy_number
            })
    return pd.DataFrame(paralogs)


def create_visualization(df, output_prefix, sample_name):
    """Create bar plot of top 10 most frequent paralogs."""
    top_paralogs = df.nlargest(10, 'copy_number')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(range(len(top_paralogs)), top_paralogs['copy_number'], color='steelblue')
    
    labels = [name[:40] + '...' if len(name) > 40 else name
              for name in top_paralogs['protein_name']]
    
    ax.set_yticks(range(len(top_paralogs)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('Copy Number')
    ax.set_title(f'Top 10 Most Frequent Paralogs - {sample_name}')
    
    for i, (bar, val) in enumerate(zip(bars, top_paralogs['copy_number'])):
        ax.text(val + 0.1, i, str(val), va='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_top10_paralogs.png', dpi=150)
    plt.close()
    print(f"Saved visualization: {output_prefix}_top10_paralogs.png")


def main():
    parser = argparse.ArgumentParser(description='Summarize protein paralogs')
    parser.add_argument('--faa', required=True, help='Protein FASTA file (.faa)')
    parser.add_argument('--clusters', required=True, help='MMseqs2 cluster TSV file')
    parser.add_argument('--output', required=True, help='Output prefix')
    parser.add_argument('--sample', default='Sample', help='Sample name for plot title')
    args = parser.parse_args()
    
    print(f"Parsing protein sequences from {args.faa}...")
    protein_names = parse_faa_headers(args.faa)
    print(f"  Found {len(protein_names)} proteins")
    
    print(f"Parsing clusters from {args.clusters}...")
    clusters = parse_clusters(args.clusters)
    print(f"  Found {len(clusters)} clusters")
    
    print("Identifying paralogs (clusters with >1 member)...")
    df = find_paralogs(clusters, protein_names)
    df = df.sort_values('copy_number', ascending=False)
    print(f"  Found {len(df)} paralog families")
    
    tsv_file = f'{args.output}_paralogs.tsv'
    df.to_csv(tsv_file, sep='\t', index=False)
    print(f"Saved summary: {tsv_file}")
    
    if len(df) > 0:
        create_visualization(df, args.output, args.sample)
    else:
        print("No paralogs found - skipping visualization")
    
    print(f"\n=== Summary for {args.sample} ===")
    print(f"Total paralog families: {len(df)}")
    if len(df) > 0:
        print(f"Total duplicated proteins: {df['copy_number'].sum()}")
        print(f"Max copy number: {df['copy_number'].max()}")
        print(f"\nTop 5 paralogs:")
        for _, row in df.head().iterrows():
            print(f"  {row['protein_name'][:50]}: {row['copy_number']} copies")


if __name__ == '__main__':
    main()
