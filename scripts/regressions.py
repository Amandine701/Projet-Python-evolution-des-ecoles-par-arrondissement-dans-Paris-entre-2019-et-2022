import pandas as pd
import statsmodels.api as sm
from unidecode import unidecode
# régression des effectifs par année et arrondissement sur une constante, certaines tranches d'âges (en âge d'avoir des enfants), et des effets fixes par arrondissement. 

# Extraction des données sur les effectifs pour les années 2019, 2020 et 2021 
# On reprend le code de stats_descr_effectif 

effectifs_ecoles = pd.read_csv("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ecoles-effectifs-nb_classes/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B", sep = ";", header = 0)
effectifs_ecoles_paris = effectifs_ecoles[
   (effectifs_ecoles['Rentrée scolaire'].isin([2019, 2020, 2021])) &
   (effectifs_ecoles["Région académique"] == "ILE-DE-FRANCE") &
   # petit bug ici avec le _192021 (effectifs_ecoles_192021['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]
   (effectifs_ecoles['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]

## Renommer les colonnes

#Plus simplement utiliser le module unidecode 

effectifs_ecoles_paris.columns = [unidecode(col).lower().replace(" ", "_").replace("d'", "").replace("'", "") for col in effectifs_ecoles_paris.columns]

# Total nombre d'élèves par arrondissement par année
nb_eleve_arrondissement_annee = effectifs_ecoles_paris.groupby(['code_postal', 'rentree_scolaire'])['nombre_total_eleves'].sum().reset_index()


# Extraction des données dans les dataframes pop_2019, pop_2020 et pop_2021 pour ne conserver que les arrondissements et la proportion de T3

pop_2019 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2019.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2020 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2020.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2021 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2021.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)


# En 2019
# On convertit la colonne ARM et NBPI en type numérique
pop_2019['ARM'] = pd.to_numeric(pop_2019['ARM'], errors='coerce')
pop_2019['NBPI'] = pd.to_numeric(pop_2019['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2019 = pop_2019[pop_2019['ARM'].between(75101, 75120)].copy()

# Étape 2 : On calcule la proportion de T3
paris_data_2019.loc[:, 'is_T3'] = paris_data_2019['NBPI'] >= 3

# Création de la colonne 'is_bac+5' en fonction de DIPLM
paris_data_2019.loc[:, 'is_bac+5'] = paris_data_2019['DIPLM'].isin(['18', '19'])

# Affichage des premières lignes pour vérifier
print(paris_data_2019[['ARM', 'is_T3', 'is_bac+5']].head())

pop_2019_reg = (
    paris_data_2019.groupby('ARM')[['is_T3', 'is_bac+5']]  # Ajout des doubles crochets pour spécifier les colonnes
    .mean()
    .reset_index()
    .rename(columns={'is_T3': 'Proportion_3_pieces_ou_plus', 'is_bac+5': 'Proportion_bac+5'})
)

print(pop_2019_reg)

# En 2020
# On convertit la colonne ARM et NBPI en type numérique
pop_2020['ARM'] = pd.to_numeric(pop_2020['ARM'], errors='coerce')
pop_2020['NBPI'] = pd.to_numeric(pop_2020['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2020 = pop_2020[pop_2020['ARM'].between(75101, 75120)].copy()

# Étape 2 : On calcule la proportion de T3
paris_data_2020.loc[:, 'is_T3'] = paris_data_2020['NBPI'] >= 3

# Création de la colonne 'is_bac+5' en fonction de DIPLM
paris_data_2020.loc[:, 'is_bac+5'] = paris_data_2020['DIPLM'].isin(['18', '19'])

# Affichage des premières lignes pour vérifier
print(paris_data_2020[['ARM', 'is_T3', 'is_bac+5']].head())

pop_2020_reg = (
    paris_data_2020.groupby('ARM')[['is_T3', 'is_bac+5']]  # Ajout des doubles crochets pour spécifier les colonnes
    .mean()
    .reset_index()
    .rename(columns={'is_T3': 'Proportion_3_pieces_ou_plus', 'is_bac+5': 'Proportion_bac+5'})
)

print(pop_2020_reg)

# En 2021
# On convertit la colonne ARM et NBPI en type numérique
pop_2021['ARM'] = pd.to_numeric(pop_2021['ARM'], errors='coerce')
pop_2021['NBPI'] = pd.to_numeric(pop_2021['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2021 = pop_2021[pop_2021['ARM'].between(75101, 75120)].copy()

# Étape 2 : On calcule la proportion de T3
paris_data_2021.loc[:, 'is_T3'] = paris_data_2021['NBPI'] >= 3

# Création de la colonne 'is_bac+5' en fonction de DIPLM
paris_data_2021.loc[:, 'is_bac+5'] = paris_data_2021['DIPLM'].isin(['18', '19'])

# Affichage des premières lignes pour vérifier
print(paris_data_2021[['ARM', 'is_T3', 'is_bac+5']].head())

pop_2021_reg = (
    paris_data_2021.groupby('ARM')[['is_T3', 'is_bac+5']]  # Ajout des doubles crochets pour spécifier les colonnes
    .mean()
    .reset_index()
    .rename(columns={'is_T3': 'Proportion_3_pieces_ou_plus', 'is_bac+5': 'Proportion_bac+5'})
)

print(pop_2021_reg)

# On extrait la proportion d'adultes âgés entre 30 et 40 pour chaque arrondissement

# En 2019
# Liste des codes INSEE pour Paris (en fonction des arrondissements et autres zones spécifiques)
codes_insee_paris = [
    75101, 75102, 75103, 75104, 75105, 75106, 75107,
    75108, 75109, 75110, 75111, 75112, 75113, 75114, 75115,
    75116, 75117, 75118, 75119, 75120
]

df_ages_2021 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/TD_POP1B_2021.csv', delimiter=';', encoding='latin1')
df_ages_2020 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/TD_POP1B_2020.csv', delimiter=';', encoding='latin1')
df_ages_2019 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/BTT_TD_POP1B_2019.csv', delimiter=';', encoding='latin1')

# On filtre les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages_2019 = df_ages_2019[df_ages_2019['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100', 'SEXE', 'NB']]

age_30_40_2019 = df_paris_ages_2019[(df_paris_ages_2019['AGED100'] >= 30) & (df_paris_ages_2019['AGED100'] <= 40)]

# On calcule l'effectif total de la population pour chaque arrondissement
total_population_per_arrondissement_2019 = df_paris_ages_2019.groupby('CODGEO')['NB'].sum()

# On calcule l'effectif des personnes âgées de 30 à 40 ans pour chaque arrondissement
population_30_40_per_arrondissement_2019 = age_30_40_2019.groupby('CODGEO')['NB'].sum()

# On Calcule la proportion de personnes âgées de 30 à 40 ans par rapport au total de la population
proportion_30_40_2019 = (population_30_40_per_arrondissement_2019 / total_population_per_arrondissement_2019).reset_index()

# On renomme la colonne pour la proportion
proportion_30_40_2019 = proportion_30_40_2019.rename(columns={'NB': 'Proportion_30_40_Ans'})

# On affiche le résultat
print(proportion_30_40_2019)

# En 2020

# On filtre les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages_2020 = df_ages_2020[df_ages_2020['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100', 'SEXE', 'NB']]

age_30_40_2020 = df_paris_ages_2020[(df_paris_ages_2020['AGED100'] >= 30) & (df_paris_ages_2020['AGED100'] <= 40)]

# On calcule l'effectif total de la population pour chaque arrondissement
total_population_per_arrondissement_2020 = df_paris_ages_2020.groupby('CODGEO')['NB'].sum()

# On calcule l'effectif des personnes âgées de 30 à 40 ans pour chaque arrondissement
population_30_40_per_arrondissement_2020 = age_30_40_2020.groupby('CODGEO')['NB'].sum()

# On Calcule la proportion de personnes âgées de 30 à 40 ans par rapport au total de la population
proportion_30_40_2020 = (population_30_40_per_arrondissement_2020 / total_population_per_arrondissement_2020).reset_index()

# On renomme la colonne pour la proportion
proportion_30_40_2020 = proportion_30_40_2020.rename(columns={'NB': 'Proportion_30_40_Ans'})

# On affiche le résultat
print(proportion_30_40_2020)

# En 2021

# On filtre les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages_2021 = df_ages_2021[df_ages_2021['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100', 'SEXE', 'NB']]

age_30_40_2021 = df_paris_ages_2021[(df_paris_ages_2021['AGED100'] >= 30) & (df_paris_ages_2021['AGED100'] <= 40)]

# On calcule l'effectif total de la population pour chaque arrondissement
total_population_per_arrondissement_2021 = df_paris_ages_2021.groupby('CODGEO')['NB'].sum()

# On calcule l'effectif des personnes âgées de 30 à 40 ans pour chaque arrondissement
population_30_40_per_arrondissement_2021 = age_30_40_2021.groupby('CODGEO')['NB'].sum()

# On Calcule la proportion de personnes âgées de 30 à 40 ans par rapport au total de la population
proportion_30_40_2021 = (population_30_40_per_arrondissement_2021 / total_population_per_arrondissement_2021).reset_index()

# On renomme la colonne pour la proportion
proportion_30_40_2021 = proportion_30_40_2021.rename(columns={'NB': 'Proportion_30_40_Ans'})

# On affiche le résultat
print(proportion_30_40_2021)


# On crée le dataframe pour la régression 2019 en joignant les différents dataframes
# On filtre nb_eleve_arrondissement_annee pour l'année 2019 
nb_eleve_2019 = nb_eleve_arrondissement_annee[nb_eleve_arrondissement_annee['rentree_scolaire'] == 2019 ]

# On sélectionne les colonnes nécessaires pour le nombre total d'élèves
nb_eleve_2019 = nb_eleve_2019[['code_postal', 'nombre_total_eleves']]

# On harmonise les colonnes pour la jointure
nb_eleve_2019['code_postal'] = nb_eleve_2019['code_postal'] + 100
nb_eleve_2019 = nb_eleve_2019.rename(columns={'code_postal': 'CODGEO'})
pop_2019_reg =  pop_2019_reg.rename(columns={'ARM': 'CODGEO'})

# On joint nb_eleve_2019 avec proportion_30_40_2019 en fonction du CODGEO
merged_data_2019 = pd.merge(nb_eleve_2019, proportion_30_40_2019, 
                       on='CODGEO', how='left')

# On joint nb_eleve_2019 avec pop_2019_reg en fonction du CODGEO
merged_data_2019 = pd.merge(
    merged_data_2019,
    pop_2019_reg[['CODGEO', 'Proportion_3_pieces_ou_plus', 'Proportion_bac+5']],
    on='CODGEO',
    how='left'
)

# print(merged_data_2019.head(2))

# On réalise la régression pour l'année 2019
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
merged_data_clean = merged_data_2019.dropna(
    subset=['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']
)

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = merged_data_clean[['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']]

# On ajoute une constante
X = sm.add_constant(X)

# Variable dépendante (nombre_total_eleves)
y = merged_data_clean['nombre_total_eleves']

# Modèle de régression linéaire
model_2019 = sm.OLS(y, X)
results = model_2019.fit()

# Résumé des résultats
print(results.summary())

# On crée le dataframe pour la régression 2020 en joignant les différents dataframes
# On filtre nb_eleve_arrondissement_annee pour l'année 2020 
nb_eleve_2020 = nb_eleve_arrondissement_annee[nb_eleve_arrondissement_annee['rentree_scolaire'] == 2020 ]

# On sélectionne les colonnes nécessaires pour le nombre total d'élèves
nb_eleve_2020 = nb_eleve_2020[['code_postal', 'nombre_total_eleves']]

# On harmonise les colonnes pour la jointure
nb_eleve_2020['code_postal'] = nb_eleve_2020['code_postal'] + 100
nb_eleve_2020 = nb_eleve_2020.rename(columns={'code_postal': 'CODGEO'})
pop_2020_reg =  pop_2020_reg.rename(columns={'ARM': 'CODGEO'})

# On joint nb_eleve_2020 avec proportion_30_40_2020 en fonction du CODGEO
merged_data_2020 = pd.merge(nb_eleve_2020, proportion_30_40_2020, 
                       on='CODGEO', how='left')

# On joint nb_eleve_2020 avec pop_2020_reg en fonction du CODGEO
merged_data_2020 = pd.merge(
    merged_data_2020,
    pop_2020_reg[['CODGEO', 'Proportion_3_pieces_ou_plus', 'Proportion_bac+5']],
    on='CODGEO',
    how='left'
)

# On réalise la régression pour l'année 2020
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
merged_data_clean = merged_data_2020.dropna(
    subset=['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']
)

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = merged_data_clean[['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']]

# On ajoute une constante
X = sm.add_constant(X)

# Variable dépendante (nombre_total_eleves)
y = merged_data_clean['nombre_total_eleves']

# Modèle de régression linéaire
model_2020 = sm.OLS(y, X)
results = model_2020.fit()

# Résumé des résultats
print(results.summary())

# On crée le dataframe pour la régression 2021 en joignant les différents dataframes
# On filtre nb_eleve_arrondissement_annee pour l'année 2021 
nb_eleve_2021 = nb_eleve_arrondissement_annee[nb_eleve_arrondissement_annee['rentree_scolaire'] == 2021 ]

# On sélectionne les colonnes nécessaires pour le nombre total d'élèves
nb_eleve_2021 = nb_eleve_2021[['code_postal', 'nombre_total_eleves']]

# On harmonise les colonnes pour la jointure
nb_eleve_2021['code_postal'] = nb_eleve_2021['code_postal'] + 100
nb_eleve_2021 = nb_eleve_2021.rename(columns={'code_postal': 'CODGEO'})
pop_2021_reg =  pop_2021_reg.rename(columns={'ARM': 'CODGEO'})

# On joint nb_eleve_2021 avec proportion_30_40_2021 en fonction du CODGEO
merged_data_2021 = pd.merge(nb_eleve_2021, proportion_30_40_2021, 
                       on='CODGEO', how='left')

# On joint nb_eleve_2021 avec pop_2021_reg en fonction du CODGEO
merged_data_2021 = pd.merge(
    merged_data_2021,
    pop_2021_reg[['CODGEO', 'Proportion_3_pieces_ou_plus', 'Proportion_bac+5']],
    on='CODGEO',
    how='left'
)

# On réalise la régression pour l'année 2021
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
merged_data_clean = merged_data_2021.dropna(
    subset=['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']
)

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = merged_data_clean[['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']]

# On ajoute une constante
X = sm.add_constant(X)

# Variable dépendante (nombre_total_eleves)
y = merged_data_clean['nombre_total_eleves']

# Modèle de régression linéaire
model_2021 = sm.OLS(y, X)
results = model_2021.fit()

# Résumé des résultats
print(results.summary())
