# Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2021
Question : Est-ce que l'évolution de la démographie des écoles est en accord avec évolution de la population (par classe d'âge).

Données :
effectifs par classe et par établissement https://data.education.gouv.fr/explore/dataset/fr-en-ecoles-effectifs-nb_classes/table/?disjunctive.rentree_scolaire&disjunctive.region_academique&disjunctive.academie&disjunctive.departement&disjunctive.commune&disjunctive.numero_ecole&disjunctive.denomination_principale&disjunctive.patronyme&disjunctive.secteur&disjunctive.code_postal&sort=tri
Recensement (données INSEE) : https://www.insee.fr/fr/information/2008354
https://www.insee.fr/fr/statistiques/8202264
https://www.insee.fr/fr/statistiques/8272002#documentation

Variables d'intérêt :
- P1 = proportion d'écoles dans chaque arrondissement (nombre écoles arrondissements / total école paris)
- P2 = proportion population de chaque arrondissement 
- P3 = proportion élèves par écoles arrondissement 

visualisation : évolution P1/P2
pyramides ages par arrondissement 

Modélisation : régression des effectifs par année et arrondissement sur une constante, certaines tranches d'âges (en âge d'avoir des enfants), et des effets fixes par arrondissement. 
Pour ce faire : merger les bases créées (pivot_df et population_pivot - ou des noms équivalents), crééer les 20 dummys (généralement il existe des fonctions déjà créées qui le font déjà) pour les arrondissements 
Age moyen du premier enfants : 33 ans à Paris 
y = a + b1x1 + b2x2 + b3x3 + H + e
x1 : proportion de gens entre 30 et 40 ans dans l'arrondissement 
x2 : proportion de cadres dans l'arrondissement 
x3 : proportion de T3 ou + dans l'arrondissement 

2e modélisation : regression en différence 

Limite : on aurait pu intégrer le nombre de naissance 3 ans avant 
Ouverture : étendre à la Grande Couronne pour voir si la baisse d'élèves dans Paris se traduit par une augmentation en banlieue (= mobilité). 
Explication par exemple : hausse des meublés touristiques à Paris (mais manque de données dans les bases qu'on a)

