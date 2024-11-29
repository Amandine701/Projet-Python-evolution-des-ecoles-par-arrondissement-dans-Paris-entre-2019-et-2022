import matplotlib.pyplot as plt
import numpy as np
from unidecode import unidecode #dans le bash pip install unidecode
import matplotlib.ticker as mticker

# Base de données effectifs_ecoles ---------
## Ne garde que les rentrées scolaires 2019, 2020, 2021 et Paris (via le code postal)

effectifs_ecoles_paris = effectifs_ecoles[
    (effectifs_ecoles['Rentrée scolaire'].isin([2019, 2020, 2021])) &
    (effectifs_ecoles["Région académique"] == "ILE-DE-FRANCE") &
    # petit bug ici avec le _192021 (effectifs_ecoles_192021['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]
    (effectifs_ecoles['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]

## Renommer les colonnes

#Plus simplement utiliser le module unidecode 

effectifs_ecoles_paris.columns = [unidecode(col).lower().replace(" ", "_").replace("d'", "").replace("'", "") for col in effectifs_ecoles_paris.columns]

#colonnes = effectifs_ecoles_paris.columns
# Fonction pour renommer les colonnes 
#def nettoyer_nom_colonne(nom):
    # Supprimer les accents
#    nom_sans_accents = unidecode(nom)
    # Supprimer "d'" et les apostrophes
#    nom_sans_apostrophe = nom_sans_accents.replace("d'", "").replace("'", "")
    # Remplacer les espaces par des tirets bas
#    nom_sans_espaces = nom_sans_apostrophe.replace(" ", "_")
    # Transformer en minuscule pour uniformité (facultatif)
#    return nom_sans_espaces.lower()

# Renommer toutes les colonnes
#effectifs_ecoles_paris.columns = [nettoyer_nom_colonne(col) for col in colonnes]



# Total nombre d'élèves par arrondissement par année
nb_eleve_arrondissement_annee = effectifs_ecoles_paris.groupby(['code_postal', 'rentree_scolaire'])['nombre_total_eleves'].sum().reset_index()

## Pivot pour réorganiser les données
pivot_df = nb_eleve_arrondissement_annee.pivot(index='code_postal', columns='rentree_scolaire', values='nombre_total_eleves')
pivot_df['evolution_total'] = ((pivot_df[2021] - pivot_df[2019]) / pivot_df[2019]) * 100
pivot_df['evolution_2019_2020'] = ((pivot_df[2020] - pivot_df[2019]) / pivot_df[2019]) * 100
pivot_df['evolution_2020_2021'] = ((pivot_df[2021] - pivot_df[2020]) / pivot_df[2020]) * 100
pivot_df['proportion_2019_2020'] = pivot_df['evolution_2019_2020'] / pivot_df['evolution_total']
pivot_df['proportion_2020_2021'] = pivot_df['evolution_2020_2021'] / pivot_df['evolution_total']
pivot_df.index = pivot_df.index.astype(str)


pivot_df_sorted = pivot_df.sort_values(by='evolution_total', ascending=False)


# Graphique : Nombre total d'élèves pas arrondissement par année

arrondissement = pivot_df.index.str[-2:]#Je coupe pour n'avoir que les 2 chiffres.
annees = pivot_df[[2019,2020,2021]].columns
bar_width = 0.25  # Largeur des barres
x = np.arange(len(arrondissement))  # Positions des arrondissements sur l'axe X

plt.figure(figsize=(10, 6))

for i, annee in enumerate(annees):
    plt.bar(x + i * bar_width, pivot_df[annee], width=bar_width, label=f"{annee}") #j'enlève le "Année" qui apparaît déjà dans le titre de la légende"

plt.title("Nombre d'élèves par arrondissement et par année")
plt.xlabel("Arrondissement")
plt.ylabel("Nombre d'élèves")
plt.xticks(x + bar_width, arrondissement, rotation=45)  # Centrer les labels des arrondissements 
plt.legend(title="Année")
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/nb_élève_par_annee.png")

# Graphique : Evolution du nombre d'élèves par arrondissement classée

plt.figure(figsize=(10, 6))
plt.bar(pivot_df_sorted.index.str[-2:], pivot_df_sorted['evolution_total'], color='skyblue') #Je garde que les 2 numéros du code postale
plt.xlabel('Arrondissement', fontsize=12)
plt.ylabel('Évolution en % (2019-2021)', fontsize=12)
plt.title('Évolution en % du Nombre d’élèves (2019 à 2021)', fontsize=14)
plt.xticks(rotation=45) #à enlever éventuellement
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/evolution_nb_eleve_par_arrondissement.png")

# Graphique : Evolution du nombre d'élèves par arrondissement avec contribution 2020, classée

x = np.arange(len(pivot_df_sorted))  # Position des barres
width = 0.6

plt.figure(figsize=(12, 6))
plt.bar(
    x,
    height=pivot_df_sorted['evolution_total'],  # Hauteur totale
    width=width,
    color='skyblue',
    label='Total'
)
plt.bar(
    x,
    height=pivot_df_sorted['evolution_total'] * pivot_df_sorted['proportion_2019_2020'],
    width=width,
    color='orange',
    label='Contribution de 2020'
)
plt.xlabel('Arrondissements', fontsize=12)
plt.ylabel('Evolution en %', fontsize=12)
plt.title("Évolution Totale du Nombre d'Eleves entre 2019 et 2021", fontsize=14)
plt.xticks(x, pivot_df_sorted.index.str[-2:], rotation=45) #idem que 2 chiffres pour l'arrondissement #à enlever éventuellement la rotation
plt.legend()
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/evolution_avec_contrib.png")



#=============== Cartographie
# Dans son bash : pip install cartiflette

import geopandas as gpd
from cartiflette import carti_download

# 1. Fonds communaux
contours_villes_arrt = carti_download(
    values=["75"],
    crs=4326,
    borders="COMMUNE_ARRONDISSEMENT",
    filter_by="DEPARTEMENT",
    source="EXPRESS-COG-CARTO-TERRITOIRE",
    year=2022,
)

# 2. Départements
departements = contours_villes_arrt.dissolve("INSEE_DEP")

departements['INSEE_COM'].unique()


velib_data = "https://opendata.paris.fr/explore/dataset/velib-emplacement-des-stations/download/?format=geojson&timezone=Europe/Berlin&lang=fr"
stations = gpd.read_file(velib_data)
stations.head(20)

ax = stations.sample(200).plot(color="red")
contours_villes_arrt.boundary.plot(ax=ax, edgecolor="k", linewidth=0.5)
departements.boundary.plot(ax=ax, edgecolor="blue", linewidth=1)
ax.set_axis_off()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/test.png")

from cartiflette import carti_map

carti_map(
    geo=contours_villes_arrt,
    df=pivot_df,
    id_geo='id',
    id_data='code_postal',
    column='evolution_total',
    legend=True,
    palette='Blues',        # Palette de couleurs
    title='test'
)
import cartiflette
print(dir(cartiflette))

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/testZ.png")

import geopandas as gpd
import matplotlib.pyplot as plt

geo_paris = gpd.read_file("paris.geojson")

# Visualiser les données avec une colonne spécifique
geo_paris.plot(column='population', legend=True, cmap='Blues')