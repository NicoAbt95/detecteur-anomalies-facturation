consommation = 350 # consommation en KWH
abonnement = 15.60 # abonnement en euros

#2 - boucles 
contrats = [
    {"identifiant": "A0001", "nom_client": "SARL Dupont", "puissance_kva": 6, "prix_kwh": 0.25, "actif": True},
    {"identifiant": "A0002", "nom_client": "SARL Martin", "puissance_kva": 9, "prix_kwh": 0.30, "actif": True},
    {"identifiant": "A0003", "nom_client": "SARL Durand", "puissance_kva": 12, "prix_kwh": 0.20, "actif": False},
    {"identifiant": "A0004", "nom_client": "SARL Petit", "puissance_kva": 15, "prix_kwh": 0.35, "actif": True}
]

print(f"Nombre contrats : {len(contrats)}") # affichage du nombre de contrats
total = 0 # initialisation de la variable total pour le calcul du total des factures

for contrat in contrats: # boucle sur la liste des contrats
    facture = round(consommation * contrat["prix_kwh"] + abonnement, 2)
    total += facture
    print(f"{contrat['identifiant']} - {contrat['nom_client']} : {facture:.2f} €") # affichage des informations du contrat
print(f"Total factures : {total:.2f} €") # affichage du total des factures

contrats_generes = [] #Création d'une liste vide pour stocker les contrats générés
for i in range(1, 6): # boucle pour générer 5 contrats
    identifiant = f"C{i:04d}" # génération de l'identifiant du contrat
    nom_client = f"Société Client {i}" # génération du nom du client
    puissance_kva =  6
    prix_kwh = 0.25 #0.25 euros par KWH
    actif =  True 
    contrats_generes.append({"identifiant": identifiant , "nom_client": nom_client, "puissance_kVA": puissance_kva, "prix_kwh": prix_kwh, "actif": actif}) # ajout du contrat généré à la liste des contrats générés
    print(f"Contrat généré : {identifiant} - {nom_client} - {puissance_kva} kVA - {prix_kwh} €/kWh - Actif : {actif}") # affichage des informations du contrat généré 

print(f"Nombre contrats générés : {len(contrats_generes)}") # affichage du nombre de contrats générés   
 