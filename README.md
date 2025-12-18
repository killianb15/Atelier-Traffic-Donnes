# Atelier Traffic Données - Bordeaux

Ce projet a pour objectif de collecter, analyser et enrichir des données de trafic routier de Bordeaux avec des informations touristiques.

## Table des matières

- [Structure du projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Description des scripts](#description-des-scripts)
- [Fonctionnalités avancées](#fonctionnalités-avancées)
- [Aspects légaux du scraping](#aspects-légaux-du-scraping)

## Structure du projet

```
Atelier-Traffic-Donnes/
│
├── data/                           # Dossier contenant les bases de données (ignoré par git)
│   ├── .gitkeep                    # Fichier pour conserver la structure du dossier
│   ├── rocade_bordeaux_YYYYMMDD_HHMMSS.db    # Bases de données trafic/météo avec historisation
│   ├── scraping_YYYYMMDD_HHMMSS.db           # Bases de données événements avec historisation
│   └── *.parquet                   # Fichiers Parquet (si conversion effectuée)
│
├── 1activiter.py                   # Atelier 1 - Collecte de données open data
├── 2activiter.py                   # Atelier 2 - Scraping d'événements avec détails (Étape 4)
├── Main.py                         # Script principal de vérification des données
├── inspect_databases.py            # Script d'inspection détaillée des bases de données
├── convert_to_parquet.py           # Script de conversion DuckDB vers Parquet
├── requirements.txt                # Dépendances Python du projet
├── .gitignore                      # Fichiers à exclure du versioning
└── README.md                       # Ce fichier
```

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Connexion Internet pour l'installation des dépendances et la collecte de données

## Installation

### 1. Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
cd Atelier-Traffic-Donnes
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :
- `requests` : pour les requêtes HTTP
- `pandas` : pour la manipulation de données
- `duckdb` : pour la base de données embarquée
- `beautifulsoup4` : pour le parsing HTML (scraping)

## Utilisation

### Atelier 1 - Collecte de données open data

Ce script récupère des données de trafic et météo depuis des sources publiques :

```bash
python 1activiter.py
```

**Sources de données :**
- **Données de trafic** : Bordeaux Métropole Open Data
- **Données météo** : Open-Meteo API (gratuite, sans clé)
- **Données d'équipements publics** : Bordeaux Métropole Open Data

**Fonctionnalités :**
- Historisation automatique avec timestamp dans le nom du fichier
- Ajout d'une colonne `date_import` dans chaque table
- Gestion des erreurs et messages informatifs

**Exemple de sortie :**
```
rocade_bordeaux_20241218_143025.db
```

### Atelier 2 - Scraping d'événements touristiques (avec Étape 4)

Ce script collecte des informations détaillées sur les événements touristiques :

```bash
python 2activiter.py
```

**Données collectées - Liste initiale :**
- Titre de l'événement
- Date
- Lien vers la page détaillée
- Image associée

**Données collectées - Détails (Étape 4) :**
- Description complète
- Lieu (adresse)
- Horaires
- Prix
- Catégorie

**Fonctionnalités :**
- Suivi automatique des liens pour extraction des détails
- Respect du serveur avec pause entre les requêtes (1 seconde)
- Historisation avec timestamp
- Gestion des erreurs et timeouts
- Messages de progression

### Vérification des données

Pour afficher un aperçu des données collectées :

```bash
python Main.py
```

Ce script :
- Scanne automatiquement tous les fichiers `.db` dans le dossier `data/`
- Affiche la liste des tables disponibles
- Affiche la structure de chaque table
- Affiche le nombre de lignes
- Affiche un aperçu des 5 premières lignes

### Inspection détaillée des bases de données

Pour une inspection complète de toutes les tables et colonnes :

```bash
python inspect_databases.py
```

Ce script affiche :
- Liste de tous les fichiers `.db` trouvés
- Pour chaque base de données : nom, taille
- Pour chaque table : nombre de lignes
- Pour chaque colonne : nom, type, contraintes, exemples de valeurs

### Conversion en format Parquet

Pour convertir toutes les bases de données en format Parquet :

```bash
python convert_to_parquet.py
```

Ce script :
- Scanne automatiquement tous les fichiers `.db`
- Convertit chaque table en fichier `.parquet` séparé
- Affiche la taille de chaque fichier créé
- Conserve les fichiers `.db` originaux

**Avantages du format Parquet :**
- Réduction de la taille des fichiers
- Lecture plus rapide pour les analyses columnaires
- Compatible avec de nombreux outils d'analyse de données

## Description des scripts

### `1activiter.py`
- Télécharge des datasets CSV depuis des sources open data
- Utilise l'API Open-Meteo pour les données météo de Bordeaux
- Crée une base de données DuckDB avec historisation (`rocade_bordeaux_YYYYMMDD_HHMMSS.db`)
- Ajoute une colonne `date_import` à chaque table
- Gère les erreurs de téléchargement

### `2activiter.py`
- Scrape la page agenda du site touristique
- **Étape 4 complétée** : Suit automatiquement les liens pour obtenir les détails
- Extrait les informations complètes des événements
- Pause d'1 seconde entre chaque requête (respect du serveur)
- Stocke les résultats dans une base DuckDB avec historisation (`scraping_YYYYMMDD_HHMMSS.db`)
- Gestion des timeouts et erreurs réseau

### `Main.py`
- Scanne automatiquement tous les fichiers `.db` du dossier `data/`
- Se connecte à chaque base de données trouvée
- Affiche la structure complète de toutes les tables
- Présente le nombre de lignes et un aperçu des données

### `inspect_databases.py`
- Inspection détaillée de toutes les bases de données
- Affiche la structure complète de chaque table
- Affiche des exemples de valeurs pour chaque colonne
- Fournit des statistiques sur chaque base de données

### `convert_to_parquet.py`
- Conversion automatique de toutes les bases DuckDB en format Parquet
- Recherche automatique de tous les fichiers `.db`
- Crée un fichier `.parquet` pour chaque table
- Affiche un récapitulatif des fichiers créés avec leur taille

## Fonctionnalités avancées

### Historisation automatique

Tous les scripts de collecte ajoutent automatiquement :
1. **Timestamp dans le nom du fichier** : `nom_YYYYMMDD_HHMMSS.db`
2. **Colonne date_import** : Enregistre la date et l'heure d'importation de chaque ligne

Cela permet de :
- Conserver plusieurs versions des données
- Suivre l'évolution des données dans le temps
- Comparer différentes collectes

### Format Parquet

Le format Parquet offre :
- **Stockage columnaire** optimisé
- **Compression** automatique des données
- **Lecture rapide** pour les analyses
- **Compatibilité** avec pandas, DuckDB, Apache Spark, etc.

### Inspection automatique

Les scripts `Main.py` et `inspect_databases.py` :
- Ne nécessitent aucune configuration
- Trouvent automatiquement toutes les bases de données
- S'adaptent à n'importe quelle structure de table

## Aspects légaux du scraping

Dans le cadre de ce projet, nous respectons les limites suivantes pour minimiser les risques juridiques :

### Limites imposées :

1. **Respect du fichier robots.txt**
   - Vérification systématique des directives du site

2. **Limitation de la fréquence des requêtes**
   - Délai d'1 seconde entre chaque requête
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

- Lecture préalable des conditions d'utilisation du site
- Pas de contournement de mesures de protection
- Stockage anonymisé (remplacement des URLs réelles par des exemples)
- Pas d'impact sur les performances du site source
- Gestion des erreurs et timeouts pour éviter la surcharge
- Pause entre les requêtes pour respecter le serveur

## Structure des données

### Table `trafic` (rocade_bordeaux_*.db)
- Données de circulation de Bordeaux Métropole
- Colonne `date_import` pour l'historisation

### Table `meteo` (rocade_bordeaux_*.db)
- Données météo horaires de Bordeaux (Open-Meteo)
- Paramètres : température, précipitations, vent, humidité
- Colonne `date_import` pour l'historisation

### Table `equipements_publics` (rocade_bordeaux_*.db)
- Équipements publics de Bordeaux Métropole
- Colonne `date_import` pour l'historisation

### Table `events` (scraping_*.db)
Colonnes :
- `link` : URL de l'événement
- `title` : Titre de l'événement
- `date` : Date de l'événement
- `image_src` : URL de l'image
- `description` : Description complète (Étape 4)
- `lieu` : Lieu de l'événement (Étape 4)
- `horaires` : Horaires de l'événement (Étape 4)
- `prix` : Prix d'entrée (Étape 4)
- `categorie` : Catégorie de l'événement (Étape 4)
- `date_import` : Date d'importation

## Contribution

Ce projet est réalisé dans un cadre pédagogique. Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.

## Licence

Projet éducatif - Usage académique uniquement

---

**Date :** Décembre 2024  
**Formation :** Atelier Traffic Données  
**Version :** 2.0 (avec historisation, Parquet, et Étape 4)
