import duckdb
from pathlib import Path

def convert_db_to_parquet():
    """Convertit toutes les tables des bases DuckDB en format Parquet"""
    
    # Liste tous les fichiers .db dans le dossier data
    data_dir = Path("data")
    if not data_dir.exists():
        print("[ERREUR] Le dossier 'data' n'existe pas")
        return
    
    db_files = sorted(data_dir.glob("*.db"))
    
    if not db_files:
        print("[ERREUR] Aucune base de données (.db) trouvée dans le dossier 'data'")
        return
    
    print(f"Recherche automatique dans le dossier 'data'...")
    print(f"Fichiers .db trouvés : {len(db_files)}")
    for db in db_files:
        print(f"  - {db.name}")
    print("\nConversion des bases de données en format Parquet...")
    print("=" * 60)
    
    total_tables = 0
    
    for db_file in db_files:
        print(f"\nTraitement de: {db_file.name}")
        
        try:
            # Connexion à la base de données
            con = duckdb.connect(str(db_file), read_only=True)
            
            # Récupérer toutes les tables
            tables_df = con.execute("SHOW TABLES").fetchdf()
            tables = tables_df['name'].tolist()
            
            if not tables:
                print(f"   [ATTENTION] Aucune table trouvée dans {db_file.name}")
                con.close()
                continue
            
            print(f"   Tables trouvées: {', '.join(tables)}")
            
            # Exporter chaque table en Parquet
            for table in tables:
                # Nom du fichier Parquet basé sur la base et la table
                db_name = db_file.stem  # nom sans extension
                parquet_file = f"data/{db_name}_{table}.parquet"
                
                # Exporter en Parquet
                con.execute(f"COPY {table} TO '{parquet_file}' (FORMAT PARQUET)")
                
                # Vérifier la taille
                parquet_path = Path(parquet_file)
                if parquet_path.exists():
                    size_kb = parquet_path.stat().st_size / 1024
                    print(f"   [OK] {table} -> {parquet_file} ({size_kb:.2f} KB)")
                    total_tables += 1
                else:
                    print(f"   [ERREUR] Erreur lors de la création de {parquet_file}")
            
            con.close()
            
        except Exception as e:
            print(f"   [ERREUR] Erreur: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"[OK] Conversion terminée ! {total_tables} table(s) exportée(s) en Parquet")
    
    # Lister tous les fichiers Parquet créés
    parquet_files = sorted(Path("data").glob("*.parquet"))
    if parquet_files:
        print(f"\nFichiers Parquet disponibles ({len(parquet_files)}):")
        for pf in parquet_files:
            size_kb = pf.stat().st_size / 1024
            print(f"  - {pf.name} ({size_kb:.2f} KB)")
    
    print("\nPour lire les fichiers Parquet avec DuckDB:")
    print("   con = duckdb.connect()")
    print("   df = con.execute(\"SELECT * FROM 'data/votre_fichier.parquet'\").fetchdf()")

if __name__ == "__main__":
    convert_db_to_parquet()

