# Projet Python : Evolution des effectifs scolaires et de la population parisienne entre 2019 et 2021
## Question : Est-ce que l'évolution de la démographie des écoles est en accord avec évolution de la population (par classe d'âge).

Cloner le projet dans un environnement VS Code et faire tourner le rapport. 

### Données :

Effectifs par classe et par établissement : https://data.education.gouv.fr/explore/dataset/fr-en-ecoles-effectifs-nb_classes/table/?disjunctive.rentree_scolaire&disjunctive.region_academique&disjunctive.academie&disjunctive.departement&disjunctive.commune&disjunctive.numero_ecole&disjunctive.denomination_principale&disjunctive.patronyme&disjunctive.secteur&disjunctive.code_postal&sort=tri

Recensement (données INSEE) : 
- https://www.insee.fr/fr/information/2008354
- https://www.insee.fr/fr/statistiques/8202264
- https://www.insee.fr/fr/statistiques/8272002 pour la documentation

### Variables d'intérêt :

- Nombre total d'élèves dans chaque arrondissement
- Population par arrondissement et par tranches d'âges
- Proportion de la population de chaque arrondissement

Variables secondaires : proportion de cadres et de T3+ dans chaque arrondissement 

### Visualisation : 

Evolution des variables d'intérêts : cartes par arrondissement et graphiques en histogrammes
Pyramides des âges par arrondissement

### Modélisation : 

Régression des effectifs par année et arrondissement sur une constante, certaines tranches d'âges (en âge d'avoir des enfants), d'autres variables explicatives et des effets fixes par arrondissement : 

y = a + b1x1 + b2x2 + b3x3 + H + e

Avec : 
- x1 : proportion de gens entre 30 et 40 ans dans l'arrondissement 
- x2 : proportion de cadres dans l'arrondissement 
- x3 : proportion de T3 ou + dans l'arrondissement
- H : effets fixes de contrôle

### Ouverture : 

On pourrait étendre l'analyse à la Grande Couronne pour voir si la baisse d'élèves dans Paris se traduit par une augmentation en banlieue, ce qui traduirait une mobilité de la population en proche banlieue. Une explication possible si ce phénomène se confirmait pourrait venir de la hausse du nombre de meublés touristiques à Paris, qui sature un peu plus le marché immobilier parisien. Mais nous manquions de données dans les bases disponibles pour mener cette analyse plus en profondeur. 

