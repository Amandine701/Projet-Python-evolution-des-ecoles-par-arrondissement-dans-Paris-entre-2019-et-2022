import matplotlib.pyplot as plt
import pandas as pd

# Liste des codes INSEE pour Paris (en fonction des arrondissements et autres zones spécifiques)
codes_insee_paris = [
    75101, 75102, 75103, 75104, 75105, 75106, 75107,
    75108, 75109, 75110, 75111, 75112, 75113, 75114, 75115,
    75116, 75117, 75118, 75119, 75120
]
codes_insee_paris_str = [str(code) for code in codes_insee_paris]

df_ages_2021 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/TD_POP1B_2021.csv', delimiter=';', encoding='latin1')
df_ages_2020 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/TD_POP1B_2020.csv', delimiter=';', encoding='latin1')
df_ages_2019 = pd.read_csv('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/BTT_TD_POP1B_2019.csv', delimiter=';', encoding='latin1')


# Filtrer les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
#df_paris_ages = df_ages_2019[df_ages_2019['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100']]


# Définir les bornes et les libellés des tranches d'âge
bins = [0, 2, 5, 11, 15, 18, 22] + list(range(23, 101, 4)) + [float('inf')]
labels = [
    '0-2 ans', '3-5 ans', '6-11 ans', '12-15 ans', '16-18 ans', '18-22 ans'
] + [f"{i}-{i+3} ans" for i in range(23, 100, 4)] + ['100 ans et plus']


# Création d'une fonction pour tracer une pyramide des âges pour chaque arrondissement (en regroupant les sexes)
def plot_age_pyramid_for_arrondissement(annee, arrondissement_code):
    df_arrondissement = globals()[f"df_paris_{annee}"] 
    # Filtrage des données pour l'arrondissement
    df_arrondissement = df_arrondissement[df_arrondissement['CODGEO'] == arrondissement_code]
    
    # Comptage du nombre d'individus dans chaque tranche d'âge (sans séparer par sexe)
    age_distribution = df_arrondissement.groupby('tranche_age', observed = False)['NB'].sum()
    
    # Tracé la pyramide des âges
    age_distribution.plot(kind='barh', color='lightblue', figsize=(10, 6))
    
    # Ajout des labels et un titre
    plt.xlabel('Nombre d\'individus')
    plt.ylabel('Tranches d\'âge')
    plt.title(f'Pyramide des âges pour l\'arrondissement {arrondissement_code}')
    plt.show()

# Pyramide des âges en 2019

# Transformer la colonne 'codgeo' en chaîne de caractères
df_ages_2019['CODGEO'] = df_ages_2019['CODGEO'].astype(str)

# Filtrer les lignes correspondant à Paris
df_paris_2019 = df_ages_2019[df_ages_2019['CODGEO'].isin(codes_insee_paris_str)]

# Créer une colonne 'tranche_age' dans le dataframe en fonction de 'AGED100'
df_paris_2019['tranche_age'] = pd.cut(df_ages_2019['AGED100'], bins=bins, labels=labels, right=False)

# Boucle pour tracer la pyramide des âges pour chaque arrondissement
for code in codes_insee_paris:
    plot_age_pyramid_for_arrondissement(2019, str(code))
    # Enregistrer le graphique dans un fichier
    plt.savefig(f'/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/Pyramides des âges 2019/pyramide_age_{code}_2019.png')
    plt.close()  # on ferme la figure pour éviter une accumulation de graphiques


# Pyramide des âges en 2020

# Transformer la colonne 'codgeo' en chaîne de caractères
df_ages_2020['CODGEO'] = df_ages_2020['CODGEO'].astype(str)

# Filtrer les lignes correspondant à Paris
df_paris_2020 = df_ages_2020[df_ages_2020['CODGEO'].isin(codes_insee_paris_str)]

# Créer une colonne 'tranche_age' dans le dataframe en fonction de 'AGED100'
df_paris_2020['tranche_age'] = pd.cut(df_ages_2020['AGED100'], bins=bins, labels=labels, right=False)

# Boucle pour tracer la pyramide des âges pour chaque arrondissement
for code in codes_insee_paris:
    plot_age_pyramid_for_arrondissement(2020, str(code))
    # Enregistrer le graphique dans un fichier
    plt.savefig(f'/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/Pyramides des âges 2020/pyramide_age_{code}_2020.png')
    plt.close()  # on ferme la figure pour éviter une accumulation de graphiques


# Pyramide des âges en 2021

# Transformer la colonne 'codgeo' en chaîne de caractères
df_ages_2021['CODGEO'] = df_ages_2021['CODGEO'].astype(str)

# Filtrer les lignes correspondant à Paris
df_paris_2021 = df_ages_2021[df_ages_2021['CODGEO'].isin(codes_insee_paris_str)]

# Créer une colonne 'tranche_age' dans le dataframe en fonction de 'AGED100'
df_paris_2021['tranche_age'] = pd.cut(df_ages_2021['AGED100'], bins=bins, labels=labels, right=False)

# Boucle pour tracer la pyramide des âges pour chaque arrondissement
for code in codes_insee_paris:
    plot_age_pyramid_for_arrondissement(2021, str(code))
    # Enregistrer le graphique dans un fichier
    plt.savefig(f'/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/Pyramides des âges 2021/pyramide_age_{code}_2021.png')
    # on ferme la figure pour éviter une accumulation de graphiques


#==== Pyramides des âges globales


Pyramid_2019 =df_paris_2019.groupby('tranche_age')['NB'].sum()
Pyramid_2020 =df_paris_2020.groupby('tranche_age')['NB'].sum()
Pyramid_2021 =df_paris_2021.groupby('tranche_age')['NB'].sum()
Pyramide_ecart = Pyramid_2021 - Pyramid_2019

df = Pyramide_ecart.to_frame(name="Effectifs")

df.plot(kind='barh', color='darkblue', figsize=(10, 6), title = "Evolution de la pyramide des âges entre 2019 et 2021", ylabel = "Tranche d'âge") 

# Ajout des labels et un titre
plt.savefig('/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/Pyramide_Paris_ecart1921.png')

