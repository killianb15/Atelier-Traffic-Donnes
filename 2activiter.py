import requests
from bs4 import BeautifulSoup
import duckdb
from pathlib import Path

# Créer le dossier data s'il n'existe pas
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

# URL de la page à scraper
url = "https://www.bordeaux-tourisme.com/agenda.html"

# Fonction pour récupérer le contenu de la page
def get_page_content(url):
    response = requests.get(url)
    return response.text

# Fonction pour extraire les données de la page
def extract_data(content):
    soup = BeautifulSoup(content, 'html.parser')

    agenda_wrapper = soup.find_all(class_="ListSit-wrapper")
    data = []

    if agenda_wrapper:

        for wrapper in agenda_wrapper:
            event_cards = wrapper.find_all("a", class_="Card")

            for card in event_cards:
                link = card.get('href')
                title = card.find("p", class_="Card-title").text.strip() #if card.find("p", class_="Card-title") else None
                date = card.find("p", class_="Card-label").text.strip() #if card.find("p", class_="Card-label") else None
                image = card.find("div", class_="Card-img").find("img")
                image_src = image.get("src") if image else None
                
                data.append((link, title, date, image_src))
                if title and date and link:
                    print(f"Titre: {title}")
                    print(f"Date: {date}")
                    print(f"URL: {link}")
                    if image_src:
                        print(f"Image: {image_src}")
                    print("-" * 40)  # Séparateur pour chaque événement
    
    return data

# Fonction pour stocker les données dans DuckDB
def store_in_duckdb(data):
    db_path = output_dir / 'scraping.db'
    conn = duckdb.connect(str(db_path))
    
    # Créer la table si elle n'existe pas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            link VARCHAR,
            title VARCHAR,
            date VARCHAR,
            image_src VARCHAR
        )
    """)
    
    # Insérer les données
    conn.executemany("""
        INSERT INTO events (link, title, date, image_src)
        VALUES (?, ?, ?, ?)
    """, data)
    
    conn.close()


def display_data_from_duckdb():
    db_path = output_dir / 'scraping.db'
    conn = duckdb.connect(str(db_path))
    result = conn.execute("SELECT * FROM events ;").fetchall()
    for row in result:
        print(row)
    conn.close()
10
# Exécuter la vérification
# display_data_from_duckdb()


# Exécution principale
content = get_page_content(url)
data = extract_data(content)
store_in_duckdb(data)

print("Données extraites et stockées avec succès dans DuckDB.")