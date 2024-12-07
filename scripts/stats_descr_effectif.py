#==== attention liste des modulesà installer dans son BASH
#pip install unidecode
#pip install py7zr geopandas openpyxl tqdm s3fs 
#pip install PyYAML xlrd
#pip install git+https://github.com/inseefrlab/cartiflette
#pip install urllib3==1.26.5 #cartiflette nécessite une version de urllib3 antérieure à la deuxième, il faut donc installer une ancienne version.

import matplotlib.pyplot as plt
import numpy as np
from unidecode import unidecode 
import matplotlib.ticker as mticker
import geopandas as gpd
from cartiflette import carti_download


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

# Total nombre d'élèves par arrondissement par année
nb_eleve_arrondissement_annee = effectifs_ecoles_paris.groupby(['code_postal', 'rentree_scolaire'])['nombre_total_eleves'].sum().reset_index()

## Pivot pour réorganiser les données
pivot_df = nb_eleve_arrondissement_annee.pivot(index='code_postal', columns='rentree_scolaire', values='nombre_total_eleves')
pivot_df['evolution_total'] = ((pivot_df[2021] - pivot_df[2019]) / pivot_df[2019]) * 100
pivot_df['evolution_2019_2020'] = ((pivot_df[2020] - pivot_df[2019]) / pivot_df[2019]) * 100
pivot_df['evolution_2020_2021'] = ((pivot_df[2021] - pivot_df[2020]) / pivot_df[2020]) * 100
pivot_df['proportion_2019_2020'] = pivot_df['evolution_2019_2020'] / pivot_df['evolution_total']
pivot_df['proportion_2020_2021'] = pivot_df['evolution_2020_2021'] / pivot_df['evolution_total']
pivot_df['evolution_total_niveau'] = (pivot_df[2021] - pivot_df[2019]) 
pivot_df['INSEE_COG'] = (pivot_df.index.astype(int)+ 100).astype(str)
pivot_df.index = pivot_df.index.astype(str)


pivot_df_sorted = pivot_df.sort_values(by='evolution_total', ascending=False)

# Proportion d'élèves par arrondissement par année

pivot_df.columns
pivot_df['effectifs_totaux_2019'] = pivot_df[2019].sum()
pivot_df['effectifs_totaux_2020'] = pivot_df[2020].sum()
pivot_df['effectifs_totaux_2021'] = pivot_df[2021].sum()
pivot_df['proportion_2019'] = pivot_df[2019] / pivot_df['effectifs_totaux_2019'] * 100
pivot_df['proportion_2020'] = pivot_df[2020] / pivot_df['effectifs_totaux_2020'] * 100
pivot_df['proportion_2021'] = pivot_df[2021] / pivot_df['effectifs_totaux_2021'] * 100

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

## Graphique : proportion d'élèves par arrondissement

proportion = [pivot_df[f"proportion_{annee}"] for annee in annees]
bar_width = 0.25
x = np.arange(len(arrondissement))

# Création de la figure et des sous-graphiques
fig, ax = plt.subplots(figsize=(10, 6))

# Histogrammes pour chaque année
for i, (annee, proportion) in enumerate(zip(annees, proportion)):
    ax.bar(x + i * bar_width, proportion, width=bar_width, label=f"Proportion {annee}")

# Ajout des labels et titres
ax.set_xticks(x + bar_width)
ax.set_xticklabels(arrondissement)
ax.set_xlabel("Arrondissements")
ax.set_ylabel("Proportion")
ax.set_title("Proportions d'élèves par arrondissement (2019 - 2021)")
ax.legend(title="Années")
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/proportion_effectifs.png")

#fig, axes = plt.subplots(1, len(annees), figsize=(15, 5), sharey=True)
#for i, annee in enumerate(annees):
#    proportions = pivot_df[f"proportion_{annee}"]
#    axes[i].bar(arrondissement, proportion, color=f"C{i}")
#    axes[i].set_title(f"Proportions en {annee}")
#    axes[i].set_xlabel("Arrondissements")
#    if i == 0:  # Ajouter un label pour l'axe Y uniquement sur le premier
#        axes[i].set_ylabel("Proportion")
#    axes[i].set_ylim(0, max(pivot_df[[f"proportion_{a}" for a in annees]].max().max() * 1.1, 0.3))  # Garde une échelle cohérente
#plt.tight_layout()
#plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/proportion_effectifs2.png")


#=============== Cartographie

petite_couronne = carti_download(
    crs=4326,
    values=["75", "92", "93", "94"],
    borders="COMMUNE_ARRONDISSEMENT",
    vectorfile_format="geojson",
    filter_by="DEPARTEMENT",
    source="EXPRESS-COG-CARTO-TERRITOIRE",
    year=2022,
)

petite_couronne.crs
petite_couronne = petite_couronne.to_crs(2154)
petite_couronne.crs



petite_couronne_count = petite_couronne.merge(pivot_df).to_crs(2154)

#Evol en niveau

aplat = petite_couronne_count.plot(column="evolution_total_niveau", cmap="Reds_r", legend=True)
aplat.set_axis_off()
aplat.set_title("Evolution du nombre d'élèves entre 2019 et 2021, par arrondissement (en milliers)",y=1.0, pad=14)
aplat

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/testt.png")


#evol en %

aplat = petite_couronne_count.plot(column="evolution_total", cmap="Reds_r", legend=True)
aplat.set_axis_off()
aplat.set_title("Evolution du nombre d'élèves entre 2019 et 2021, par arrondissement (en %)",y=1.0, pad=-14)
aplat

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/test5.png")