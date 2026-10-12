# Détecteur d'anomalies de facturation

Projet personnel : détection d'anomalies sur des factures d'énergie fictives,
par règles métier puis machine learning, avec explication par un LLM.

## Prérequis
- Python 3.13
- `pip install -r requirements.txt`

## Générer les données
```
python src/generate_data.py
```
Produit `data/contrats.csv` (50 contrats) et `data/factures.csv` (factures mensuelles 2025),
avec environ 6 % d'anomalies injectées et étiquetées dans la colonne `anomalie` :
consommation aberrante, index qui recule, montant erroné.