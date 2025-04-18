# Base de Données et Analyse des Crashs Aériens

Ce projet vise à créer une base de données complète des crashs aériens et à réaliser des analyses statistiques avancées pour comprendre les facteurs contribuant à ces incidents, avec l'objectif d'améliorer la sécurité aérienne.

## Table des Matières
- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Structure du Projet](#structure-du-projet)
- [Sources de Données](#sources-de-données)
- [Extraction et Traitement des Données](#extraction-et-traitement-des-données)
- [Analyse et Modélisation](#analyse-et-modélisation)
- [Visualisations](#visualisations)
- [Usage et Exemples](#usage-et-exemples)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Introduction

Le transport aérien est l'un des modes de transport les plus sûrs, mais des incidents et accidents se produisent encore. Ce projet compile et analyse les données des crashs aériens pour identifier les tendances, les causes communes et les facteurs de risque. Notre objectif est de contribuer à la recherche sur la sécurité aérienne en fournissant une base de données complète et des analyses statistiques robustes.

## Fonctionnalités

- **Extraction de données** : Collecte automatisée depuis des sources officielles (NTSB, ASN, BEA, etc.)
- **Base de données** : Structure PostgreSQL optimisée pour stocker et interroger les données des accidents
- **Analyse exploratoire** : Notebooks Jupyter pour l'analyse visuelle et statistique
- **Modélisation prédictive** : Algorithmes ML pour identifier les facteurs de risque
- **Visualisations** : Graphiques, cartes et tableaux de bord interactifs
- **API** : Accès programmatique aux données et aux résultats d'analyse

## Installation

### Prérequis
- Python 3.8+
- PostgreSQL 12+
- Git

### Étapes d'installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-nom/crash-analysis-project.git
cd crash-analysis-project

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditez le fichier .env avec vos paramètres

# Initialiser la base de données
psql -U your_user -d your_db -f schema.sql
```

## Structure du Projet

Le projet est organisé selon la structure suivante :
```
crash_analysis_project/
├── data/               # Données brutes et traitées
├── models/             # Modèles entraînés
├── notebooks/          # Jupyter notebooks
├── results/            # Résultats d'analyse
├── src/                # Code source
├── tests/              # Tests unitaires
└── ...                 # Fichiers de configuration
```

## Sources de Données

Les données sont extraites des sources suivantes :
- [National Transportation Safety Board (NTSB)](https://www.ntsb.gov/Pages/AviationQueryv2.aspx)
- [Aviation Safety Network (ASN)](https://asn.flightsafety.org/)
- [Bureau d'Enquêtes et d'Analyses (BEA)](https://www.bea.aero/en/investigation-reports/list-of-reports)
- [Air Accidents Investigation Branch (AAIB)](https://www.gov.uk/government/organisations/air-accidents-investigation-branch)
- Autres agences nationales et internationales

## Extraction et Traitement des Données

Le processus d'extraction et de traitement des données comprend :

1. **Collecte** : Scripts automatisés pour extraire les données des sources officielles
2. **Nettoyage** : Traitement des valeurs manquantes, correction des formats, dédoublonnage
3. **Transformation** : Normalisation, standardisation et création de nouvelles caractéristiques
4. **Chargement** : Importation dans la base de données PostgreSQL

## Analyse et Modélisation

Notre approche analytique comprend :

- **Analyse exploratoire** : Identification des tendances temporelles et géographiques
- **Analyse statistique** : Tests d'hypothèses et corrélations entre facteurs
- **Modélisation prédictive** : Utilisation d'algorithmes ML pour identifier les facteurs de risque
  - Régression logistique
  - Forêts aléatoires
  - Gradient boosting
  - SVM

## Visualisations

Le projet inclut diverses visualisations :
- Distribution temporelle des accidents
- Cartographie mondiale des incidents
- Analyse par type d'avion et d'opérateur
- Facteurs contribuant aux accidents
- Tendances de sécurité au fil du temps

## Usage et Exemples

### Extraction des données
```bash
python src/data/extract_data.py
```

### Entraînement des modèles
```bash
python src/models/train_model.py
```

### Exécution d'une analyse complète
```bash
python src/main.py --full-analysis
```

## Contribuer

Les contributions sont les bienvenues ! Voici comment vous pouvez participer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

Veuillez consulter le fichier CONTRIBUTING.md pour les directives détaillées.

## Licence

Ce projet est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
