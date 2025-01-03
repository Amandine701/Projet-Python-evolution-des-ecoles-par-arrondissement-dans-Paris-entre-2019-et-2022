import pandas as pd
import statsmodels.api as sm
from unidecode import unidecode

# régression des effectifs par année et arrondissement sur une constante, certaines tranches d'âges (en âge d'avoir des enfants), et des effets fixes par arrondissement. 
# Etape 1 : on sélectionne les données nécessaires au sein de trois dataframes nb_eleve_arrondissement_annee, pop_all_years (extrait de la base logement), proportion_30_40_all_years (extrait de la base de recensement sur l'âge)
# Etape 2 : on fusionne les trois dataframes pour obtenir un dataframe unique 
# Etape 3 : on effectue la régression


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

nb_eleve_arrondissement_annee_reg = nb_eleve_arrondissement_annee

pop_2019 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2019.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2020 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2020.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2021 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2021.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)

# En 2019
# On convertit la colonne ARM et NBPI en type numérique
pop_2019['ARM'] = pd.to_numeric(pop_2019['ARM'], errors='coerce')
pop_2019['NBPI'] = pd.to_numeric(pop_2019['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2019_reg = pop_2019[pop_2019['ARM'].between(75101, 75120)].copy()

# On calcule la proportion de T3

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

# En 2020
# On convertit la colonne ARM et NBPI en type numérique
pop_2020['ARM'] = pd.to_numeric(pop_2020['ARM'], errors='coerce')
pop_2020['NBPI'] = pd.to_numeric(pop_2020['NBPI'], errors='coerce')

# On filtre pour les arrondissements parisiens (ARM entre 75101 et 75120)
paris_data_2020_reg = pop_2020[pop_2020['ARM'].between(75101, 75120)].copy()

# On calcule la proportion de T3
paris_data_2020_reg.loc[:, 'is_T3'] = paris_data_2020_reg['NBPI'] >= 3

# Création de la colonne 'is_bac+5' en fonction de DIPLM
paris_data_2020_reg.loc[:, 'is_bac+5'] = paris_data_2020_reg['DIPLM'].isin(['18', '19'])

# Affichage des premières lignes pour vérifier
print(paris_data_2020_reg[['ARM', 'is_T3', 'is_bac+5']].head())

pop_2020_reg = (
    paris_data_2020_reg.groupby('ARM')[['is_T3', 'is_bac+5']]  # Ajout des doubles crochets pour spécifier les colonnes
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

# on regroupe les dataframes pop_2019_reg, pop_2020_reg et pop_2021_reg en un seul dataframe

# Ajout de la colonne `rentree_scolaire`
pop_2019_reg['rentree_scolaire'] = 2019
pop_2020_reg['rentree_scolaire'] = 2020
pop_2021_reg['rentree_scolaire'] = 2021

# Regroupement des DataFrames
pop_all_years_reg = pd.concat([pop_2019_reg, pop_2020_reg, pop_2021_reg], ignore_index=True)

#---------------------------------Création du dataframe proportion_30_40_all_years (base de données recensement détaillant l'âge)----------------------------------

# On extrait la proportion d'adultes âgés entre 30 et 40 pour chaque arrondissement

df_ages_2021 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/TD_POP1B_2021.csv', delimiter=';', encoding='latin1')
df_ages_2020 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/TD_POP1B_2020.csv', delimiter=';', encoding='latin1')
df_ages_2019 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/BTT_TD_POP1B_2019.csv', delimiter=';', encoding='latin1')

# En 2019
# Liste des codes INSEE pour Paris (en fonction des arrondissements et autres zones spécifiques)
codes_insee_paris = [
    75101, 75102, 75103, 75104, 75105, 75106, 75107,
    75108, 75109, 75110, 75111, 75112, 75113, 75114, 75115,
    75116, 75117, 75118, 75119, 75120
]

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

# En 2020

# On filtre les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages_2020_reg = df_ages_2020[df_ages_2020['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100', 'SEXE', 'NB']]

age_30_40_2020_reg = df_paris_ages_2020_reg[(df_paris_ages_2020_reg['AGED100'] >= 30) & (df_paris_ages_2020_reg['AGED100'] <= 40)]

# On calcule l'effectif total de la population pour chaque arrondissement
total_population_per_arrondissement_2020_reg = df_paris_ages_2020_reg.groupby('CODGEO')['NB'].sum()

# On calcule l'effectif des personnes âgées de 30 à 40 ans pour chaque arrondissement
population_30_40_per_arrondissement_2020_reg = age_30_40_2020_reg.groupby('CODGEO')['NB'].sum()

# On Calcule la proportion de personnes âgées de 30 à 40 ans par rapport au total de la population
proportion_30_40_2020_reg = (population_30_40_per_arrondissement_2020_reg / total_population_per_arrondissement_2020_reg).reset_index()

# On renomme la colonne pour la proportion
proportion_30_40_2020_reg = proportion_30_40_2020_reg.rename(columns={'NB': 'Proportion_30_40_Ans'})

# On affiche le résultat
print(proportion_30_40_2020_reg)

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

# On regroupe les trois dataframes proportion_30_40_2021, proportion_30_40_2019 et proportion_30_40_2020 en créant une colonne rentree_scolaire pour distinguer l'année

# Ajout de la colonne `rentree_scolaire` pour chaque DataFrame
proportion_30_40_2019_reg['rentree_scolaire'] = 2019
proportion_30_40_2020_reg['rentree_scolaire'] = 2020
proportion_30_40_2021_reg['rentree_scolaire'] = 2021

# Concaténation des DataFrames
proportion_30_40_all_years_reg = pd.concat(
    [proportion_30_40_2019_reg, proportion_30_40_2020_reg, proportion_30_40_2021_reg],
    ignore_index=True
)

#--------------------------------------------Etape 2 : on fusionne les trois dataframes en un dataframe unqiue-------------------------


# On harmonise les colonnes pour la jointure
nb_eleve_arrondissement_annee_reg['code_postal'] = nb_eleve_arrondissement_annee_reg['code_postal'] + 100
nb_eleve_arrondissement_annee_reg = nb_eleve_arrondissement_annee.rename(columns={'code_postal': 'CODGEO'})
pop_all_years_reg = pop_all_years_reg.rename(columns={'ARM': 'CODGEO'})

# On joint nb_eleve_arrondissement_annee avec proportion_30_40_all_years en fonction du CODGEO et de l'année
merged_data_reg_temporaire = pd.merge(
    nb_eleve_arrondissement_annee_reg,
    proportion_30_40_all_years_reg,
    on=['CODGEO', 'rentree_scolaire'],
    how='inner'
)

# On joint merged_data avec pop_all_years en fonction du CODGEO et rentree_scolaire
merged_data_reg = pd.merge(
    merged_data_reg_temporaire,
    pop_all_years_reg,
    on=['CODGEO', 'rentree_scolaire'],
    how='inner'
)

# print(merged_data_reg)

#--------------------------Etape 3 : on réalise la régression avec indicatrices arrondissements--------------------------------------
# On réalise la régression 
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
merged_data_reg_clean = merged_data_reg.dropna(
    subset=['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']
)

# Création des indicatrices pour CODGEO (arrondissements)
indicatrices_codgeo = pd.get_dummies(merged_data_reg_clean['CODGEO'], prefix='arrondissement').astype(int)

# Création des indicatrices pour rentree_scolaire (années)
indicatrices_annees = pd.get_dummies(merged_data_reg_clean['rentree_scolaire'], prefix='annee').astype(int)

# Supprimer l'indicatrice du 20ᵉ arrondissement et de l'année 2021
indicatrices_codgeo = indicatrices_codgeo.drop(columns=['arrondissement_75120'], errors='ignore')
indicatrices_annees = indicatrices_annees.drop(columns=['annee_2021'], errors='ignore')

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = pd.concat([
    merged_data_reg_clean[['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']],
    indicatrices_codgeo,
    indicatrices_annees
], axis=1)


# On ajoute une constante
X = sm.add_constant(X)

# Variable dépendante (nombre_total_eleves)
y = merged_data_reg_clean['nombre_total_eleves']

# Modèle de régression linéaire
model_effectifs_absolus = sm.OLS(y, X)
results = model_effectifs_absolus.fit()

# Résumé des résultats
print(results.summary())


#--------------------------Etape 4 : on réalise la régression avec indicatrices zones--------------------------------------
# On réalise la régression 
# On supprime les lignes avec des valeurs manquantes pour les variables explicatives uniquement
merged_data_reg_clean = merged_data_reg.dropna(
    subset=['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']
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
merged_data_reg_clean['CODGEO'] = merged_data_reg_clean['CODGEO'].astype(str)

# Appliquer la fonction de classification
merged_data_reg_clean['zone_geographique'] = merged_data_reg_clean['CODGEO'].apply(classify_arrondissement)

# Créer des indicatrices pour les zones géographiques
indicatrices_zones = pd.get_dummies(merged_data_reg_clean['zone_geographique'], prefix='zone').astype(int)

# Exemple de suppression d'une indicatrice 
# Ici, nous supprimons la colonne "zone_centre" pour éviter une colinéarité si nécessaire.
indicatrices_zones = indicatrices_zones.drop(columns=['zone_centre'], errors='ignore')

# On définit les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = pd.concat([
    merged_data_reg_clean[['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']],
    indicatrices_zones,
], axis=1)


# On ajoute une constante
X = sm.add_constant(X)

# Variable dépendante (nombre_total_eleves)
y = merged_data_reg_clean['nombre_total_eleves']

# Modèle de régression linéaire
model_effectifs_absolus_zone = sm.OLS(y, X)
results = model_effectifs_absolus_zone.fit()

# Résumé des résultats
print(results.summary())
#--------------------------Etape 5 : régression lasso----------------------------------------------------------------------
# Conclusion : toutes les variables sont significatives

from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Suppression des lignes avec des valeurs manquantes pour les variables explicatives uniquement
merged_data_reg_clean = merged_data_reg.dropna(
    subset=['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']
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
merged_data_reg_clean['CODGEO'] = merged_data_reg_clean['CODGEO'].astype(str)

# Appliquer la fonction de classification
merged_data_reg_clean['zone_geographique'] = merged_data_reg_clean['CODGEO'].apply(classify_arrondissement)

# Créer des indicatrices pour les zones géographiques
indicatrices_zones = pd.get_dummies(merged_data_reg_clean['zone_geographique'], prefix='zone').astype(int)

# Exemple de suppression d'une indicatrice 
# Ici, nous supprimons la colonne "zone_centre" pour éviter une colinéarité si nécessaire.
indicatrices_zones = indicatrices_zones.drop(columns=['zone_centre'], errors='ignore')

# Définir les variables explicatives (on exclut CODGEO et nombre_total_eleves)
X = pd.concat([
    merged_data_reg_clean[['Proportion_3_pieces_ou_plus', 'Proportion_bac+5', 'Proportion_30_40_Ans']],
    indicatrices_zones,
], axis=1)

# Variable dépendante (nombre_total_eleves)
y = merged_data_reg_clean['nombre_total_eleves']

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardiser les données (requis pour la régression Lasso)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Régularisation Lasso
lasso_model = Lasso(alpha=0.1)  # Vous pouvez ajuster alpha pour contrôler la régularisation
lasso_model.fit(X_train_scaled, y_train)

# Prédictions sur les données de test
y_pred = lasso_model.predict(X_test_scaled)

# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Afficher les résultats
print("Mean Squared Error (MSE):", mse)
print("R-squared (R²):", r2)

# Afficher les coefficients Lasso
coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": lasso_model.coef_
})
print(coef_df)