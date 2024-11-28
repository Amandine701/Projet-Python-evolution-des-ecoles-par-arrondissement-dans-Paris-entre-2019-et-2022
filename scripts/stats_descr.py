import matplotlib.pyplot as plt
import numpy as np
from unidecode import unidecode

# Base de données effectifs_ecoles ---------
## Ne garde que les rentrées scolaires 2019, 2020, 2021 et Paris (via le code postal)

effectifs_ecoles_paris = effectifs_ecoles[
    (effectifs_ecoles['Rentrée scolaire'].isin([2019, 2020, 2021])) &
    (effectifs_ecoles["Région académique"] == "ILE-DE-FRANCE") &
    (effectifs_ecoles_192021['Code Postal'].isin([75001,75002,75003,75004, 75005, 75006, 75007, 75008, 75009, 75010, 75011, 75012, 75013, 75014, 75015, 75016, 75017, 75018, 75019, 75020]))]


## Renommer les colonnes

colonnes = effectifs_ecoles_paris.columns

# Fonction pour renommer les colonnes
def nettoyer_nom_colonne(nom):
    # Supprimer les accents
    nom_sans_accents = unidecode(nom)
    # Supprimer "d'" et les apostrophes
    nom_sans_apostrophe = nom_sans_accents.replace("d'", "").replace("'", "")
    # Remplacer les espaces par des tirets bas
    nom_sans_espaces = nom_sans_apostrophe.replace(" ", "_")
    # Transformer en minuscule pour uniformité (facultatif)
    return nom_sans_espaces.lower()

# Renommer toutes les colonnes
effectifs_ecoles_paris.columns = [nettoyer_nom_colonne(col) for col in colonnes]

# Total nombre d'élèves par arrondissement par année
nb_eleve_arrondissement_annee = effectifs_ecoles_paris.groupby(['code_postal', 'rentree_scolaire'])['nombre_total_eleves'].sum().reset_index()

## Pivot pour réorganiser les données
pivot_df = nb_eleve_arrondissement_annee.pivot(index='code_postal', columns='rentree_scolaire', values='nombre_total_eleves')
pivot_df['evolution_total'] = ((pivot_df[2021] - pivot_df[2019]) / pivot_df[2019]) * 100
pivot_df['evolution_2019_2020'] = ((pivot_df[2020] - pivot_df[2019]) / pivot_df[2019]) * 100
pivot_df['evolution_2020_2021'] = ((pivot_df[2021] - pivot_df[2020]) / pivot_df[2020]) * 100
pivot_df['proportion_2019_2020'] = pivot_df['evolution_2019_2020'] / pivot_df['evolution_total']
pivot_df['proportion_2020_2021'] = pivot_df['evolution_2020_2021'] / pivot_df['evolution_total']

pivot_df_sorted = pivot_df.sort_values(by='evolution_total', ascending=False)


# Graphique : Nombre total d'élèves pas arrondissement par année

arrondissement = pivot_df.index
annees = pivot_df[[2019,2020,2021]].columns
bar_width = 0.25  # Largeur des barres
x = np.arange(len(arrondissement))  # Positions des régions sur l'axe X

plt.figure(figsize=(10, 6))

for i, annee in enumerate(annees):
    plt.bar(x + i * bar_width, pivot_df[annee], width=bar_width, label=f"Année {annee}")

plt.title("Nombre d'élèves par arrondissement et par année")
plt.xlabel("Arrondissement")
plt.ylabel("Nombre d'élèves")
plt.xticks(x + bar_width, arrondissement, rotation=45)  # Centrer les labels des régions
plt.legend(title="Année")
plt.tight_layout()

plt.savefig("nb_élève_par_annee.png")

# Graphique : Evolution du nombre d'élèves par arrondissement classée

plt.figure(figsize=(10, 6))
plt.bar(pivot_df_sorted.index.astype(str), pivot_df_sorted['evolution_total'], color='skyblue')
plt.xlabel('Arrondissement (Code Postal)', fontsize=12)
plt.ylabel('Évolution en % (2019-2021)', fontsize=12)
plt.title('Évolution en % du Nombre d’Élèves (2019 à 2021)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("evolution_nb_eleve_par_arrondissement.png")

# Graphique : Evolution du nombre d'élèves par arrondissement avec contribution 2020, classée

x = np.arange(len(pivot_df_sorted))  # Position des barres
width = 0.6

plt.figure(figsize=(12, 6))
plt.bar(
    x,
    height=pivot_df_sorted['evolution_total'],  # Hauteur totale
    width=width,
    color='skyblue',
    label='Évolution totale'
)
plt.bar(
    x,
    height=pivot_df_sorted['evolution_total'] * pivot_df_sorted['proportion_2019_2020'],
    width=width,
    color='orange',
    label='Contribution 2019-2020'
)
plt.xlabel('Arrondissements (Code Postal)', fontsize=12)
plt.ylabel('Évolution totale (%)', fontsize=12)
plt.title("Évolution Totale du Nombre d'Eleves(2019 à 2021)", fontsize=14)
plt.xticks(x, pivot_df_sorted.index.astype(str), rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("evolution_avec_contrib_2020.png")



