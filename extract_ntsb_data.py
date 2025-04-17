import psycopg2

# Remplacez les valeurs suivantes par les informations valides de votre base de données
dbname = "mydatabase"
user = "myuser"
password = "mypassword"
host = "localhost"
port = 5432  # Assurez-vous que le port est un entier

try:
    # Connexion à la base de données PostgreSQL
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connexion réussie à la base de données")
    
    # Créez un curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()
    
    # Exemple de requête pour vérifier la connexion
    cursor.execute("SELECT * FROM your_table LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    # Fermez le curseur et la connexion
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"Erreur de connexion à la base de données : {e}")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")