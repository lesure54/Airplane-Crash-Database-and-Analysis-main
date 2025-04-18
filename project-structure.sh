crash_analysis_project/
├── data/
│   ├── raw/                  # Données brutes extraites
│   ├── processed/            # Données nettoyées et prétraitées
│   └── external/             # Données provenant de sources externes
├── models/                   # Modèles entraînés et sauvegardés
├── notebooks/                # Jupyter notebooks pour l'analyse exploratoire
├── results/                  # Résultats d'analyse, graphiques, etc.
├── src/                      # Code source
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── extract_data.py   # Scripts d'extraction de données
│   │   └── preprocess_data.py # Scripts de prétraitement
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train_model.py    # Scripts d'entraînement
│   │   └── predict_model.py  # Scripts de prédiction
│   └── visualization/
│       ├── __init__.py
│       └── visualize.py      # Scripts de visualisation
├── tests/                    # Tests unitaires et d'intégration
├── .env.example              # Exemple de fichier d'environnement
├── .gitignore                # Fichiers à ignorer par Git
├── requirements.txt          # Dépendances Python
├── setup.py                  # Configuration d'installation
├── README.md                 # Documentation principale
└── LICENSE                   # Licence du projet
