import pandas as pd
from database import engine

CSV_PATH = "data/NRI_Table_CensusTracts.csv"
CHUNK_SIZE = 10000

total_rows = 0

for chunk in pd.read_csv(
    CSV_PATH,
    usecols=["TRACTFIPS", "RISK_SCORE"],
    dtype={"TRACTFIPS": str},
    chunksize=CHUNK_SIZE,
):
    chunk = chunk.rename(columns={"TRACTFIPS": "census_tract", "RISK_SCORE": "risk_score"})
    chunk.to_sql("fema_risk", engine, if_exists="append", index=False)
    total_rows += len(chunk)
    print(f"Loaded {total_rows} rows so far...")

print("Done.")

