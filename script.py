import pandas as pd
import zipfile
import requests
import os
from io import BytesIO

pop_mun = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/8c35e301-192d-4c14-a0b4-dfa02deecbc1", sep = ",", header=0, encoding='windows-1252', low_memory=False)
print(pop_mun.head(20))

effectifs_ecoles = pd.read_csv("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ecoles-effectifs-nb_classes/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B", sep = ";", header = 0)
print(effectifs_ecoles.head(20))

code_geographique = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/2648d606-504d-4e91-ac1f-d70c92adc039", sep = ",", header=0, encoding='windows-1252')
print(code_geographique.head(20))

#Filtrer pour ne garder que Paris dans les deux bases de données 
#Matcher par arrondissement ? (Code postal) 
#Le nom de la commune dans pop_mun se récupère à partir de la colonne com_code à croiser avec code_géographique pour avoir le nom de la commune

print(pop_mun.columns)
print(effectifs_ecoles.columns)

# Il faut aussi charger les bases de données du recensement pour les autres années : ici c'est que 2020 

#Données resensements 

#Racine https://www.insee.fr/fr/information/2008354

#Fichiers des mobilités scolaires 

#Millésime 2020 https://www.insee.fr/fr/statistiques/7637890
#Mobilité scolaire 2020 https://www.insee.fr/fr/statistiques/7637665?sommaire=7637890

# Lien du fichier ZIP à télécharger
url = "https://www.insee.fr/fr/statistiques/fichier/7637665/RP2020_mobsco_csv.zip"
response = requests.get(url)
print(response)

if response.status_code == 200:
    print("Téléchargement réussi !")
    
    # Ouvrir le fichier ZIP depuis la mémoire (en mémoire via BytesIO)
    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        
        # Dossier où les fichiers extraits seront placés
        extract_folder = "extracted_files"
        os.makedirs(extract_folder, exist_ok=True)
        
        # Extraire tous les fichiers dans le dossier temporaire
        zip_ref.extractall(extract_folder)
        
        # Lister les fichiers extraits
        extracted_files = os.listdir(extract_folder)
        csv_files = [f for f in extracted_files if f.endswith('.csv')]
        
        # Si des fichiers CSV sont trouvés, on charge le premier dans un DataFrame
        if csv_files:
            csv_file = csv_files[0]  # Utiliser le premier fichier CSV trouvé
            print(f"Fichier CSV trouvé : {csv_file}")
            
            # Charger le fichier CSV dans un DataFrame pandas
            mobscol_2020 = pd.read_csv(os.path.join(extract_folder, csv_file), nrows=100, header=0, encoding='windows-1252', low_memory=False)
            
            # Afficher les premières lignes des données
            print(mobscol_2020.head())
        else:
            print("Aucun fichier CSV trouvé dans l'archive ZIP.")
else:
    print(f"Erreur lors du téléchargement du fichier : {response.status_code}")

['COMMUNE', 'ARM','DCETUF','AGEREV10','CSM','INPSM','NPERR']
mobscol_2020 = pd.read_csv(, sep = ",", nrows=100, header=0, encoding='windows-1252', low_memory=False)
print(mobscol_2020(20))


