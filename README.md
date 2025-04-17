# Base de Données et Analyse des Crashs Aériens

Ce projet vise à créer une base de données complète des crashs aériens et à réaliser des analyses statistiques et des modèles prédictifs pour comprendre les facteurs contribuant à ces incidents.

## Table des Matières
- [Introduction](#introduction)
- [Sources de Données](#sources-de-données)
- [Schéma de la Base de Données](#schéma-de-la-base-de-données)
- [Extraction des Données](#extraction-des-données)
- [Analyse des Données et Modélisation](#analyse-des-données-et-modélisation)
- [Spécification du Modèle Prédictif](#spécification-du-modèle-prédictif)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Introduction
Le transport aérien reste l'un des modes de transport les plus sûrs, mais des incidents et des accidents se produisent encore. Ce projet vise à créer une base de données détaillée des crashs aériens, à analyser les données pour identifier les tendances et les modèles, et à développer des modèles prédictifs pour mieux comprendre les facteurs qui contribuent à ces accidents.

## Sources de Données
Les principales sources de données pour ce projet sont :
- [National Transportation Safety Board (NTSB)](https://www.ntsb.gov/Pages/AviationQueryv2.aspx)
- [Aviation Safety Network (ASN)](https://asn.flightsafety.org/)
- [Bureau d'Enquêtes et d'Analyses (BEA)](https://www.bea.aero/en/investigation-reports/list-of-reports)
- [Air Accidents Investigation Branch (AAIB)](https://www.gov.uk/government/organisations/air-accidents-investigation-branch)
- [Bundesstelle für Flugunfalluntersuchung (BFU)](https://www.bfu-web.de/EN/Publications/Investigation-Report)
- [Agence de l'Union Européenne pour la Sécurité Aérienne (EASA)](https://www.easa.europa.eu/document-library/accident-reports)

## Schéma de la Base de Données
Le schéma de la base de données est conçu pour stocker des informations détaillées sur les crashs aériens. La table principale est `airplane_crashes`, qui comprend les champs suivants :
- `id` : Identifiant unique pour chaque crash
- `event_date` : Date du crash
- `location` : Lieu du crash
- `operator` : Opérateur de l'avion
- `aircraft_type` : Type de l'avion
- `registration` : Numéro d'immatriculation de l'avion
- `flight_number` : Numéro de vol
- `route` : Itinéraire du vol
- `fatalities` : Nombre de victimes
- `description` : Description du crash
- `source_url` : URL de la source de l'information

## Extraction des Données
Les données sont extraites des sites web du NTSB, ASN, BEA, AAIB, BFU, et EASA en utilisant des techniques de web scraping et stockées dans la table `airplane_crashes`. Le script d'extraction est écrit en Python et utilise les bibliothèques `requests` et `beautifulsoup4`.

### Script pour l'Extraction des Données

```python name=translations/fr/extract_data.py
import requests
import psycopg2
from bs4 import BeautifulSoup

# Connexion à la base de données
conn = psycopg2.connect("dbname=yourdbname user=youruser password=yourpassword host=yourhost port=yourport")
cur = conn.cursor()

# Fonction pour extraire les données d'une URL donnée
def extract_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    crashes = []
    for item in soup.find_all('div', class_='accident-item'):
        event_date = item.find('span', class_='event-date').text
        location = item.find('span', class_='location').text
        operator = item.find('span', class_='operator').text
        aircraft_type = item.find('span', class_='aircraft-type').text
        registration = item.find('span', class_='registration').text
        flight_number = item.find('span', class_='flight-number').text
        route = item.find('span', class_='route').text
        fatalities = int(item.find('span', class_='fatalities').text)
        description = item.find('span', class_='description').text
        source_url = url
        
        crash = {
            "event_date": event_date,
            "location": location,
            "operator": operator,
            "aircraft_type": aircraft_type,
            "registration": registration,
            "flight_number": flight_number,
            "route": route,
            "fatalities": fatalities,
            "description": description,
            "source_url": source_url
        }
        crashes.append(crash)
    
    return crashes

# Liste des URLs pour extraire les données
urls = [
    "https://www.ntsb.gov/Pages/AviationQueryv2.aspx",
    "https://www.bea.aero/en/investigation-reports/list-of-reports",
    "https://www.gov.uk/government/organisations/air-accidents-investigation-branch",
    "https://www.bfu-web.de/EN/Publications/Investigation-Report",
    "https://www.easa.europa.eu/document-library/accident-reports"
]

# Extraire les données de chaque URL et les insérer dans la base de données
for url in urls:
    crashes = extract_data_from_url(url)
    for crash in crashes:
        cur.execute("""
            INSERT INTO airplane_crashes (event_date, location, operator, aircraft_type, registration, flight_number, route, fatalities, description, source_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (crash['event_date'], crash['location'], crash['operator'], crash['aircraft_type'], crash['registration'], crash['flight_number'], crash['route'], crash['fatalities'], crash['description'], crash['source_url']))
        conn.commit()

# Fermer la connexion à la base de données
cur.close()
conn.close()
```

## Analyse des Données et Modélisation
La section d'analyse et de modélisation comprend :
- **Analyse Exploratoire des Données (EDA)** : Visualisation et compréhension des données.
- **Analyse Statistique** : Identification des tendances et des modèles.
- **Modélisation Prédictive** : Construction et évaluation de modèles pour prédire les crashs aériens.

### Analyse Exploratoire des Données (EDA)
L'EDA implique la visualisation de la distribution des crashs au fil du temps, des lieux géographiques, des opérateurs, des types d'avions, et d'autres facteurs.

### Analyse Statistique
Des tests et des modèles statistiques sont utilisés pour identifier les facteurs significatifs qui contribuent aux crashs aériens.

### Modélisation Prédictive
Des modèles d'apprentissage automatique sont développés pour prédire la probabilité des crashs aériens en fonction de divers facteurs. Les modèles sont évalués en utilisant des métriques telles que l'exactitude, la précision, le rappel et le F1-score.

## Spécification du Modèle Prédictif

````markdown name=translations/fr/model_specification.md
# Modèle Prédictif pour les Crashs Aériens

## Introduction
Ce document décrit la spécification détaillée d'un modèle prédictif conçu pour prévoir la probabilité des crashs aériens en se basant sur des données historiques. Le modèle vise à identifier les facteurs qui contribuent aux crashs aériens et à prédire les incidents futurs.

## Données
Les données utilisées pour ce modèle proviennent du National Transportation Safety Board (NTSB) et de l'Aviation Safety Network (ASN). Le jeu de données comprend des informations détaillées sur les crashs aériens, telles que la date, le lieu, l'opérateur, le type d'avion et le nombre de victimes.

## Prétraitement des Données
Avant de construire le modèle, les données passent par plusieurs étapes de prétraitement :
1. **Nettoyage des Données** : Suppression ou imputation des valeurs manquantes, correction des types de données et gestion des valeurs aberrantes.
2. **Ingénierie des Caractéristiques** : Création de nouvelles caractéristiques à partir des données existantes, telles que la période de l'année, les conditions météorologiques et l'âge de l'avion.
3. **Normalisation des Données** : Mise à l'échelle des caractéristiques numériques pour s'assurer qu'elles ont des plages similaires.

## Sélection du Modèle
Plusieurs algorithmes d'apprentissage automatique seront évalués pour trouver le meilleur modèle pour prédire les crashs aériens. Ces algorithmes incluent :
1. **Régression Logistique** : Un modèle simple mais efficace pour les problèmes de classification binaire.
2. **Forêt d'Arbres Décisionnels** : Une méthode d'ensemble qui combine plusieurs arbres décisionnels pour améliorer la précision.
3. **Gradient Boosting** : Une autre méthode d'ensemble qui construit des modèles de manière séquentielle pour corriger les erreurs des modèles précédents.
4. **Machine à Vecteurs de Support (SVM)** : Un classifieur puissant qui trouve l'hyperplan optimal pour séparer les classes.

## Entraînement du Modèle
Le jeu de données est divisé en ensembles d'entraînement et de test. L'ensemble d'entraînement est utilisé pour entraîner le modèle, et l'ensemble de test est utilisé pour évaluer ses performances. Une validation croisée est effectuée pour s'assurer que le modèle se généralise bien aux données non vues.

## Évaluation du Modèle
Les performances du modèle sont évaluées en utilisant les métriques suivantes :
1. **Exactitude** : La proportion des instances correctement prédites.
2. **Précision** : La proportion des prédictions positives vraies parmi toutes les prédictions positives.
3. **Rappel** : La proportion des prédictions positives vraies parmi toutes les instances positives réelles.
4. **F1-Score** : La moyenne harmonique de la précision et du rappel, fournissant un équilibre entre les deux.

## Ajustement des Hyperparamètres
L'ajustement des hyperparamètres est effectué pour optimiser les performances du modèle. Des techniques telles que la recherche sur grille et la recherche aléatoire sont utilisées pour trouver la meilleure combinaison d'hyperparamètres pour chaque algorithme.

## Résultats
Le modèle final est sélectionné en fonction de ses performances sur l'ensemble de test. Les résultats sont présentés en termes d'exactitude, de précision, de rappel et de F1-score. Des visualisations telles que les matrices de confusion et les courbes ROC sont utilisées pour illustrer les performances du modèle.

## Conclusion
Le modèle prédictif fournit des informations précieuses sur les facteurs contribuant aux crashs aériens et aide à prévoir les incidents futurs. Le modèle peut être utilisé par les autorités aéronautiques et les compagnies aériennes pour améliorer les mesures de sécurité et prévenir les crashs futurs.

## Travaux Futurs
Les améliorations futures du modèle peuvent inclure :
1. **Incorporation de Plus de Caractéristiques** : Ajout de données supplémentaires telles que les conditions météorologiques, les dossiers de maintenance et l'expérience des pilotes.
2. **Amélioration de la Qualité des Données** : Amélioration du jeu de données en obtenant des données plus précises et plus complètes.
3. **Exploration de Nouveaux Algorithmes** : Investigation de techniques d'apprentissage automatique plus sophistiquées telles que l'apprentissage profond.

## Utilisation
Pour exécuter le modèle prédictif, suivez ces étapes :
1. Assurez-vous que le jeu de données est prétraité et nettoyé.
2. Divisez le jeu de données en ensembles d'entraînement et de test.
3. Entraînez le modèle en utilisant l'ensemble d'entraînement.
4. Évaluez le modèle en utilisant l'ensemble de test.
5. Effectuez l'ajustement des hyperparamètres pour optimiser les performances du modèle.
6. Utilisez le modèle final pour faire des prédictions et analyser les résultats.

## Licence
Cette spécification de modèle est licenciée sous la Licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
