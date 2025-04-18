import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix, classification_report
import joblib
import os
from datetime import datetime

# Configuration
DATA_DIR = "data/processed"
MODELS_DIR = "models"
RESULTS_DIR = "results"
RANDOM_STATE = 42

# Création des répertoires nécessaires
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_data(file_path):
    """Charge les données depuis un fichier CSV."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return None

def preprocess_data(data):
    """Prétraite les données pour l'analyse."""
    if data is None:
        return None, None, None, None
    
    # Conversion de la date en caractéristiques temporelles
    data['event_date'] = pd.to_datetime(data['event_date'])
    data['year'] = data['event_date'].dt.year
    data['month'] = data['event_date'].dt.month
    data['day'] = data['event_date'].dt.day
    data['day_of_week'] = data['event_date'].dt.dayofweek
    
    # Sélection des caractéristiques pour le modèle
    # Utilisation de 'Fatalities' comme seule caractéristique numérique pour cet exemple
    # Dans un cas réel, vous auriez plus de caractéristiques numériques et catégorielles
    numeric_features = ['Fatalities', 'year', 'month', 'day']
    categorical_features = []  # Par exemple: 'Operator', 'Location' catégorisée, etc.
    
    # Préprocesseur pour les données
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
        # Si vous avez des caractéristiques catégorielles, décommentez la ligne suivante
        # ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])
    
    # Préparation des données
    X = data[numeric_features]  # + categorical_features si vous en avez
    y = data['target']
    
    # Division en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    
    return X_train, X_test, y_train, y_test, preprocessor, numeric_features

def train_and_evaluate_models(X_train, X_test, y_train, y_test, preprocessor):
    """Entraîne et évalue différents modèles."""
    if X_train is None:
        return None
    
    # Définition des modèles
    models = {
        'Logistic Regression': LogisticRegression(random_state=RANDOM_STATE),
        'Random Forest': RandomForestClassifier(random_state=RANDOM_STATE),
        'Gradient Boosting': GradientBoostingClassifier(random_state=RANDOM_STATE),
        'SVM': SVC(probability=True, random_state=RANDOM_STATE)
    }
    
    results = {}
    best_f1 = 0
    best_model_name = None
    
    for name, model in models.items():
        print(f"\nEntraînement du modèle: {name}")
        
        # Création du pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        # Entraînement
        pipeline.fit(X_train, y_train)
        
        # Prédictions
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        
        # Métriques
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'model': pipeline
        }
        
        # Mise à jour du meilleur modèle
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
        
        # Rapport de classification
        print(f"\nRapport de classification pour {name}:")
        print(classification_report(y_test, y_pred))
        
        # Matrice de confusion
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Matrice de confusion - {name}')
        plt.ylabel('Valeur réelle')
        plt.xlabel('Valeur prédite')
        plt.savefig(f"{RESULTS_DIR}/confusion_matrix_{name.replace(' ', '_').lower()}.png")
        
        # Courbe ROC
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taux de faux positifs')
        plt.ylabel('Taux de vrais positifs')
        plt.title(f'Courbe ROC - {name}')
        plt.legend(loc="lower right")
        plt.savefig(f"{RESULTS_DIR}/roc_curve_{name.replace(' ', '_').lower()}.png")
    
    # Sauvegarde du meilleur modèle
    if best_model_name:
        best_model = results[best_model_name]['model']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = f"{MODELS_DIR}/best_model_{best_model_name.replace(' ', '_').lower()}_{timestamp}.pkl"
        joblib.dump(best_model, model_path)
        print(f"\nMeilleur modèle ({best_model_name}) sauvegardé à: {model_path}")
    
    return results

def feature_importance(results, numeric_features):
    """Analyse l'importance des caractéristiques."""
    if 'Random Forest' in results:
        model = results['Random Forest']['model']
        # Extraction du classifieur depuis le pipeline
        rf = model.named_steps['classifier']
        
        # Récupération de l'importance des caractéristiques
        importances = rf.feature_importances_
        
        # Création d'un DataFrame pour une meilleure visualisation
        feature_imp = pd.DataFrame({
            'Caractéristique': numeric_features,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Caractéristique', data=feature_imp)
        plt.title('Importance des caractéristiques (Random Forest)')
        plt.tight_layout()
        plt.savefig(f"{RESULTS_DIR}/feature_importance.png")
        
        return feature_imp
    return None

def main():
    """Fonction principale pour l'analyse des données et la modélisation."""
    # Chargement des données
    data_file = f"{DATA_DIR}/airplane_crashes.csv"
    data = load_data(data_file)
    
    if data is None:
        print("Impossible de procéder sans données valides.")
        return
    
    # Prétraitement des données
    X_train, X_test, y_train, y_test, preprocessor, numeric_features = preprocess_data(data)
    
    # Entraînement et évaluation des modèles
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test, preprocessor)
    
    # Analyse de l'importance des caractéristiques
    if results:
        feature_imp = feature_importance(results, numeric_features)
        if feature_imp is not None:
            print("\nImportance des caractéristiques:")
            print(feature_imp)
    
    print("\nAnalyse terminée. Les résultats sont disponibles dans le dossier 'results'.")

if __name__ == "__main__":
    main()
