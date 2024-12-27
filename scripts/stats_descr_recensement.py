import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from unidecode import unidecode 
import matplotlib.ticker as mticker
import geopandas as gpd
from cartiflette import carti_download

pop_2019 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2019.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2020 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2020.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)
pop_2021 = pd.read_csv("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/extracted_files/FD_LOGEMTZA_2021.csv", sep = ";", header=0, encoding='UTF-8', low_memory=False)

# Recensement

## Sélectionne uniquement Paris
pop_2021_paris = pop_2021[
    (pop_2021['COMMUNE'] == 75056)]
pop_2021_paris["ANNEE"] = 2021
#pop_2021_paris["ARM"].unique()

pop_2020_paris = pop_2020[
    (pop_2020['COMMUNE'] == 75056)]
pop_2020_paris["ANNEE"] = 2020
pop_2020_paris = pop_2020_paris.drop(columns=["Texte"])
#pop_2020_paris["ARM"].unique()
#pop_2020_paris["INPER"].unique()

pop_2019_paris = pop_2019[
    (pop_2019['COMMUNE'] == 75056)]
pop_2019_paris["ANNEE"] = 2019
#pop_2019_paris["ARM"].unique()

## Focus sur le nombre total d'habitants, compris comme la somme des habitants d'un logement
pop_paris = pd.concat([pop_2021_paris, pop_2020_paris, pop_2019_paris], ignore_index=True)
pop_paris = pop_paris[pop_paris['INPER'] != 'Y']
pop_paris['INPER'] = pop_paris['INPER'].astype(int)


#=== Nombre de personnes de moins de 3, 5 ou 11 ans
pop_paris['INP3M'] = pop_paris['INP3M'].astype(int)
pop_paris['INP5M'] = pop_paris['INP5M'].astype(int)
pop_paris['INP11M'] = pop_paris['INP11M'].astype(int)
pop_paris['Maternelle'] = pop_paris['INP5M']-pop_paris['INP3M']
pop_paris['Elementaire'] = pop_paris['INP11M']-pop_paris['INP5M']
pop_paris['Primaire'] = pop_paris['INP11M']-pop_paris['INP3M']

pop_totale = pop_paris.groupby(['ANNEE'])['INPER'].sum().reset_index()
pop_totale["Evolution en niveau"] = pop_totale["INPER"].diff().fillna(0)
pop_totale["Evolution en %"] = pop_totale["INPER"].pct_change().fillna(0) * 100
pop_totale.rename(columns={'INPER':"Nombre d'habitants en logement ordinaire"}, inplace=True)


pop_totale_arrondissement = pop_paris.groupby(['ANNEE', 'ARM']).agg({'INPER': 'sum','INP3M': 'sum','INP5M': 'sum','INP11M': 'sum','Maternelle': 'sum','Elementaire': 'sum','Primaire': 'sum'}).reset_index()

pivot_pop_totale = pop_totale_arrondissement.pivot(index='ARM', columns='ANNEE', values='INPER')
pivot_pop_totale['evolution_total'] = ((pivot_pop_totale[2021] - pivot_pop_totale[2019]) / pivot_pop_totale[2019]) * 100
pivot_pop_totale['evolution_2019_2020'] = ((pivot_pop_totale[2020] - pivot_pop_totale[2019]) / pivot_pop_totale[2019]) * 100
pivot_pop_totale['evolution_2020_2021'] = ((pivot_pop_totale[2021] - pivot_pop_totale[2020]) / pivot_pop_totale[2020]) * 100
pivot_pop_totale['proportion_2019_2020'] = pivot_pop_totale['evolution_2019_2020'] / pivot_pop_totale['evolution_total']
pivot_pop_totale['proportion_2020_2021'] = pivot_pop_totale['evolution_2020_2021'] / pivot_pop_totale['evolution_total']
pivot_pop_totale['evolution_total_niveau'] = (pivot_pop_totale[2021] - pivot_pop_totale[2019]) 
pivot_pop_totale['INSEE_COG'] = pivot_pop_totale.index
pivot_pop_totale.index = pivot_pop_totale.index.astype(str)

pivot_pop_totale_sorted = pivot_pop_totale.sort_values(by='evolution_total', ascending=False)

#=== Tableau évolution 2019-2021 par arrondissement
part_evolution_par_an_et_arrondissement = pivot_pop_totale[['proportion_2019_2020', 'proportion_2020_2021']]

part_evolution_par_an_et_arrondissement.rename(
    columns={
        'proportion_2019_2020': "part de l'année 2020",
        'proportion_2020_2021': "part de l'année 2021"
    },
    inplace=True
)

part_evolution_par_an_et_arrondissement.reset_index(drop=False, inplace=True)
part_evolution_par_an_et_arrondissement.index.name = None
part_evolution_par_an_et_arrondissement.columns.name = None

# Proportion population par arrondissement 

pivot_pop_totale['population_totale_2019'] = pivot_pop_totale[2019].sum()
pivot_pop_totale['population_totale_2020'] = pivot_pop_totale[2020].sum()
pivot_pop_totale['population_totale_2021'] = pivot_pop_totale[2021].sum()
pivot_pop_totale['proportion_2019'] = pivot_pop_totale[2019] / pivot_pop_totale['population_totale_2019'] * 100
pivot_pop_totale['proportion_2020'] = pivot_pop_totale[2020] / pivot_pop_totale['population_totale_2020'] * 100
pivot_pop_totale['proportion_2021'] = pivot_pop_totale[2021] / pivot_pop_totale['population_totale_2021'] * 100

## Graphiques 

### Evolution classée par arrondissement
plt.figure(figsize=(10, 6))
plt.bar(pivot_pop_totale_sorted.index.str[-2:], pivot_pop_totale_sorted['evolution_total'], color='skyblue') #Je garde que les 2 numéros du code postale
plt.xlabel('Arrondissement', fontsize=12)
plt.ylabel('Évolution en % (2019-2021)', fontsize=12)
plt.title('Évolution en % de la Population (2019 à 2021)', fontsize=14)
plt.xticks(rotation=45) #à enlever éventuellement
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/evolution_population_par_arrondissement.png")

### Evolution avec contribution 2019-2020

x = np.arange(len(pivot_pop_totale_sorted))  # Position des barres
width = 0.6

plt.figure(figsize=(12, 6))
plt.bar(
    x,
    height=pivot_pop_totale_sorted['evolution_total'],  # Hauteur totale
    width=width,
    color='skyblue',
    label='Total'
)
plt.bar(
    x,
    height=pivot_pop_totale_sorted['evolution_total'] * pivot_pop_totale_sorted['proportion_2019_2020'],
    width=width,
    color='orange',
    label='Contribution de 2020'
)
plt.xlabel('Arrondissements', fontsize=12)
plt.ylabel('Evolution en %', fontsize=12)
plt.title("Évolution Totale de la Population entre 2019 et 2021", fontsize=14)
plt.xticks(x, pivot_pop_totale_sorted.index.str[-2:], rotation=45) #idem que 2 chiffres pour l'arrondissement #à enlever éventuellement la rotation
plt.legend()
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/evolution_population_avec_contrib.png")

## Graphique : proportion de la population par arrondissement

arrondissement = pivot_pop_totale.index.str[-2:]#Je coupe pour n'avoir que les 2 chiffres.
annees = pivot_pop_totale[[2019,2020,2021]].columns
proportion = [pivot_pop_totale[f"proportion_{annee}"] for annee in annees]
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
ax.set_title("Proportions de la population par arrondissement (2019-2021)")
ax.legend(title="Années")
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/proportion_population.png")


## Cartographie

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

pivot_pop_totale.columns

petite_couronne_count = petite_couronne.merge(pivot_pop_totale).to_crs(2154) 

set(petite_couronne.columns).intersection(set(pivot_pop_totale.columns))
petite_couronne_count.head(20)

## Evolution en niveau

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
aplat = petite_couronne_count.plot(
    column="evolution_total_niveau",
    cmap="RdBu",
    legend=True,
    ax=ax,
    legend_kwds={
        "orientation": "horizontal",  # Rend la légende horizontale
        "shrink": 0.5,  # Ajuste la taille de la barre de couleur
        "pad": 0.1,  # Espacement entre la légende et la carte
        "label": "Évolution en milliers"
    }
)
ax.set_axis_off()
ax.set_title(
    "Evolution de la population par arrondissement entre 2019 et 2021",
    y=1.05,  # Titre au-dessus de la carte
    fontsize=16
)

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/carte_evol_population_niveau.png")

## Evolution en %

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
aplat = petite_couronne_count.plot(
    column="evolution_total",
    cmap="RdBu",
    legend=True,
    ax=ax,
    legend_kwds={
        "orientation": "horizontal",  # Rend la légende horizontale
        "shrink": 0.5,  # Ajuste la taille de la barre de couleur
        "pad": 0.1,  # Espacement entre la légende et la carte
        "label": "Évolution en %"
    }
)
ax.set_axis_off()
ax.set_title(
    "Evolution de la population par arrondissement entre 2019 et 2021",
    y=1.05,  # Titre au-dessus de la carte
    fontsize=16
)

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/graphs/carte_evol_population_pourcentage.png")
