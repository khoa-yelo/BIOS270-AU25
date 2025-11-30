import sqlite3
import pandas as pd
import argparse
import tqdm
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default="all_protein_ids.txt")
    args = parser.parse_args()
    return args
class BacteriaDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def get_all_record_ids(self):
        #TODO: write the query to get all unique record_id from the gff table
        query = #TODO
        df = self.query(query)
        return df["record_id"].dropna().tolist()
    
    def get_protein_ids_from_record_id(self, record_id):
        #TODO: write function to return list of protein_ids for a given record_id
        query = #TODO
        df = self.query(query)
        return df["protein_id"].dropna().tolist()

    def index_record_ids(self):
        query = "CREATE INDEX IF NOT EXISTS record_id_index ON gff(record_id)"
        self.conn.execute(query)

    def query(self, query):
        return pd.read_sql(query, self.conn)
        
    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()

def write_protein_ids(protein_ids, output_path):
    with open(output_path, "w") as f:
        f.write("\n".join(protein_ids))

if __name__ == "__main__":
    args = parse_args()
    db = BacteriaDatabase(args.database_path)
    print("Total number of record ids: ", len(db.get_all_record_ids()))
    all_protein_ids = []
    # db.index_record_ids()
    tic = time.time()
    for i, record_id in enumerate(db.get_all_record_ids()):
        protein_ids = db.get_protein_ids_from_record_id(record_id)
        all_protein_ids.extend(protein_ids)
        if i % 10 == 0:
            print(f"Processed {i} record ids in {time.time() - tic} seconds")
    toc = time.time()
    print(f"Total time: {toc - tic}")
    print("Total number of protein ids: ", len(all_protein_ids))
    write_protein_ids(all_protein_ids, args.output_path)
    db.close()
