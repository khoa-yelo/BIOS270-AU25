import Bio
from Bio import SeqIO


def read_fasta(file_path):
    """Reads a FASTA file and returns a list of sequences."""
    sequences = []
    for record in SeqIO.parse(file_path, "fasta"):
        sequences.append(str(record.seq))
    return sequences


if __name__ == "__main__":
    fasta_file = "example.fasta"
    sequences = read_fasta(fasta_file)
    for seq in sequences:
        print(seq)
