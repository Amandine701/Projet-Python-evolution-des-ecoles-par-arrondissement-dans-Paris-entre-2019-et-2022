import pandas as pd

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


