import sqlite3
import csv
import pandas as pd

def connect(db_route):
    conn = sqlite3.connect(db_route)
    cursor = conn.cursor()
    return cursor, conn

def extract(cursor, conn):
    results = []
    with open("csv for gnomad.csv", "r", encoding="utf-8-sig") as f:
        targets = csv.DictReader(f)
        for row in targets:
            # Use parameterized queries to prevent SQL injection
            query = "SELECT * FROM revel WHERE chr = ? AND grch38_pos = ? AND ref_nt = ? AND alt_nt = ?"
            cursor.execute(query, (row['Chromosome'], row['Coordinates'], row['Reference'], row['alt']))
            result = cursor.fetchone()  # Assuming you expect only one row per query
            if result:
                results.append(result)
                print(result)  # Do something with the result
        conn.close()
        df_results = pd.DataFrame(results, columns=["Index_Number","Chr", "Hg19_Pos", "Grch38_Pos", "Ref_Nt", "Alt_Nt","Ref_aa","Alt_aa","Revel_Score"])
        df_results.to_csv("revel_scores.csv", index=False)

cursor, conn = connect("revel.db")
extract(cursor, conn)

