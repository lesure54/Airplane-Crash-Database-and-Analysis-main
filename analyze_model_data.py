import csv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc

data = [
    {"Date": "2023-01-01", "Location": "New York", "Operator": "Airline A", "Flight Number": "AA123", "Fatalities": 5, "target": 0},
    {"Date": "2023-02-15", "Location": "Los Angeles", "Operator": "Airline B", "Flight Number": "BB456", "Fatalities": 10, "target": 1},
    {"Date": "2023-03-20", "Location": "Chicago", "Operator": "Airline C", "Flight Number": "CC789", "Fatalities": 2, "target": 0},
    {"Date": "2023-04-10", "Location": "Houston", "Operator": "Airline D", "Flight Number": "DD101", "Fatalities": 8, "target": 1},
    {"Date": "2023-05-05", "Location": "Miami", "Operator": "Airline E", "Flight Number": "EE202", "Fatalities": 0, "target": 0},
    {"Date": "2023-06-15", "Location": "Seattle", "Operator": "Airline F", "Flight Number": "FF303", "Fatalities": 3, "target": 1},
    {"Date": "2023-07-20", "Location": "San Francisco", "Operator": "Airline G", "Flight Number": "GG404", "Fatalities": 7, "target": 1},
    {"Date": "2023-08-30", "Location": "Las Vegas", "Operator": "Airline H", "Flight Number": "HH505", "Fatalities": 4, "target": 0},
    {"Date": "2023-09-10", "Location": "Denver", "Operator": "Airline I", "Flight Number": "II606", "Fatalities": 6, "target": 1},
    {"Date": "2023-10-25", "Location": "Boston", "Operator": "Airline J", "Flight Number": "JJ707", "Fatalities": 1, "target": 0},
    {"Date": "2023-11-11", "Location": "Orlando", "Operator": "Airline K", "Flight Number": "KK808", "Fatalities": 9, "target": 1},
    {"Date": "2023-12-05", "Location": "Dallas", "Operator": "Airline L", "Flight Number": "LL909", "Fatalities": 5, "target": 0},
    {"Date": "2024-01-15", "Location": "Atlanta", "Operator": "Airline M", "Flight Number": "MM010", "Fatalities": 7, "target": 1},
    {"Date": "2024-02-20", "Location": "Phoenix", "Operator": "Airline N", "Flight Number": "NN111", "Fatalities": 2, "target": 0},
    {"Date": "2024-03-30", "Location": "Minneapolis", "Operator": "Airline O", "Flight Number": "OO212", "Fatalities": 6, "target": 1},
    {"Date": "2024-04-10", "Location": "San Diego", "Operator": "Airline P", "Flight Number": "PP313", "Fatalities": 4, "target": 0},
    {"Date": "2024-05-25", "Location": "Detroit", "Operator": "Airline Q", "Flight Number": "QQ414", "Fatalities": 8, "target": 1},
    {"Date": "2024-06-05", "Location": "Philadelphia", "Operator": "Airline R", "Flight Number": "RR515", "Fatalities": 3, "target": 0},
    {"Date": "2024-07-15", "Location": "Charlotte", "Operator": "Airline S", "Flight Number": "SS616", "Fatalities": 1, "target": 0},
    {"Date": "2024-08-20", "Location": "Austin", "Operator": "Airline T", "Flight Number": "TT717", "Fatalities": 9, "target": 1},
    {"Date": "2024-09-15", "Location": "San Antonio", "Operator": "Airline U", "Flight Number": "UU818", "Fatalities": 4, "target": 0},
    {"Date": "2024-10-05", "Location": "Nashville", "Operator": "Airline V", "Flight Number": "VV919", "Fatalities": 5, "target": 1},
    {"Date": "2024-11-20", "Location": "Memphis", "Operator": "Airline W", "Flight Number": "WW020", "Fatalities": 3, "target": 0},
    {"Date": "2024-12-15", "Location": "Jacksonville", "Operator": "Airline X", "Flight Number": "XX121", "Fatalities": 2, "target": 0},
    {"Date": "2025-01-10", "Location": "Indianapolis", "Operator": "Airline Y", "Flight Number": "YY222", "Fatalities": 8, "target": 1},
    {"Date": "2025-02-05", "Location": "Columbus", "Operator": "Airline Z", "Flight Number": "ZZ323", "Fatalities": 7, "target": 1},
    {"Date": "2025-03-20", "Location": "Fort Worth", "Operator": "Airline AA", "Flight Number": "AA424", "Fatalities": 6, "target": 1},
    {"Date": "2025-04-15", "Location": "El Paso", "Operator": "Airline BB", "Flight Number": "BB525", "Fatalities": 4, "target": 0},
    {"Date": "2025-05-10", "Location": "Louisville", "Operator": "Airline CC", "Flight Number": "CC626", "Fatalities": 9, "target": 1},
    {"Date": "2025-06-15", "Location": "Baltimore", "Operator": "Airline DD", "Flight Number": "DD727", "Fatalities": 3, "target": 0},
]

# Nom du fichier CSV
csv_file = "airplane_crashes.csv"

# Champs du CSV
fields = ["Date", "Location", "Operator", "Flight Number", "Fatalities", "target"]

# Écriture des données dans le fichier CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"Le fichier {csv_file} a été généré avec succès.")

# Lecture du fichier CSV avec pandas
try:
    data = pd.read_csv(csv_file)
    print("Fichier CSV lu avec succès")
except pd.errors.ParserError as e:
    print("Erreur lors de la lecture du fichier CSV:", e)
    data = None
except FileNotFoundError:
    print(f"Le fichier '{csv_file}' n'a pas été trouvé.")
    data = None
except Exception as e:
    print("Une erreur s'est produite:", e)
    data = None

if data is not None:
    # Preprocess data
    # Drop non-numeric columns
    data = data.drop(columns=["Date", "Location", "Operator", "Flight Number"])

    # Split data into training and testing sets
    X = data.drop('target', axis=1)  # Replace 'target' with the actual target column name
    y = data['target']  # Replace 'target' with the actual target column name
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define models
    models = {
        'Logistic Regression': LogisticRegression(),
        'Random Forest': RandomForestClassifier(),
        'Gradient Boosting': GradientBoostingClassifier(),
        'SVM': SVC(probability=True)
    }

    # Train and evaluate models
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }

        print(f"{name} - Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1-Score: {f1}")

        if y_prob is not None:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.2f})')

    # Plot ROC curve
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.show()