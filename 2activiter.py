import requests
from bs4 import BeautifulSoup
import duckdb
from pathlib import Path
from datetime import datetime
import time

# Créer le dossier data s'il n'existe pas
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

# URL de la page à scraper
url = "https://www.bordeaux-example.com/agenda.html"
base_url = "https://www.bordeaux-example.com"

# Fonction pour récupérer le contenu de la page
def get_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[ERREUR] Impossible de récupérer {url}: {e}")
        return None

# ETAPE 4 : Fonction pour extraire les détails d'une page d'événement
def get_event_details(event_url):
    """Suit le lien d'un événement pour obtenir les détails complets"""
    
    # Construire l'URL complète si nécessaire
    if event_url and not event_url.startswith('http'):
        event_url = base_url + event_url
    
    print(f"  --> Récupération des détails depuis: {event_url}")
    
    content = get_page_content(event_url)
    if not content:
        return None
    
    soup = BeautifulSoup(content, 'html.parser')
    
    details = {
        'description': None,
        'lieu': None,
        'horaires': None,
        'prix': None,
        'categorie': None
    }
    
    # Essayer d'extraire la description
    desc_element = soup.find('div', class_='description') or soup.find('p', class_='event-description')
    if desc_element:
        details['description'] = desc_element.get_text(strip=True)[:500]  # Limiter à 500 caractères
    
    # Essayer d'extraire le lieu
    lieu_element = soup.find('div', class_='location') or soup.find('span', class_='lieu')
    if lieu_element:
        details['lieu'] = lieu_element.get_text(strip=True)
    
    # Essayer d'extraire les horaires
    horaires_element = soup.find('div', class_='schedule') or soup.find('span', class_='horaires')
    if horaires_element:
        details['horaires'] = horaires_element.get_text(strip=True)
    
    # Essayer d'extraire le prix
    prix_element = soup.find('div', class_='price') or soup.find('span', class_='prix')
    if prix_element:
        details['prix'] = prix_element.get_text(strip=True)
    
    # Essayer d'extraire la catégorie
    cat_element = soup.find('div', class_='category') or soup.find('span', class_='categorie')
    if cat_element:
        details['categorie'] = cat_element.get_text(strip=True)
    
    return details

# Fonction pour extraire les données de la page principale
def extract_data(content):
    soup = BeautifulSoup(content, 'html.parser')

    agenda_wrapper = soup.find_all(class_="ListSit-wrapper")
    data = []

    if agenda_wrapper:

        for wrapper in agenda_wrapper:
            event_cards = wrapper.find_all("a", class_="Card")

            print(f"\n[OK] {len(event_cards)} événements trouvés\n")

            for i, card in enumerate(event_cards, 1):
                link = card.get('href')
                title = card.find("p", class_="Card-title").text.strip() if card.find("p", class_="Card-title") else None
                date = card.find("p", class_="Card-label").text.strip() if card.find("p", class_="Card-label") else None
                image = card.find("div", class_="Card-img").find("img") if card.find("div", class_="Card-img") else None
                image_src = image.get("src") if image else None
                
                print(f"[{i}/{len(event_cards)}] {title}")
                
                # ETAPE 4 : Suivre le lien pour obtenir les détails
                details = get_event_details(link) if link else None
                
                # Ajouter les données avec les détails
                data.append((
                    link,
                    title,
                    date,
                    image_src,
                    details['description'] if details else None,
                    details['lieu'] if details else None,
                    details['horaires'] if details else None,
                    details['prix'] if details else None,
                    details['categorie'] if details else None
                ))
                
                # Respecter le serveur : pause entre chaque requête
                time.sleep(1)
                
                print("-" * 80)
    
    return data

# Fonction pour stocker les données dans DuckDB avec détails (ETAPE 4)
def store_in_duckdb(data):
    # Ajouter la date pour l'historisation
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    db_path = output_dir / f'scraping_{date_str}.db'
    conn = duckdb.connect(str(db_path))
    
    # Créer la table avec les colonnes de détails (ETAPE 4)
    import_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            link VARCHAR,
            title VARCHAR,
            date VARCHAR,
            image_src VARCHAR,
            description VARCHAR,
            lieu VARCHAR,
            horaires VARCHAR,
            prix VARCHAR,
            categorie VARCHAR,
            date_import VARCHAR
        )
    """)
    
    # Insérer les données avec tous les détails
    import_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_with_import = [
        (link, title, date, image_src, description, lieu, horaires, prix, categorie, import_date) 
        for link, title, date, image_src, description, lieu, horaires, prix, categorie in data
    ]
    
    conn.executemany("""
        INSERT INTO events (link, title, date, image_src, description, lieu, horaires, prix, categorie, date_import)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data_with_import)
    
    conn.close()
    print(f"\n[OK] Base de données créée: {db_path}")
    print(f"[OK] {len(data)} événements avec détails stockés")


def display_data_from_duckdb(db_filename):
    db_path = output_dir / db_filename
    conn = duckdb.connect(str(db_path))
    result = conn.execute("SELECT * FROM events ;").fetchall()
    for row in result:
        print(row)
    conn.close()
10
# Exécuter la vérification
# display_data_from_duckdb()


# Exécution principale
print("=" * 80)
print("ETAPE 4 : SCRAPING AVEC SUIVI DES LIENS")
print("=" * 80)

content = get_page_content(url)
if content:
    data = extract_data(content)
    if data:
        store_in_duckdb(data)
        print("\n" + "=" * 80)
        print("[OK] ETAPE 4 TERMINEE : Données détaillées extraites et stockées")
        print("=" * 80)
    else:
        print("[ATTENTION] Aucune donnée extraite")
else:
    print("[ERREUR] Impossible de récupérer la page principale")