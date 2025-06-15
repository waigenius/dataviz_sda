# dataviz_sda

## Présentation du projet
Projet analyse de données

Lien du dataset :  https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data
Lancement de l'app : python -m streamlit run app.py

Part 1 : Nettoyage et Analyse Exploratoire d’un Dataset de Véhicules

Objectif
Ce projet vise à nettoyer, analyser et préparer un jeu de données de véhicules d'occasion afin de permettre des analyses fiables sur les prix, les caractéristiques techniques, et les tendances du marché automobile.

Équipe
Projet réalisé par Waï LEKONE et Damien KOHLER

---

Étapes du projet

1. Chargement et exploration initiale (`vehicles.csv`)
- Lecture du fichier CSV
- Exploration des dimensions, types de colonnes et valeurs
- Premières statistiques descriptives (numeriques & catégorielles)

2. Nettoyage du dataset

Corrections de types
- Conversion de `posting_date` en `datetime`
- Nettoyage de la colonne `cylinders` (suppression de texte inutile, détection des `NaN`)

Gestion des valeurs manquantes
- Imputation conditionnelle de `condition` en fonction de `title_status`
- Méthode d’imputation avancée par modèle pour `manufacturer`, `drive`, `fuel`, etc.
  - Méthode : remplissage par mode local ou tirage aléatoire basé sur la distribution observée
- Vérification des proportions conservées avant/après

Suppression de données inutiles ou bruitées
- Colonnes supprimées : `id`, `url`, `region`, etc.
- Lignes supprimées :
  - Véhicules non roulants (`salvage`, `parts only`)
  - Lignes avec `NaN` critiques (`price`, `year`, `model`, etc.)

Détection des doublons
- Dédoublonnage avec `VIN` + `posting_date`
- Deuxième passe sans `VIN` via combinaison `price`, `year`, `model`, etc.

Gestion des valeurs aberrantes
- Odometer : gardé entre `100` et `300 000` miles
- Year : borné entre `1950` et `2021`
- Price : borné entre `500` et `150 000`

---
Axes d’analyse proposés
1. Distribution du prix
2. Décote selon l’âge (nouvelle variable : `vehicle_age`)
3. Analyse géographique par État
4. Prix en fonction du kilométrage et de l’état
5. Analyse par marque et modèle
---
Export
Le DataFrame nettoyé est enregistré sous le nom :  
df.to_csv("vehicles_clean.csv", index=False)


Part 2 : Application Streamlit - Craigslist Cars & Trucks

Objectif
Déployer une application interactive permettant de visualiser et d’explorer un large dataset (> 400 000 lignes) d’annonces de véhicules d’occasion issues de Craigslist (USA), préalablement nettoyé.

---

Technologies utilisées
- Streamlit : framework Python pour créer des interfaces interactives
- Plotly Express : visualisation interactive (graphiques dynamiques)
- Pandas / NumPy : traitement et nettoyage des données
- Pillow : gestion des images (bannière)

---

Fichiers nécessaires
- `vehicles_clean.csv` : dataset nettoyé (export de la 1ère partie)
- `Images/banner-car.jpg` : bannière d’en-tête
- `app.py` : fichier principal de l'application (code ci-dessus)

---

Structure de l’application

Sidebar (menu latéral)
- Contexte du projet (Sorbonne Data Analytics - Session 6)
- Objectifs pédagogiques
- Description du dataset et des traitements effectués
- Membres du groupe

---

Onglets interactifs

1. Exploration du dataset
- Aperçu des premières lignes
- Structure du DataFrame (`info()`)
- Statistiques descriptives

2. Distribution des prix
- Histogramme dynamique des prix
- Filtre interactif sur la plage de prix

3. Décote selon l'âge
- Nuage de points `vehicle_age` vs `price`
- Régression linéaire pour illustrer la décote

4. Répartition géographique
- Carte des USA avec le nombre d’annonces par État (choroplèthe)

5. Prix vs Kilométrage
- Nuage de points `odometer` vs `price`, coloré par `condition`
- Permet d’analyser l’usure en lien avec le prix

6. Analyse par modèle
- Filtres multi-critères : carburant, transmission, condition, etc.
- Top N modèles par prix moyen
- Graphique en barres

7. Nuage de mots
- Affichage de l'image nuage de mots générée par le text mining

---

KPIs affichés
- Nombre total d’annonces
- Prix moyen
- Nombre de modèles uniques

Part 3 - Analyse de texte - Text Mining sur un article PDF

Objectif  
Cette partie vise à appliquer des techniques de text mining en français sur un article au format PDF afin d'extraire, nettoyer et analyser le contenu textuel. L'objectif final est de générer un nuage de mots basé sur les termes les plus significatifs.

Technologies utilisées  
- pdfminer.six : extraction de texte depuis un PDF  
- spaCy (modèle `fr_core_news_sm`) : traitement du langage naturel  
- wordcloud : visualisation du vocabulaire le plus fréquent  
- collections.Counter : calcul des fréquences  
- re, os : gestion système et expressions régulières

Étapes du processus

1. Extraction du texte depuis un fichier PDF  
La fonction `extract_text_from_pdf(pdf_path)` utilise `pdfminer` pour lire le texte brut du fichier PDF spécifié.  
Elle vérifie si le fichier existe, puis extrait et retourne le contenu textuel.  

2. Prétraitement linguistique  
Un pipeline spaCy en français est utilisé pour nettoyer le texte extrait :  
- Conversion en minuscules  
- Suppression de la ponctuation, des chiffres, des mots vides (stopwords)  
- Conservation uniquement des mots alphabétiques (lettres)  
- Lemmatisation : réduction des mots à leur forme racine  
- Élimination des tokens trop courts (≤ 1 lettre)

3. Comptage des occurrences  
Le module `Counter` permet de compter les fréquences des lemmes obtenus.  
Un aperçu des 50 premiers tokens est affiché, ainsi que le top 20 des mots les plus fréquents.  

4. Nuage de mots 
Les mots nettoyés et comptés sont utilisés pour créer un nuage de mots (`WordCloud`).  
L'image est sauvegardé dans le dossier "image" pour affichage sur l'application.

Remarques importantes  
- Le modèle spaCy `fr_core_news_sm` doit être installé manuellement avant exécution :  
  `python -m spacy download fr_core_news_sm`  
- Le PDF à analyser doit être nommé `article_VO.pdf` et présent dans le répertoire du script