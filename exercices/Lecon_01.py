identifiant = "A0001"
nom_client = "SARL Dupont"
puissance_kva = 6
prix_kwh = 0.25 #0.25 euros par KWH
actif =  True 

consommation = 350 # consommation en KWH
abonnement = 15.60 # abonnement en euros
print(f"Le Contrat {identifiant} du client {nom_client} a une puissance souscrite de {puissance_kva} kva, le prix du KWH est de {prix_kwh    } euros , son contrat est ouvert : {actif}") # affichage des informations du contrat      

contrat = {"identifiant": identifiant , "nom_client": nom_client, "puissance_kva": puissance_kva, "prix_kwh": prix_kwh, "actif": actif} #définition d'un dictionnaire pour le contrat
print(contrat["nom_client"])        # lire une valeur du contrat   
contrat["puissance_kva"] = 9     # modifier une valeur du contrat
print(contrat)  # lire la valeur modifiée du contrat


#Exercice de calcul de la facture d'électricité
facture = round(consommation * contrat["prix_kwh"] + abonnement, 2) # calcul de la facture d'électricité
print(f"La facture du client {nom_client} est de : {facture:.2f} €")