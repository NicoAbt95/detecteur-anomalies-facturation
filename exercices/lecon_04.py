import random
from faker import Faker
from datetime import date 
random.seed(42)  # pour que les résultats soient reproductibles
Faker.seed(42)   # pour que les résultats soient reproductibles
fake = Faker("fr_FR")
ABONNEMENTS = {3: 11.50, 6: 15.60, 9: 19.50, 12: 23.30}#liste de clés et valeurs pour les abonnements selon la puissance souscrite
KWH_PAR_KVA = 40 #Consommation mensuelle de base par kVA souscrit
contrats = []
factures = []
COEF_SAISON = [1.5, 1.4, 1.2, 1.0, 0.8, 0.7, 0.6, 0.6, 0.7, 0.9, 1.2, 1.4]

def calculer_facture(consommation, prix_kwh,abonnement): 
    """Calcule la facture arrondie au centime."""     
    facture = round(consommation * prix_kwh + abonnement, 2)
    return facture

def generer_contrat(numero):
    """Générer un contrat fictif avec des informations aléatoires"""
    identifiant = f"C{numero:04d}"  # génération de l'identifiant du contrat
    nom_client = fake.company()  # génération d'un nom de société fictive
    puissance_kva = random.choice(list(ABONNEMENTS.keys()))  # choix aléatoire de la puissance souscrite parmi les clés du dictionnaire ABONNEMENTS   
    prix_kwh = round(random.uniform(0.20, 0.30), 4)  # génération d'un prix du kWh aléatoire entre 0.20 et 0.30 euros
    actif = random.random() < 0.9  #  90% de chances que le contrat soit actif et 10% de chances qu'il soit inactif
    contrat = {"identifiant": identifiant, "nom_client": nom_client, "puissance_kva": puissance_kva, "prix_kwh": prix_kwh, "actif": actif}  # ajout de la facture calculée au contrat   
    return contrat

numero_facture = 1
for numero_contrat in range(1, 11):
    contrat = generer_contrat(numero_contrat)
    contrats.append(contrat)
    index = random.randint(10000,50000) #Index de début aléatoire pour chaque contrat
  
    for mois in range(1, 13):
        # 1. consommation_kwh : base × COEF_SAISON[mois - 1] × aléa, arrondie à l'entier
        # 2. montant : calculer_facture(...) avec cette consommation
        # 3. index_debut = index actuel ; index_fin = index_debut + consommation
        # 4. construire le dictionnaire complet de la facture, puis append
        # 5. préparer le mois suivant : faire avancer index et numero_facture
        
        #1 
        consommation_kwh = round(contrat["puissance_kva"] * random.uniform(0.9, 1.1) * COEF_SAISON[mois-1]*KWH_PAR_KVA) # calcul base * coef du mois * aléa
        #2 
        montant = calculer_facture(consommation_kwh, contrat["prix_kwh"], ABONNEMENTS[contrat["puissance_kva"]])  # calcul du montant de la facture

        #3
        index_debut = index # index de début = index actuel
        index_fin = index_debut + consommation_kwh  # Chaque mois, l'index de fin est égal à l'index de début + la consommation en kWh

        #4  

        facture = {
            "id_facture": f"F{numero_facture:05d}" ,
            "identifiant_contrat": contrat["identifiant"], 
            "date_facture": date(2025, mois, 1),  # génération de la date de la facture (1er jour du mois), 
            "consommation_kwh": consommation_kwh, 
            "montant": montant, 
            "index_debut": index_debut, 
            "index_fin": index_fin}  # création du dictionnaire de la facture
            
        factures.append(facture) 
        
        index = index_fin  # préparation du mois suivant : faire avancer index pour le mois suivant
        numero_facture += 1

for facture in factures[0:12]:
    print(f"{facture['id_facture']} | {facture['identifiant_contrat']} | {facture['date_facture']:%m/%Y} | {facture['index_debut']} -> {facture['index_fin']} | {facture['consommation_kwh']} kWh | {facture['montant']:.2f} €")  # affichage des informations de la facture
#print(f"Nombre de contrats générés : {len(contrats)}") Nombre de contrats générés : 10
#print(f"Nombre de factures générées : {len(factures)}")Nombre de factures générées : 120