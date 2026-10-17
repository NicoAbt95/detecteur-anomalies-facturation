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

## Résultats – détection par règles métier
| Règle | Anomalie visée | Précision | Rappel |
|---|---|---|---|
| Index fin < index début | index_recule | 100 % | 100 % |
| Montant ≠ recalcul (±0,01 €) | montant_errone | 100 % | 100 % |
| Consommation > 3× médiane du contrat | consommation_aberrante | 100 % | 100 % |

Limite : données synthétiques, anomalies franches et sans bruit.
Détail dans `notebooks/03_pistes_detection.ipynb`.