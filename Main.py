import requests
import pandas as pd
import duckdb
from datetime import datetime
from pathlib import Path


# Recherche automatique de toutes les bases de données dans le dossier data
data_dir = Path("data")
if not data_dir.exists():
    print("[ERREUR] Le dossier 'data' n'existe pas")
    exit(1)

db_files = sorted(data_dir.glob("*.db"))

if not db_files:
    print("[ERREUR] Aucune base de données (.db) trouvée dans le dossier 'data'")
    exit(1)

print(f"Fichiers .db trouvés : {len(db_files)}")
for db in db_files:
    print(f"  - {db.name}")

# Parcourir automatiquement toutes les bases de données
for db_file in db_files:
    con = duckdb.connect(str(db_file))
    print(f"\n{'='*50}")
    print(f"Base de données: {db_file}")
    print(f"{'='*50}")
    
    # Afficher toutes les tables dans la base de données
    df = con.execute("SHOW TABLES").fetchdf()
    print(f"\nTables disponibles: {df['name'].tolist()}")
    
    # Parcourir automatiquement toutes les tables
    for table_name in df["name"].tolist():
        print(f"\n[OK] Table '{table_name}' trouvée")
        
        # Décrire la structure de la table
        df_describe = con.execute(f"DESCRIBE {table_name}").fetchdf()
        print(df_describe)
        
        # Afficher le nombre de lignes
        count = con.execute(f"SELECT COUNT(*) as total FROM {table_name}").fetchdf()
        print(f"\nNombre de lignes : {count['total'].iloc[0]}")
        
        # Afficher un aperçu des données (5 premières lignes)
        print("\nAperçu des données :")
        df_preview = con.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
        print(df_preview)
    
    con.close() 


