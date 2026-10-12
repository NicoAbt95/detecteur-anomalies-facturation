"""Génère un jeu de données fictif de contrats et de factures d'électricité,
avec des anomalies injectées et étiquetées.

Usage (depuis la racine du projet) : python src/generate_data.py
"""
import random
from datetime import date

import pandas as pd
from faker import Faker

# --- Paramètres ---
GRAINE = 42
NB_CONTRATS = 50
ANNEE = 2025
ABONNEMENTS = {3: 11.50, 6: 15.60, 9: 19.50, 12: 23.30}
KWH_PAR_KVA = 40
COEF_SAISON = [1.5, 1.4, 1.2, 1.0, 0.8, 0.7, 0.6, 0.6, 0.7, 0.9, 1.2, 1.4]

random.seed(GRAINE)
Faker.seed(GRAINE)
fake = Faker("fr_FR")


def calculer_facture(consommation, prix_kwh, abonnement):
    """Calcule la facture arrondie au centime."""     
    facture = round(consommation * prix_kwh + abonnement, 2)
    return facture

def generer_contrat(numero):
    """Génère un contrat fictif. Les contrats inactifs ont un mois de résiliation."""
    identifiant = f"C{numero:04d}"  # génération de l'identifiant du contrat
    nom_client = fake.company()  # génération d'un nom de société fictive
    puissance_kva = random.choice(list(ABONNEMENTS.keys()))  # choix aléatoire de la puissance souscrite parmi les clés du dictionnaire ABONNEMENTS   
    prix_kwh = round(random.uniform(0.20, 0.30), 4)  # génération d'un prix du kWh aléatoire entre 0.20 et 0.30 euros
    actif = random.random() < 0.9  #  90% de chances que le contrat soit actif et 10% de chances qu'il soit inactif  
    mois_resiliation = None
    if not actif:
        mois_resiliation = random.randint(1, 11)
    else : 
        mois_resiliation = None
    contrat = {"identifiant": identifiant, "nom_client": nom_client, "puissance_kva": puissance_kva, "prix_kwh": prix_kwh, "actif": actif, "mois_resiliation": mois_resiliation}  
    return contrat

def tirer_anomalie():
    """Tire au hasard le type d'anomalie d'une facture, ou None (environ 94 % des cas)."""
     #tirage de l'anomalie
    tirage = random.random()
    if tirage < 0.02:
        type_anomalie = "consommation_aberrante"
    elif tirage < 0.04:
        type_anomalie = "index_recule"
    elif tirage < 0.06:
        type_anomalie = "montant_errone"
    else:
        type_anomalie = None
    return type_anomalie

def generer_factures(contrats):
    """Génère les factures mensuelles de chaque contrat, avec les anomalies injectées."""
    numero_facture = 1
    factures = []
    for numero_contrat in range(1, NB_CONTRATS):
        contrat = generer_contrat(numero_contrat)
        contrats.append(contrat)
        index = random.randint(10000,50000) #Index de début aléatoire pour chaque contrat

        for mois in range(1, 13):
            # Si contrat résilié alors on ne génère pas de facture pour les mois suivants 
            if contrat['mois_resiliation'] is not None and mois > contrat['mois_resiliation']: 
                #Mois_résil = 2 et mois = 3 alors on ne génère pas de facture pour les mois suivants
                continue 
            
            consommation_reelle = round(contrat["puissance_kva"] * random.uniform(0.9, 1.1) * COEF_SAISON[mois - 1] * KWH_PAR_KVA)
            consommation_kwh = consommation_reelle
            type_anomalie = tirer_anomalie()

            if type_anomalie == "consommation_aberrante":
                consommation_kwh *= 10

            # Montant : calculé APRÈS la consommation facturée
            montant = calculer_facture(consommation_kwh, contrat["prix_kwh"], ABONNEMENTS[contrat["puissance_kva"]])
            if type_anomalie == "montant_errone":
                montant = round(montant * contrat["puissance_kva"], 2)

            index_debut = index
            index_fin = index_debut + consommation_kwh
            if type_anomalie == "index_recule":
                index_fin = index_debut - consommation_kwh
  
            facture = {
                "id_facture": f"F{numero_facture:05d}" ,
                "identifiant_contrat": contrat["identifiant"], 
                "date_facture": date(ANNEE, mois, 1),  
                "consommation_kwh": consommation_kwh, 
                "montant": montant, 
                "index_debut": index_debut, 
                "index_fin": index_fin,  
                "anomalie" : type_anomalie 
            }

            factures.append(facture) 

            index = index_debut + consommation_reelle
            numero_facture += 1
        
    return factures

def main():
    """Génère les données, les exporte en CSV et affiche un bilan."""
    contrats = []
    for numero in range(1, NB_CONTRATS + 1):
        contrats.append(generer_contrat(numero))
    factures = generer_factures(contrats)

    df_contrats = pd.DataFrame(contrats)
    df_factures = pd.DataFrame(factures)
    print(df_factures.head())
    print(df_factures.shape)
    print(df_factures.dtypes)
    print(df_factures["anomalie"].value_counts(dropna=False))
    df_contrats.to_csv("data/contrats.csv", index=False)
    df_factures.to_csv("data/factures.csv", index=False)
    print(df_factures["anomalie"].notna().sum())

if __name__ == "__main__":
    main()







