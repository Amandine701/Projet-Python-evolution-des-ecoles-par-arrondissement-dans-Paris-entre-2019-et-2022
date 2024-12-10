import pandas as pd
import zipfile
import requests
import os
from io import BytesIO



effectifs_ecoles = pd.read_csv("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ecoles-effectifs-nb_classes/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B", sep = ";", header = 0)
print(effectifs_ecoles.head(20))

code_geographique = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/2648d606-504d-4e91-ac1f-d70c92adc039", sep = ",", header=0, encoding='windows-1252')
print(code_geographique.head(20))

# Filtrer pour ne conserver que Paris dans les deux bases de données
#Matcher par arrondissement ? (Code postal) 
#Le nom de la commune dans pop_mun se récupère à partir de la colonne com_code à croiser avec code_géographique pour avoir le nom de la commune

print(effectifs_ecoles.columns)
effectifs_ecoles["Rentrée scolaire"].unique()



#Données resensements 

#Racine https://www.insee.fr/fr/information/2008354


#Année 2021 pour les logements en zone A (IDF) https://www.insee.fr/fr/statistiques/8268903?sommaire=8205966#consulter

# Lien du fichier ZIP à télécharger
url = "https://www.insee.fr/fr/statistiques/fichier/8268903/RP2021_logemtza.zip"
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
        pop_2021 = pd.read_csv(os.path.join(extract_folder, "FD_LOGEMTZA_2021.csv"), sep = ";", header=0, encoding='UTF-8', low_memory=False)

else:
    print(f"Erreur lors du téléchargement du fichier : {response.status_code}")


print(pop_2021.head(20))



#Année 2020 pour les logements en zone A (IDF) https://www.insee.fr/fr/statistiques/7705908?sommaire=7637890

# Lien du fichier ZIP à télécharger
url = "https://www.insee.fr/fr/statistiques/fichier/7705908/RP2020_LOGEMTZA_csv.zip"
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
        pop_2020 = pd.read_csv(os.path.join(extract_folder, "FD_LOGEMTZA_2020.csv"), sep = ";", header=0, encoding='UTF-8', low_memory=False)

else:
    print(f"Erreur lors du téléchargement du fichier : {response.status_code}")

#['COMMUNE', 'ARM','DCETUF','AGEREV10','CSM','INPSM','NPERR']
#mobscol_2020 = pd.read_csv(, sep = ";", nrows=100, header=0, encoding='windows-1252', low_memory=False)

print(pop_2020.head(20))




#Année 2019 pour les logements en zone A (IDF) https://www.insee.fr/fr/statistiques/6544344?sommaire=6456104

# Lien du fichier ZIP à télécharger
url = "https://www.insee.fr/fr/statistiques/fichier/6544344/RP2019_LOGEMTZA_csv.zip"
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
        pop_2019 = pd.read_csv(os.path.join(extract_folder, "FD_LOGEMTZA_2019.csv"), sep = ";", header=0, encoding='UTF-8', low_memory=False)

else:
    print(f"Erreur lors du téléchargement du fichier : {response.status_code}")

#['COMMUNE', 'ARM','DCETUF','AGEREV10','CSM','INPSM','NPERR']
#mobscol_2020 = pd.read_csv(, sep = ";", nrows=100, header=0, encoding='windows-1252', low_memory=False)

print(pop_2019.head(20))


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
            mobscol_2020 = pd.read_csv(os.path.join(extract_folder, csv_file), sep = ";", nrows=100, header=0, encoding='windows-1252', low_memory=False)
            
            # Afficher les premières lignes des données
            print(mobscol_2020.head())
        else:
            print("Aucun fichier CSV trouvé dans l'archive ZIP.")
else:
    print(f"Erreur lors du téléchargement du fichier : {response.status_code}")

#['COMMUNE', 'ARM','DCETUF','AGEREV10','CSM','INPSM','NPERR']
#mobscol_2020 = pd.read_csv(, sep = ";", nrows=100, header=0, encoding='windows-1252', low_memory=False)

print(mobscol_2020.head(20))

# Fichier détaillant la population par classe d'âge dans les arrondissements parisiens
en 2019
#https://www.insee.fr/fr/statistiques/8272002#documentation

#  Chargement fichier ZIP depuis l'URL
url = 'https://www.insee.fr/fr/statistiques/fichier/6456157/BTT_TD_POP1B_2019.zip'
zip_filename = 'BTT_TD_POP1B_2019.zip'

# Téléchargement le fichier 
if not os.path.exists(zip_filename):
    response = requests.get(url)
    with open(zip_filename, 'wb') as file:
        file.write(response.content)
    print(f"Fichier {zip_filename} téléchargé avec succès.")
else:
    print(f"Le fichier {zip_filename} existe déjà.")


# Extraction du contenu du fichier ZIP
with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    zip_ref.extractall("extracted_files")
    print("Fichiers extraits.")

file_to_read = "extracted_files/BTT_TD_POP1B_2019.csv" 

# Transformation du fichier CSV dans un DataFrame
df_ages_2019 = pd.read_csv('extracted_files/BTT_TD_POP1B_2019.csv', delimiter=';', encoding='latin1')




# Fichier détaillant la population par classe d'âge dans les arrondissements parisiens
en 2021
#https://www.insee.fr/fr/statistiques/8202264

#  Chargement fichier ZIP depuis l'URL
url = 'https://www.insee.fr/fr/statistiques/fichier/8202264/TD_POP1B_2021_csv.zip'
zip_filename = 'TD_POP1B_2021.zip'

# Téléchargement le fichier 
if not os.path.exists(zip_filename):
    response = requests.get(url)
    with open(zip_filename, 'wb') as file:
        file.write(response.content)
    print(f"Fichier {zip_filename} téléchargé avec succès.")
else:
    print(f"Le fichier {zip_filename} existe déjà.")


# Extraction du contenu du fichier ZIP
with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    zip_ref.extractall("extracted_files")
    print("Fichiers extraits.")

file_to_read = "extracted_files/TD_POP1B_2021.csv" 

# Transformation du fichier CSV dans un DataFrame
df_ages_2021 = pd.read_csv('extracted_files/TD_POP1B_2021.csv', delimiter=';', encoding='latin1')

# Fichier détaillant la population par classe d'âge dans les arrondissements parisiens
en 2020

#  Chargement fichier ZIP depuis l'URL
url = 'https://www.insee.fr/fr/statistiques/fichier/7631680/TD_POP1B_2020_csv.zip'
zip_filename = 'BTT_TD_POP1B_2020.zip'

# Téléchargement le fichier 
if not os.path.exists(zip_filename):
    response = requests.get(url)
    with open(zip_filename, 'wb') as file:
        file.write(response.content)
    print(f"Fichier {zip_filename} téléchargé avec succès.")
else:
    print(f"Le fichier {zip_filename} existe déjà.")


# Extraction du contenu du fichier ZIP
with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    zip_ref.extractall("extracted_files")
    print("Fichiers extraits.")

file_to_read = "extracted_files/TD_POP1B_2020.csv" 

# Transformation du fichier CSV dans un DataFrame
df_ages_2020 = pd.read_csv('extracted_files/TD_POP1B_2020.csv', delimiter=';', encoding='latin1')






