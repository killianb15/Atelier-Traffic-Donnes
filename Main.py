import requests
import pandas as pd
import duckdb
from datetime import datetime
from pathlib import Path


#select des databases dans le dossier data
db_files = [f for f in Path("data").glob("*.db")]
for db_file in db_files:
    con = duckdb.connect(db_file)
    print(f"Base de données: {db_file}")
    #différentes tables dans la base de données
    df = con.execute("Show tables").fetchdf()
    print(df)


    df = con.execute("SELECT * FROM trafic").fetchdf()
    print(df)
    con.close() 

