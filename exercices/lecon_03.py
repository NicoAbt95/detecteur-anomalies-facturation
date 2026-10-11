import random
from faker import Faker
random.seed(42)  # pour que les résultats soient reproductibles
Faker.seed(42)   # pour que les résultats soient reproductibles
fake = Faker("fr_FR")
ABONNEMENTS = {3: 11.50, 6: 15.60, 9: 19.50, 12: 23.30}
consommation = 350 # consommation en KWH
contrats = []

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

for i in range(1, 11):
    contrat = generer_contrat(i)
    contrats.append(contrat)
    contrat["facture"] = calculer_facture(consommation, contrat["prix_kwh"], ABONNEMENTS[contrat["puissance_kva"]])  # ajout de la facture calculée au contrat
    print (f"{contrat['identifiant']} - {contrat['nom_client']} - {contrat['puissance_kva']} kVA - {contrat['prix_kwh']} €/kWh - Actif : {contrat['actif'] } - Facture calculée : {contrat['facture']:.2f} €")  # affichage des informations du contrat et de la facture calculée

print(contrats)