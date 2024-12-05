# Recensement

## Sélectionne uniquement Paris
pop_2021_paris = pop_2021[
    (pop_2021['COMMUNE'] == 75056)]
pop_2021_paris["ANNEE"] = 2021
pop_2021_paris["ARM"].unique()

pop_2020_paris = pop_2020[
    (pop_2020['COMMUNE'] == 75056)]
pop_2020_paris["ANNEE"] = 2020
pop_2020_paris = pop_2020_paris.drop(columns=["Texte"])
pop_2020_paris["ARM"].unique()
pop_2020_paris["INPER"].unique()

pop_2019_paris = pop_2019[
    (pop_2019['COMMUNE'] == 75056)]
pop_2019_paris["ANNEE"] = 2019
pop_2019_paris["ARM"].unique()

## Focus sur le nombre total d'habitants, compris comme la somme des habitants d'un logement
pop_paris = pd.concat([pop_2021_paris, pop_2020_paris, pop_2019_paris], ignore_index=True)
print(pop_paris.head(20))
pop_paris = pop_paris[pop_paris['INPER'] != 'Y']
pop_paris['INPER'] = pop_paris['INPER'].astype(int)

pop_totale_arrondissement = pop_paris.groupby(['ANNEE', 'ARM'])['INPER'].sum().reset_index()

pivot_pop_totale = pop_totale_arrondissement.pivot(index='ARM', columns='ANNEE', values='INPER')
pivot_pop_totale['evolution_total'] = ((pivot_pop_totale[2021] - pivot_pop_totale[2019]) / pivot_pop_totale[2019]) * 100
pivot_pop_totale['evolution_2019_2020'] = ((pivot_pop_totale[2020] - pivot_pop_totale[2019]) / pivot_pop_totale[2019]) * 100
pivot_pop_totale['evolution_2020_2021'] = ((pivot_pop_totale[2021] - pivot_pop_totale[2020]) / pivot_pop_totale[2020]) * 100
pivot_pop_totale['proportion_2019_2020'] = pivot_pop_totale['evolution_2019_2020'] / pivot_pop_totale['evolution_total']
pivot_pop_totale['proportion_2020_2021'] = pivot_pop_totale['evolution_2020_2021'] / pivot_pop_totale['evolution_total']
pivot_pop_totale['evolution_total_niveau'] = (pivot_pop_totale[2021] - pivot_df[2019]) 
pivot_pop_totale['INSEE_COG'] = (pivot_pop_totale.index.astype(int)+ 100).astype(str)
pivot_pop_totale.index = pivot_pop_totale.index.astype(str)

pivot_pop_totale_sorted = pivot_pop_totale.sort_values(by='evolution_total', ascending=False)

## Graphiques 

### Evolution classée par arrondissement
plt.figure(figsize=(10, 6))
plt.bar(pivot_pop_totale_sorted.index.str[-2:], pivot_pop_totale_sorted['evolution_total'], color='skyblue') #Je garde que les 2 numéros du code postale
plt.xlabel('Arrondissement', fontsize=12)
plt.ylabel('Évolution en % (2019-2021)', fontsize=12)
plt.title('Évolution en % de la Population (2019 à 2021)', fontsize=14)
plt.xticks(rotation=45) #à enlever éventuellement
plt.tight_layout()

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/evolution_population_par_arrondissement.png")

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

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/evolution_population_avec_contrib.png")

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



petite_couronne_count = petite_couronne.merge(pivot_pop_totale).to_crs(2154)

#Evol en niveau

aplat = petite_couronne_count.plot(column="evolution_total_niveau", cmap="Reds_r", legend=True)
aplat.set_axis_off()
aplat.set_title("Evolution de la Population entre 2019 et 2021",y=1.0, pad=14)
aplat

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/carte_pop.png")


#evol en %

aplat = petite_couronne_count.plot(column="evolution_total", cmap="Reds_r", legend=True)
aplat.set_axis_off()
aplat.set_title("Evolution du nombre d'élèves entre 2019 et 2021, par arrondissement (en %)",y=1.0, pad=-14)
aplat

plt.savefig("/home/onyxia/work/Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2022/carte_pop2.png")