# Atelier Traffic Données - Bordeaux

Ce projet a pour objectif de collecter, analyser et enrichir des données de trafic routier de Bordeaux avec des informations touristiques.

## 📋 Table des matières

- [Structure du projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Description des scripts](#description-des-scripts)
- [Aspects légaux du scraping](#aspects-légaux-du-scraping)

## 📁 Structure du projet

```
Atelier-Traffic-Donnes/
│
├── data/                      # Dossier contenant les bases de données (ignoré par git)
│   ├── .gitkeep              # Fichier pour conserver la structure du dossier
│   ├── rocade_bordeaux.db    # Base de données trafic/météo (généré)
│   └── scraping.db           # Base de données événements touristiques (généré)
│
├── scripts/                   # Scripts d'ingestion et de traitement
│   └── .gitkeep              # Fichier pour conserver la structure du dossier
│
├── 1activiter.py             # Atelier 1 - Collecte de données open data
├── 2activiter.py             # Atelier 2 - Scraping d'événements touristiques
├── Main.py                   # Script principal de vérification des données
├── requirements.txt          # Dépendances Python du projet
├── .gitignore               # Fichiers à exclure du versioning
└── README.md                # Ce fichier
```

## 🔧 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Connexion Internet pour l'installation des dépendances et la collecte de données

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd Atelier-Traffic-Donnes
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :
- `requests` : pour les requêtes HTTP
- `pandas` : pour la manipulation de données
- `duckdb` : pour la base de données embarquée
- `beautifulsoup4` : pour le parsing HTML (scraping)

## 📊 Utilisation

### Atelier 1 - Collecte de données open data

Ce script récupère des données de trafic et météo depuis des sources publiques :

```bash
python 1activiter.py
```

**Sources de données :**
- Données de trafic : Bordeaux Métropole Open Data
- Données météo : Météo France
- Données travaux routiers : Rocade Bordeaux

### Atelier 2 - Scraping d'événements touristiques

Ce script collecte des informations sur les événements touristiques :

```bash
python 2activiter.py
```

**Données collectées :**
- Titre de l'événement
- Date
- Lien vers la page détaillée
- Image associée

### Vérification des données

Pour afficher un aperçu des données collectées :

```bash
python Main.py
```

## 📝 Description des scripts

### `1activiter.py`
- Télécharge des datasets CSV depuis des sources open data
- Crée une base de données DuckDB (`rocade_bordeaux.db`)
- Stocke les données de trafic, météo et travaux routiers

### `2activiter.py`
- Scrape la page agenda du site touristique
- Extrait les informations des événements
- Stocke les résultats dans une base DuckDB (`scraping.db`)

### `Main.py`
- Se connecte aux bases de données créées
- Affiche la structure des tables
- Présente un échantillon des données collectées

## ⚖️ Aspects légaux du scraping

Dans le cadre de ce projet, nous respectons les limites suivantes pour minimiser les risques juridiques :

### Limites imposées :

1. **Respect du fichier robots.txt**
   - Vérification systématique des directives du site

2. **Limitation de la fréquence des requêtes**
   - Délai entre les requêtes pour éviter la surcharge du serveur
   - Pas d'utilisation de requêtes parallèles agressives

3. **Identification claire**
   - User-Agent approprié pour identifier notre scraper
   - Pas d'usurpation d'identité

4. **Usage personnel et éducatif uniquement**
   - Les données collectées sont utilisées à des fins pédagogiques
   - Pas de revente ou redistribution des données

5. **Respect de la propriété intellectuelle**
   - Pas de copie intégrale du contenu du site
   - Citation de la source des données

6. **Volume limité**
   - Collecte uniquement des données nécessaires au projet
   - Pas de scraping massif de l'intégralité du site

### Bonnes pratiques appliquées :

- ✅ Lecture préalable des conditions d'utilisation du site
- ✅ Pas de contournement de mesures de protection
- ✅ Stockage anonymisé (remplacement des URLs réelles par des exemples)
- ✅ Pas d'impact sur les performances du site source

## 🤝 Contribution

Ce projet est réalisé dans un cadre pédagogique. Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.

## 📄 Licence

Projet éducatif - Usage académique uniquement

---

**Auteur :** [Votre nom]  
**Date :** Décembre 2025  
**Formation :** Atelier Traffic Données

