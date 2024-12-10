import matplotlib.pyplot as plt

# Liste des codes INSEE pour Paris (en fonction des arrondissements et autres zones spécifiques)
codes_insee_paris = [
    75101, 75102, 75103, 75104, 75105, 75106, 75107,
    75108, 75109, 75110, 75111, 75112, 75113, 75114, 75115,
    75116, 75117, 75118, 75119, 75120
]

# Pyramide des âges en 2019

# Filtrer les données pour Paris (codes INSEE) et ne conserver que la variable AGED100
df_paris_ages = df_ages_2019[df_ages_2019['CODGEO'].isin(codes_insee_paris)][['CODGEO', 'AGED100']]

# Afficher les premières lignes du DataFrame filtré
print(df_paris_ages.head())

# Liste des codes INSEE pour Paris
codes_insee_paris = [
    75101, 75102, 75103, 75104, 75105, 75106, 75107,
    75108, 75109, 75110, 75111, 75112, 75113, 75114, 75115,
    75116, 75117, 75118, 75119, 75120
]

# Transformer les codes INSEE en chaînes de caractères
codes_insee_paris_str = [str(code) for code in codes_insee_paris]

# Transformer la colonne 'codgeo' en chaîne de caractères
df_ages_2019['CODGEO'] = df_ages_2019['CODGEO'].astype(str)

# Filtrer les lignes correspondant à Paris
df_paris = df_ages_2019[df_ages_2019['CODGEO'].isin(codes_insee_paris_str)]

# Afficher les premières lignes pour vérifier le résultat
print(df_paris.head())


# Définir les bornes et les libellés des tranches d'âge
bins = [0, 2, 5, 11, 15, 18, 22] + list(range(23, 101, 4)) + [float('inf')]
labels = [
    '0-2 ans', '3-5 ans', '6-11 ans', '12-15 ans', '16-18 ans', '18-22 ans'
] + [f"{i}-{i+3} ans" for i in range(23, 100, 4)] + ['100 ans et plus']

# Créer une colonne 'tranche_age' dans le dataframe en fonction de 'AGED100'
df_paris['tranche_age'] = pd.cut(df_ages_2019['AGED100'], bins=bins, labels=labels, right=False)


# Création d'une fonction pour tracer une pyramide des âges pour chaque arrondissement (en regroupant les sexes)
def plot_age_pyramid_for_arrondissement(arrondissement_code):
    # Filtrage des données pour l'arrondissement
    df_arrondissement = df_paris[df_paris['CODGEO'] == arrondissement_code]
    
    # Comptage du nombre d'individus dans chaque tranche d'âge (sans séparer par sexe)
    age_distribution = df_arrondissement.groupby('tranche_age')['NB'].sum()
    
    # Tracé la pyramide des âges
    age_distribution.plot(kind='barh', color='lightblue', figsize=(10, 6))
    
    # Ajout des labels et un titre
    plt.xlabel('Nombre d\'individus')
    plt.ylabel('Tranches d\'âge')
    plt.title(f'Pyramide des âges pour l\'arrondissement {arrondissement_code}')
    plt.show()

# Tracés
# Boucle pour tracer la pyramide des âges pour chaque arrondissement
for code in codes_insee_paris:
    plot_age_pyramid_for_arrondissement(str(code))
    # Enregistrer le graphique dans un fichier
    plt.savefig(f'pyramide_age_{code}_2019.png')
    plt.close()  # on ferme la figure pour éviter une accumulation de graphiques


# Pyramide des âges en 2020


# Transformer la colonne 'codgeo' en chaîne de caractères
df_ages_2020['CODGEO'] = df_ages_2020['CODGEO'].astype(str)

# Filtrer les lignes correspondant à Paris
df_paris_2020 = df_ages_2020[df_ages_2020['CODGEO'].isin(codes_insee_paris_str)]


# Créer une colonne 'tranche_age' dans le dataframe en fonction de 'AGED100'
df_paris_2020['tranche_age'] = pd.cut(df_ages_2020['AGED100'], bins=bins, labels=labels, right=False)


# Création d'une fonction pour tracer une pyramide des âges pour chaque arrondissement (en regroupant les sexes)
def plot_age_pyramid_for_arrondissement_2020(arrondissement_code):
    # Filtrage des données pour l'arrondissement
    df_arrondissement = df_paris_2020[df_paris_2020['CODGEO'] == arrondissement_code]
    
    # Comptage du nombre d'individus dans chaque tranche d'âge (sans séparer par sexe)
    age_distribution = df_arrondissement.groupby('tranche_age')['NB'].sum()
    
    # Tracé la pyramide des âges
    age_distribution.plot(kind='barh', color='lightblue', figsize=(10, 6))
    
    # Ajout des labels et un titre
    plt.xlabel('Nombre d\'individus')
    plt.ylabel('Tranches d\'âge')
    plt.title(f'Pyramide des âges pour l\'arrondissement {arrondissement_code} en 2020')
    plt.show()

# Tracés
# Boucle pour tracer la pyramide des âges pour chaque arrondissement
for code in codes_insee_paris:
    plot_age_pyramid_for_arrondissement_2020(str(code))
    # Enregistrer le graphique dans un fichier
    plt.savefig(f'pyramide_age_{code}_2020.png')
    plt.close()  # on ferme la figure pour éviter une accumulation de graphiques
