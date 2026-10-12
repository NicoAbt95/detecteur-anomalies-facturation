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
compteur = {"index_recule": 0, "montant_errone": 0, "consommation_aberrante": 0}


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
    mois_resiliation = None
    if not actif:
        mois_resiliation = random.randint(1, 11)
    else : 
        mois_resiliation = None
    contrat = {"identifiant": identifiant, "nom_client": nom_client, "puissance_kva": puissance_kva, "prix_kwh": prix_kwh, "actif": actif, "mois_resiliation": mois_resiliation}  
    return contrat

numero_facture = 1
for numero_contrat in range(1, 51):
    contrat = generer_contrat(numero_contrat)
    contrats.append(contrat)
    index = random.randint(10000,50000) #Index de début aléatoire pour chaque contrat
  
    for mois in range(1, 13):
        #0 Si contrat résilié alors on ne génère pas de facture pour les mois suivants 
        if contrat['mois_resiliation'] is not None and mois > contrat['mois_resiliation']: 
            #Mois_résil = 2 et mois = 3 alors on ne génère pas de facture pour les mois suivants
            continue #On passe au mois suivant sans générer de facture
        
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

        # Consommation : la réelle, puis la facturée (éventuellement fausse)
        consommation_reelle = round(contrat["puissance_kva"] * random.uniform(0.9, 1.1) * COEF_SAISON[mois - 1] * KWH_PAR_KVA)
        consommation_kwh = consommation_reelle
        if type_anomalie == "consommation_aberrante":
            consommation_kwh *= 10

        # Montant : calculé APRÈS la consommation facturée
        montant = calculer_facture(consommation_kwh, contrat["prix_kwh"], ABONNEMENTS[contrat["puissance_kva"]])
        if type_anomalie == "montant_errone":
            montant = round(montant * contrat["puissance_kva"], 2)

        # Index affichés sur la facture
        index_debut = index
        index_fin = index_debut + consommation_kwh
        if type_anomalie == "index_recule":
            index_fin = index_debut - consommation_kwh


        #4  
        facture = {
            "id_facture": f"F{numero_facture:05d}" ,
            "identifiant_contrat": contrat["identifiant"], 
            "date_facture": date(2025, mois, 1),  # génération de la date de la facture (1er jour du mois), 
            "consommation_kwh": consommation_kwh, 
            "montant": montant, 
            "index_debut": index_debut, 
            "index_fin": index_fin,  # création du dictionnaire de la facture
            "anomalie" : type_anomalie 
        }

    
        factures.append(facture) 

        #5. préparer le mois suivant : faire avancer index et numero_facture
        index = index_debut + consommation_reelle
        numero_facture += 1

for facture in factures[0:12]:
    print(f"{facture['id_facture']} | {facture['identifiant_contrat']} | {facture['date_facture']:%m/%Y} | {facture['index_debut']} -> {facture['index_fin']} | {facture['consommation_kwh']} kWh | {facture['montant']:.2f} €")  # affichage des informations de la facture

for facture in factures:
    if facture["anomalie"] is not None:  
        compteur[facture["anomalie"]]= compteur.get(facture["anomalie"],0)+1

#affichage du nombre d'anomalies dans la liste compteur : 
for anomalie, nombre in compteur.items():
    print(f"Nombre de facture pour l'anomalie {anomalie}: {nombre}")  

print(f"Nombre total de factures générées : {len(factures)}")

#Liste des factures anormales
for facture in factures:
        if facture["anomalie"] == 'consommation_aberrante': 
            print(f"Consommation aberrante : Facture {facture['id_facture']} du contrat {facture['identifiant_contrat']} | Consommation {facture['consommation_kwh']}")
        elif facture["anomalie"] == 'montant_errone':
            print(f"Montant erroné : Facture {facture['id_facture']} du contrat {facture['identifiant_contrat']} | Montant {facture['montant']}")
        elif facture["anomalie"] == 'index_recule':
            print(f"Index reculé : Facture {facture['id_facture']} du contrat {facture['identifiant_contrat']} | index Début {facture['index_debut']} vs index Fin : {facture['index_fin']}")
