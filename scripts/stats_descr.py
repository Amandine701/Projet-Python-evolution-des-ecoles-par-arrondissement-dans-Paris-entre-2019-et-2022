# Base de données effectifs_ecoles
# Ne garde que les rentrées scolaires 2019, 2020, 2021 et la région Ile de France, restreindre plus tard aux communes

effectifs_ecoles_192021 = effectifs_ecoles[(effectifs_ecoles['Rentrée scolaire'].isin([2019, 2020, 2021])) & (effectifs_ecoles["Région académique"] == "ILE-DE-FRANCE")]

effectifs_ecoles_192021["Rentrée scolaire"].unique()
effectifs_ecoles_192021.columns
effectifs_ecoles_192021["Commune"].unique()

## Renommer les colonnes

from unidecode import unidecode

colonnes = effectifs_ecoles_192021.columns

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
effectifs_ecoles_192021.columns = [nettoyer_nom_colonne(col) for col in colonnes]


