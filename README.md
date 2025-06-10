# dataviz_sda

## Présentation du projet
Projet analyse de données

Lien du dataset :  https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data


Étapes de réflexion et préparation des données
1. Suppression des colonnes non utiles
Certaines colonnes du dataset ne sont pas pertinentes pour notre analyse, car elles ne contiennent pas d’informations exploitables d’un point de vue statistique ou visuel :
url, region_url, image_url : adresses web non exploitables en visualisation ou en analyse.
description: informations spécifiques à chaque annonce, non utiles pour des analyses globales. (potentiellement utile pour dédoublonnage ?)
Décision : Suppression de ces colonnes pour alléger le dataset et se concentrer sur les variables analytiques.

2. Formatage de la date de publication
La colonne posting_date est initialement au format texte.
Transformation : Conversion au format datetime (jour/mois/année) avec pd.to_datetime().
Création possible d’une colonne dérivée year_posted pour analyser les tendances temporelles.
Justification : Permet d’effectuer des regroupements temporels (par mois, trimestre…) et de filtrer les publications récentes.

3. Suppression des lignes incomplètes
Certaines lignes présentent des valeurs manquantes dans des colonnes essentielles à l’analyse :
price, year, manufacturer, model, odometer, condition…
Décision : Définir les variables critiques et suppression des lignes ayant des valeurs manquantes sur ces variables.
Justification : Ces informations sont nécessaires pour toute analyse descriptive ou modélisation. Les conserver créerait du bruit dans l’analyse.

4. Traitement des valeurs incohérentes
Certaines annonces ont : Un price = 0 (don gratuit ou erreur)
Un price très élevé (> 250 000 $)
Un year irréaliste (avant 1950 ou après l’année actuelle)
Un odometer très faible (ex : 1) ou excessif (> 500 000)
Décision : Supprimer les annonces à price <= 1000 ou price > 250000
Supprimer les années incohérentes
Supprimer les valeurs aberrantes sur odometer via un filtre ou IQR
Justification : Ces valeurs faussent les statistiques globales et les visualisations. Une borne réaliste permet une analyse plus fiable.

5. Suppression des doublons
Pour identifier les doublons, nous utilisons les colonnes clés suivantes : price, year, manufacturer, model, condition, cylinders, et éventuellement posting_date.
Décision : Détection des doublons sur cette combinaison, puis suppression des doublons exacts.
Justification : De nombreuses annonces sont postées plusieurs fois ou apparaissent dans des régions voisines. Les doublons gonflent artificiellement les volumes et biaisent les statistiques.

6. Autres traitements possibles
Homogénéisation des libellés : nettoyage des valeurs catégorielles (ex : standardiser good, Good, GOOD)
Suppression des valeurs rares dans certains champs (ex : catégories type avec < 1% des annonces)
Remplissage conditionnel : certaines valeurs manquantes peuvent être imputées si d’autres champs sont suffisamment renseignés