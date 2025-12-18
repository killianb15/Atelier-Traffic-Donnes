import duckdb
from pathlib import Path

def inspect_all_databases():
    """Affiche toutes les tables et colonnes de toutes les bases de données dans le dossier data"""
    
    # Recherche automatique de toutes les bases de données
    data_dir = Path("data")
    if not data_dir.exists():
        print("[ERREUR] Le dossier 'data' n'existe pas")
        return
    
    db_files = sorted(data_dir.glob("*.db"))
    
    if not db_files:
        print("[ERREUR] Aucune base de données (.db) trouvée dans le dossier 'data'")
        return
    
    print("=" * 80)
    print(f"INSPECTION DES BASES DE DONNEES")
    print(f"Nombre de fichiers .db trouvés : {len(db_files)}")
    print("=" * 80)
    
    # Parcourir chaque base de données
    for db_file in db_files:
        print(f"\n{'#' * 80}")
        print(f"# BASE DE DONNEES : {db_file.name}")
        print(f"# Chemin : {db_file}")
        print(f"# Taille : {db_file.stat().st_size / 1024:.2f} KB")
        print(f"{'#' * 80}\n")
        
        try:
            # Connexion à la base de données
            con = duckdb.connect(str(db_file), read_only=True)
            
            # Récupérer toutes les tables
            tables_df = con.execute("SHOW TABLES").fetchdf()
            tables = tables_df['name'].tolist()
            
            if not tables:
                print("[ATTENTION] Aucune table trouvée dans cette base de données\n")
                con.close()
                continue
            
            print(f"Nombre de tables : {len(tables)}\n")
            
            # Pour chaque table, afficher la structure
            for i, table in enumerate(tables, 1):
                print(f"\n{'=' * 80}")
                print(f"TABLE {i}/{len(tables)} : {table}")
                print(f"{'=' * 80}")
                
                # Récupérer la structure de la table
                structure_df = con.execute(f"DESCRIBE {table}").fetchdf()
                
                # Récupérer le nombre de lignes
                count_result = con.execute(f"SELECT COUNT(*) as total FROM {table}").fetchdf()
                row_count = count_result['total'].iloc[0]
                
                print(f"\nNombre de lignes : {row_count}")
                print(f"\nStructure de la table :")
                print("-" * 80)
                
                # Afficher chaque colonne avec ses détails
                for idx, row in structure_df.iterrows():
                    col_name = row['column_name']
                    col_type = row['column_type']
                    null = row['null']
                    
                    null_str = "NULL autorisé" if null == 'YES' else "NOT NULL"
                    print(f"  {idx+1}. {col_name}")
                    print(f"     Type: {col_type}")
                    print(f"     Contrainte: {null_str}")
                    
                    # Afficher un échantillon de valeurs (5 premières valeurs uniques)
                    try:
                        sample_df = con.execute(f"""
                            SELECT DISTINCT {col_name} 
                            FROM {table} 
                            WHERE {col_name} IS NOT NULL 
                            LIMIT 5
                        """).fetchdf()
                        
                        if not sample_df.empty:
                            values = sample_df[col_name].tolist()
                            values_str = ", ".join([str(v)[:50] for v in values])
                            print(f"     Exemples: {values_str}")
                    except:
                        pass
                    
                    print()
            
            con.close()
            
        except Exception as e:
            print(f"[ERREUR] Erreur lors de l'inspection de {db_file.name}: {str(e)}\n")
    
    print("\n" + "=" * 80)
    print("INSPECTION TERMINEE")
    print("=" * 80)

if __name__ == "__main__":
    inspect_all_databases()

