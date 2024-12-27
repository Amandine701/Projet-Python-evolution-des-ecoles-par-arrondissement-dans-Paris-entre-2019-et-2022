# Projet-Python-evolution-des-ecoles-par-arrondissement-dans-Paris-entre-2019-et-2021
## Question : Est-ce que l'évolution de la démographie des écoles est en accord avec évolution de la population (par classe d'âge).

Cloner le projet dans un environnement VS Code et faire tourner le rapport. 

Données :
effectifs par classe et par établissement https://data.education.gouv.fr/explore/dataset/fr-en-ecoles-effectifs-nb_classes/table/?disjunctive.rentree_scolaire&disjunctive.region_academique&disjunctive.academie&disjunctive.departement&disjunctive.commune&disjunctive.numero_ecole&disjunctive.denomination_principale&disjunctive.patronyme&disjunctive.secteur&disjunctive.code_postal&sort=tri

Recensement (données INSEE) : https://www.insee.fr/fr/information/2008354
https://www.insee.fr/fr/statistiques/8202264
https://www.insee.fr/fr/statistiques/8272002 #documentation

Variables d'intérêt :

- Nombre d'élèves dans chaque arrondissement
- Population par arrondissement et par tranches d'âges
- Proportion de la population de chaque arrondissement 

Visualisation : 

Evolution des variables d'intérêts : cartes par arrondissement et graphiques en histogrammes
Pyramides des âges par arrondissement 

Modélisation : 

Régression des effectifs par année et arrondissement sur une constante, certaines tranches d'âges (en âge d'avoir des enfants), d'autres variables explicatives et des effets fixes par arrondissement. 
Age moyen du premier enfants : 33 ans à Paris 
y = a + b1x1 + b2x2 + b3x3 + H + e
x1 : proportion de gens entre 30 et 40 ans dans l'arrondissement 
x2 : proportion de cadres dans l'arrondissement 
x3 : proportion de T3 ou + dans l'arrondissement 

Ouverture : 

Etendre à la Grande Couronne pour voir si la baisse d'élèves dans Paris se traduit par une augmentation en banlieue (= mobilité). 
Explication par exemple : hausse des meublés touristiques à Paris (mais manque de données dans les bases qu'on a)

