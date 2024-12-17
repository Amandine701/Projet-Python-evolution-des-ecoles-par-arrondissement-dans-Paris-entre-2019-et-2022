import pandas as pd
import statsmodels.api as sm
from unidecode import unidecode


# régression des effectifs par année et arrondissement sur une constante, certaines tranches d'âges (en âge d'avoir des enfants), et des effets fixes par arrondissement. 
# Etape 1 : on sélectionne les données nécessaires au sein de trois dataframes nb_eleve_arrondissement_annee, pop_all_years (extrait de la base logement), proportion_30_40_all_years (extrait de la base de recensement sur l'âge)
# Etape 2 : on harmonise les dataframes
# Etape 3 : on crée un dataframe avec les ratios
# Etape 4 : on réalise la régression


#-------------------------------Etape 1-------------------------------------------------------------------
#------------------------------Création du dataframe nb_eleve_arrondissement_annee------------------------

# Extraction des données sur les effectifs pour les années 2019, 2020 et 2021 
# On extrait le dataframe nb_eleve_arrondissement_annee en reprenant le code du fichier stats_descr_effectif (lignes 19 à 33)

#--------------------------Création du dataframe pop_all_years (base de données logement)---------------------------------------------

# Extraction des données dans les dataframes pop_2019, pop_2020 et pop_2021 pour ne conserver que les arrondissements et la proportion de T3 et création du dataframe pop_all_years

effectifs_ecoles = pd.read_csv("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ecoles-effectifs-nb_classes/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B", sep = ";", header = 0)
effectifs_ecoles_paris = effectifs_ecoles[
    (effectifs_ecoles['Rentrée scolaire'].isin([2019, 2020, 2021])) &
    (effectifs_ecoles["Région académique"] == "ILE-DE-FRANCE") &
    # petit bug ici avec le _192021 (effectifs_ecoles_192021['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]
    (effectifs_ecoles['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]
effectifs_ecoles_paris.columns = [unidecode(col).lower().replace(" ", "_").replace("d'", "").replace("'", "") for col in effectifs_ecoles_paris.columns]

nb_eleve_arrondissement_annee = effectifs_ecoles_paris.groupby(['code_postal', 'rentree_scolaire'])['nombre_total_eleves'].sum().reset_index()

nb_eleve_arrondissement_annee_reg= nb_eleve_arrondissement_annee

pop_2019 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2019.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2021 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2021.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)

# En 2019
# On convertit la colonne ARM et NBPI en type numérique
pop_2019['ARM'] = pd.to_numeric(pop_2019['ARM'], errors='coerce')
pop_2019['NBPI'] = pd.to_numeric(pop_2019['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2019_reg = pop_2019[pop_2019['ARM'].between(75101, 75120)].copy()

# Étape 2 : On calcule la proportion de T3
paris_data_2019_reg.loc[:, 'is_T3'] = paris_data_2019_reg['NBPI'] >= 3

# Création de la colonne 'is_bac+5' en fonction de DIPLM
paris_data_2019_reg.loc[:, 'is_bac+5'] = paris_data_2019_reg['DIPLM'].isin(['18', '19'])


# Affichage des premières lignes pour vérifier
print(paris_data_2019_reg[['ARM', 'is_T3', 'is_bac+5']].head())

pop_2019_reg = (
    paris_data_2019_reg.groupby('ARM')[['is_T3', 'is_bac+5']]  # Ajout des doubles crochets pour spécifier les colonnes
    .mean()
    .reset_index()
    .rename(columns={'is_T3': 'Proportion_3_pieces_ou_plus', 'is_bac+5': 'Proportion_bac+5'})
)

print(pop_2019_reg)

# En 2021
# On convertit la colonne ARM et NBPI en type numérique
pop_2021['ARM'] = pd.to_numeric(pop_2021['ARM'], errors='coerce')
pop_2021['NBPI'] = pd.to_numeric(pop_2021['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2021_reg = pop_2021[pop_2021['ARM'].between(75101, 75120)].copy()

# Étape 2 : On calcule la proportion de T3
paris_data_2021_reg.loc[:, 'is_T3'] = paris_data_2021_reg['NBPI'] >= 3

# Création de la colonne 'is_bac+5' en fonction de DIPLM
paris_data_2021_reg.loc[:, 'is_bac+5'] = paris_data_2021_reg['DIPLM'].isin(['18', '19'])

# Affichage des premières lignes pour vérifier
print(paris_data_2021_reg[['ARM', 'is_T3', 'is_bac+5']].head())

pop_2021_reg = (
    paris_data_2021_reg.groupby('ARM')[['is_T3', 'is_bac+5']]  # Ajout des doubles crochets pour spécifier les colonnes
    .mean()
    .reset_index()
    .rename(columns={'is_T3': 'Proportion_3_pieces_ou_plus', 'is_bac+5': 'Proportion_bac+5'})
)

print(pop_2021_reg)

#---------------------------------Création du dataframe proportion_30_40_all_years (base de données recensement détaillant l'âge)----------------------------------

# On extrait la proportion d'adultes âgés entre 30 et 40 pour chaque arrondissement

# En 2019
# Liste des codes INSEE pour Paris (en fonction des arrondissements et autres zones spécifiques)
codes_insee_paris = [
    75101, 75102, 75103, 75104, 75105, 75106, 75107,
    75108, 75109, 75110, 75111, 75112, 75113, 75114, 75115,
    75116, 75117, 75118, 75119, 75120
]

df_ages_2021 = pd.read_csv('extracted_files/TD_POP1B_2021.csv', delimiter=';', encoding='latin1')
df_ages_2020 = pd.read_csv('extracted_files/TD_POP1B_2020.csv', delimiter=';', encoding='latin1')
df_ages_2019 = pd.read_csv('extracted_files/BTT_TD_POP1B_2019.csv', delimiter=';', encoding='latin1')

# On filtre les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages_2019_reg = df_ages_2019[df_ages_2019['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100', 'SEXE', 'NB']]

age_30_40_2019_reg = df_paris_ages_2019_reg[(df_paris_ages_2019_reg['AGED100'] >= 30) & (df_paris_ages_2019_reg['AGED100'] <= 40)]

# On calcule l'effectif total de la population pour chaque arrondissement
total_population_per_arrondissement_2019_reg = df_paris_ages_2019_reg.groupby('CODGEO')['NB'].sum()

# On calcule l'effectif des personnes âgées de 30 à 40 ans pour chaque arrondissement
population_30_40_per_arrondissement_2019_reg = age_30_40_2019_reg.groupby('CODGEO')['NB'].sum()

# On Calcule la proportion de personnes âgées de 30 à 40 ans par rapport au total de la population
proportion_30_40_2019_reg = (population_30_40_per_arrondissement_2019_reg / total_population_per_arrondissement_2019_reg).reset_index()

# On renomme la colonne pour la proportion
proportion_30_40_2019_reg = proportion_30_40_2019_reg.rename(columns={'NB': 'Proportion_30_40_Ans'})

# On affiche le résultat
print(proportion_30_40_2019_reg)

# En 2021

# On filtre les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages_2021_reg = df_ages_2021[df_ages_2021['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100', 'SEXE', 'NB']]

age_30_40_2021_reg = df_paris_ages_2021_reg[(df_paris_ages_2021_reg['AGED100'] >= 30) & (df_paris_ages_2021_reg['AGED100'] <= 40)]

# On calcule l'effectif total de la population pour chaque arrondissement
total_population_per_arrondissement_2021_reg = df_paris_ages_2021_reg.groupby('CODGEO')['NB'].sum()

# On calcule l'effectif des personnes âgées de 30 à 40 ans pour chaque arrondissement
population_30_40_per_arrondissement_2021_reg = age_30_40_2021_reg.groupby('CODGEO')['NB'].sum()

# On Calcule la proportion de personnes âgées de 30 à 40 ans par rapport au total de la population
proportion_30_40_2021_reg = (population_30_40_per_arrondissement_2021_reg / total_population_per_arrondissement_2021_reg).reset_index()

# On renomme la colonne pour la proportion
proportion_30_40_2021_reg = proportion_30_40_2021_reg.rename(columns={'NB': 'Proportion_30_40_Ans'})

# On affiche le résultat
print(proportion_30_40_2021_reg)

#-----------------------------Etape 2 on harmonise les données-----------------------------------------------------------------------------
nb_eleve_arrondissement_annee_reg['code_postal'] = nb_eleve_arrondissement_annee_reg['code_postal'] + 100
nb_eleve_arrondissement_annee_reg = nb_eleve_arrondissement_annee.rename(columns={'code_postal': 'CODGEO'})
pop_2019_reg = pop_2019_reg.rename(columns={'ARM': 'CODGEO'})
pop_2021_reg = pop_2021_reg.rename(columns={'ARM': 'CODGEO'})


#-----------------------------Etape 3 on crée un dataframe avec les ratios-----------------------------------------------------------------------------
# On filtre les données pour 2019 et 2021 dans nb_eleve_arrondissement_annee
nb_eleves_2019_reg = nb_eleve_arrondissement_annee_reg[nb_eleve_arrondissement_annee['rentree_scolaire'] == 2019][['CODGEO', 'nombre_total_eleves']]
nb_eleves_2021_reg = nb_eleve_arrondissement_annee_reg[nb_eleve_arrondissement_annee['rentree_scolaire'] == 2021][['CODGEO', 'nombre_total_eleves']]

# On renomme les colonnes pour éviter les conflits
nb_eleves_2019_reg.rename(columns={'nombre_total_eleves': 'eleves_2019'}, inplace=True)
nb_eleves_2021_reg.rename(columns={'nombre_total_eleves': 'eleves_2021'}, inplace=True)

# On fusionne les données de 2019 et 2021 sur 'CODGEO'
eleves_ratio_reg = pd.merge(nb_eleves_2019_reg, nb_eleves_2021_reg, on='CODGEO')
eleves_ratio_reg['ratio_eleves'] = eleves_ratio_reg['eleves_2021'] / eleves_ratio_reg['eleves_2019']

# On fusionner pop_2019_reg et pop_2021_reg
pop_2019_reg.rename(columns={'ARM': 'CODGEO'}, inplace=True)  # Harmoniser les clés
pop_ratios_reg = pd.merge(pop_2019_reg, pop_2021_reg, on='CODGEO', suffixes=('_2019', '_2021'))

# On calcule les ratios pour 'Proportion_3_pieces_ou_plus' et 'Proportion_bac+5'
pop_ratios_reg['ratio_3_pieces'] = pop_ratios_reg['Proportion_3_pieces_ou_plus_2021'] / pop_ratios_reg['Proportion_3_pieces_ou_plus_2019']
pop_ratios_reg['ratio_bac+5'] = pop_ratios_reg['Proportion_bac+5_2021'] / pop_ratios_reg['Proportion_bac+5_2019']

# On fusionne proportion_30_40_2019_reg et proportion_30_40_2021_reg
proportion_ratios_reg = pd.merge(proportion_30_40_2019_reg, proportion_30_40_2021_reg, on='CODGEO', suffixes=('_2019', '_2021'))
proportion_ratios_reg['ratio_30_40'] = proportion_ratios_reg['Proportion_30_40_Ans_2021'] / proportion_ratios_reg['Proportion_30_40_Ans_2019']

# On fusionne tous les ratios dans un seul DataFrame final
final_ratios_reg = pd.merge(eleves_ratio_reg[['CODGEO', 'ratio_eleves']], pop_ratios_reg[['CODGEO', 'ratio_3_pieces', 'ratio_bac+5']], on='CODGEO')
final_ratios_reg = pd.merge(final_ratios_reg, proportion_ratios_reg[['CODGEO', 'ratio_30_40']], on='CODGEO')

# Afficher le DataFrame final
print(final_ratios_reg)

#--------------------------Etape 4 : on réalise la régression--------------------------------------

# On réalise la régression 
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
final_ratios_reg_clean = final_ratios_reg.dropna(
    subset=['ratio_3_pieces', 'ratio_bac+5', 'ratio_30_40','ratio_eleves' ]
)

# Création des indicatrices pour CODGEO (arrondissements)
indicatrices_codgeo = pd.get_dummies(final_ratios_reg_clean['CODGEO'], prefix='arrondissement').astype(int)

# Supprimer l'indicatrice du 20ᵉ arrondissement 
indicatrices_codgeo = indicatrices_codgeo.drop(columns=['arrondissement_75120'], errors='ignore')

# ON réinitialise les index avant de concaténer

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X_ratio = pd.concat([
    final_ratios_reg_clean[['ratio_3_pieces', 'ratio_bac+5', 'ratio_30_40']],
    indicatrices_codgeo,
], axis=1)


# On ajoute une constante
X_ratio = sm.add_constant(X_ratio)

# Variable dépendante (nombre_total_eleves)
y_ratio = final_ratios_reg_clean['ratio_eleves']

# Modèle de régression linéaire
model_avec_ratios = sm.OLS(y_ratio, X_ratio)
results = model_avec_ratios.fit()

# Résumé des résultats
print(results.summary())

#--------------------------Etape 5 : on réalise la régression avec indicatrices zones--------------------------------------
# On réalise la régression 
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
final_ratios_reg_clean = final_ratios_reg.dropna(
    subset=['ratio_3_pieces', 'ratio_bac+5', 'ratio_30_40','ratio_eleves' ]
)


# Fonction de classification des arrondissements en catégories géographiques
def classify_arrondissement(codgeo):
    arrondissement = int(codgeo[-2:])  # Extraire les deux derniers chiffres du code géographique
    if arrondissement in [1, 2, 3, 4]:
        return "centre"
    elif arrondissement in [10, 11, 19, 20]:
        return "nord-est"
    elif arrondissement in [8, 9, 17, 18]:
        return "nord-ouest"
    elif arrondissement in [5, 12, 13]:
        return "sud-est"
    elif arrondissement in [6, 7, 14, 15, 16]:
        return "sud-ouest"
    else:
        return "autre"
        
# Convertir CODGEO en chaîne
final_ratios_reg_clean['CODGEO'] = final_ratios_reg_clean['CODGEO'].astype(str)

# Appliquer la fonction de classification
final_ratios_reg_clean['zone_geographique'] = final_ratios_reg_clean['CODGEO'].apply(classify_arrondissement)

# Créer des indicatrices pour les zones géographiques
indicatrices_zones = pd.get_dummies(final_ratios_reg_clean['zone_geographique'], prefix='zone').astype(int)

#suppression d'une indicatrice 
# Ici, nous supprimons la colonne "zone_centre" pour éviter une colinéarité si nécessaire.
indicatrices_zones = indicatrices_zones.drop(columns=['zone_centre'], errors='ignore')

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = pd.concat([
    final_ratios_reg_clean[['ratio_bac+5', 'ratio_30_40','ratio_3_pieces']],
    indicatrices_zones,
], axis=1)


# On ajoute une constante
X = sm.add_constant(X)

# Variable dépendante (nombre_total_eleves)
y = final_ratios_reg_clean['ratio_eleves']

# Modèle de régression linéaire
model_effectifs_absolus = sm.OLS(y, X)
results = model_effectifs_absolus.fit()

# Résumé des résultats
print(results.summary())