import requests
import psycopg2
import pandas as pd
import csv
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

# Paramètres de la base de données depuis variables d'environnement
DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT", 5432)
}

# Créer un dossier pour les données brutes si non existant
raw_data_dir = Path("data/raw")
raw_data_dir.mkdir(parents=True, exist_ok=True)

def connect_to_database():
    """Établit une connexion à la base de données."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def extract_ntsb_data():
    """Extrait les données du NTSB via leur API."""
    print("Extraction des données du NTSB...")
    # URL de l'API NTSB - Utilisez l'URL appropriée
    url = "https://data.ntsb.gov/carol-main-public/api/Query/GetResultsByPage"
    
    # Paramètres pour la requête API (ajustez selon l'API réelle)
    params = {
        "page": 1,
        "pageSize": 100,
        "eventType": "Aviation",
        "sortColumn": "EventDate",
        "sortDirection": "DESC"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CrashDatabaseResearch/1.0; +http://yourdomain.com/contact)"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Sauvegarde des données brutes
            with open(raw_data_dir / "ntsb_data.json", "w") as f:
                json.dump(data, f)
            
            # Traitement des données (à adapter selon la structure réelle des données)
            crashes = []
            for item in data.get("results", []):
                crash = {
                    "event_date": item.get("eventDate"),
                    "location": f"{item.get('city', '')}, {item.get('state', '')}, {item.get('country', '')}",
                    "operator": item.get("operator"),
                    "aircraft_type": item.get("aircraftType"),
                    "registration": item.get("registration"),
                    "flight_number": item.get("flightNumber"),
                    "route": item.get("departureAirport", "") + " to " + item.get("destinationAirport", ""),
                    "fatalities": item.get("totalFatalities", 0),
                    "description": item.get("narrative", ""),
                    "source_url": f"https://data.ntsb.gov/carol-main-public/basic-search/result?eventId={item.get('eventId')}"
                }
                crashes.append(crash)
            
            return crashes
        else:
            print(f"Erreur lors de la requête API: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erreur lors de l'extraction des données NTSB: {e}")
        return []

def extract_aviation_safety_network_data():
    """Extrait les données de l'Aviation Safety Network."""
    print("Extraction des données de l'Aviation Safety Network...")
    # URL de recherche ASN
    url = "https://aviation-safety.net/database/dblist.php?Year=2023"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CrashDatabaseResearch/1.0; +http://yourdomain.com/contact)"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Sauvegarde du HTML brut
            with open(raw_data_dir / "asn_data.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            crashes = []
            
            # Exemple d'extraction - à adapter selon la structure réelle du site
            table = soup.find('table', class_='statistics')
            if table:
                for row in table.find_all('tr')[1:]:  # Sauter l'en-tête
                    cells = row.find_all('td')
                    if len(cells) >= 6:
                        date_str = cells[0].text.strip()
                        try:
                            event_date = datetime.strptime(date_str, '%d-%b-%Y').strftime('%Y-%m-%d')
                        except:
                            event_date = None
                            
                        crash = {
                            "event_date": event_date,
                            "location": cells[2].text.strip(),
                            "operator": cells[3].text.strip(),
                            "aircraft_type": cells[4].text.strip(),
                            "registration": cells[1].text.strip(),
                            "flight_number": "",  # Non disponible dans cette table
                            "route": "",  # Non disponible dans cette table
                            "fatalities": cells[5].text.strip().split('/')[0] if '/' in cells[5].text else 0,
                            "description": "",  # Nécessiterait de suivre le lien pour obtenir les détails
                            "source_url": "https://aviation-safety.net" + cells[0].find('a')['href'] if cells[0].find('a') else ""
                        }
                        crashes.append(crash)
            
            return crashes
        else:
            print(f"Erreur lors de la requête ASN: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erreur lors de l'extraction des données ASN: {e}")
        return []

def save_to_database(crashes, source):
    """Sauvegarde les données des crashs dans la base de données."""
    conn = connect_to_database()
    if not conn:
        return False
    
    cursor = conn.cursor()
    successful_inserts = 0
    
    try:
        for crash in crashes:
            # Conversion des types si nécessaire
            fatalities = int(crash["fatalities"]) if crash["fatalities"] and str(crash["fatalities"]).isdigit() else 0
            
            cursor.execute("""
                INSERT INTO airplane_crashes (
                    event_date, location, operator, aircraft_type, 
                    registration, flight_number, route, fatalities, 
                    description, source_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;  -- Évite les doublons
            """, (
                crash["event_date"], crash["location"], crash["operator"], 
                crash["aircraft_type"], crash["registration"], crash["flight_number"], 
                crash["route"], fatalities, crash["description"], crash["source_url"]
            ))
            successful_inserts += cursor.rowcount
        
        conn.commit()
        print(f"Données de {source} sauvegardées avec succès. {successful_inserts} nouvelles entrées.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la sauvegarde des données de {source}: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def save_to_csv(crashes, source):
    """Sauvegarde les données des crashs dans un fichier CSV."""
    if not crashes:
        print(f"Aucune donnée à sauvegarder pour {source}")
        return
    
    filename = f"data/processed/{source}_crashes.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    fieldnames = ["event_date", "location", "operator", "aircraft_type", 
                 "registration", "flight_number", "route", "fatalities", 
                 "description", "source_url"]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for crash in crashes:
                writer.writerow({k: crash.get(k, '') for k in fieldnames})
        print(f"Données de {source} sauvegardées dans {filename}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données en CSV: {e}")

def main():
    """Fonction principale pour l'extraction des données."""
    # Création des dossiers de données si non existants
    os.makedirs("data/processed", exist_ok=True)
    
    # Extraction des données du NTSB
    ntsb_crashes = extract_ntsb_data()
    if ntsb_crashes:
        save_to_database(ntsb_crashes, "NTSB")
        save_to_csv(ntsb_crashes, "ntsb")
    
    # Extraction des données de l'Aviation Safety Network
    asn_crashes = extract_aviation_safety_network_data()
    if asn_crashes:
        save_to_database(asn_crashes, "ASN")
        save_to_csv(asn_crashes, "asn")

if __name__ == "__main__":
    main()
