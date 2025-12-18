import duckdb
import requests
import os
import tempfile
from pathlib import Path
from datetime import datetime


output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

# Ajouter la date pour l'historisation
date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
db_name = output_dir / f'rocade_bordeaux_{date_str}.db'


if os.path.exists(db_name):
    print(f"La base de données '{db_name}' existe déjà.")

else:
    print(f"Création de la nouvelle base de données '{db_name}'.")


conn = duckdb.connect(str(db_name))
print(f"Connecté à la base de données '{db_name}'.")

def load_data_from_url(url, table_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
            tmpfile.write(response.content)
            tmpfile_path = tmpfile.name
        
        # Ajouter une colonne de date d'import pour l'historisation
        import_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *, '{import_date}' AS date_import
            FROM read_csv_auto('{tmpfile_path}', normalize_names=True, ignore_errors=true)
        """)
        print(f"Données chargées avec succès dans la table '{table_name}'.")
    except requests.RequestException as e:
        print(f"Erreur lors du chargement des données pour {table_name}: {e}")
    except duckdb.Error as e:
        print(f"Erreur DuckDB lors du chargement des données pour {table_name}: {e}")


traffic_url = "https://opendata.bordeaux-example.fr/explore/dataset/ci_trafi_l/download/?format=csv"
load_data_from_url(traffic_url, "trafic")

weather_url = "https://donneespubliques.example.fr/donnees_libres/Txt/Synop/synop.2023.csv.gz"
load_data_from_url(weather_url, "meteo")


roadworks_url = "https://www.rocadebordeaux-example.com"
load_data_from_url(roadworks_url, "travaux_routiers")


tables = conn.execute("SHOW TABLES").fetchall()
print("Tables dans la base de données:")
for table in tables:
    print(f"- {table[0]}")


conn.close()
print("Connexion à la base de données fermée.")