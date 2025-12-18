import requests
import pandas as pd
import duckdb
from datetime import datetime
from pathlib import Path


# Select des databases dans le dossier data
db_files = [f for f in Path("data").glob("*.db")]
for db_file in db_files:
    con = duckdb.connect(str(db_file))
    print(f"\n{'='*50}")
    print(f"Base de données: {db_file}")
    print(f"{'='*50}")
    
    # Afficher toutes les tables dans la base de données
    df = con.execute("SHOW TABLES").fetchdf()
    print(f"\nTables disponibles: {df['name'].tolist()}")
    
    # Vérifier et décrire la table 'trafic' si elle existe
    if "trafic" in df["name"].values:
        print("\n✓ Table 'trafic' trouvée")
        df_trafic = con.execute("DESCRIBE trafic").fetchdf()
        print(df_trafic)
    
    # Vérifier et décrire la table 'events' si elle existe
    if "events" in df["name"].values:
        print("\n✓ Table 'events' trouvée")
        df_events = con.execute("DESCRIBE events").fetchdf()
        print(df_events)
        df_events = con.execute("SELECT title, date FROM events").fetchdf()
        print(df_events)
    con.close() 


