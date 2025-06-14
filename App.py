import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Projet Craigslist Cars & Trucks",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Barre latérale
st.sidebar.title("Formation Sorbonne Data Analytics")
st.sidebar.subheader("Session 6 2025/2026")
st.sidebar.markdown(
    "**Membres du groupe :**\n- Waï Lekone\n- Damien Kohler"
)

# Liens utiles
st.sidebar.markdown(
    "**Télécharger le dataset :** [CSV nettoyé](./vehicles_clean.csv)"
)
st.sidebar.markdown(
    "**Environnement GitHub :** [Repo Projet](https://github.com/ton-user/ton-repo)"
)

# Titre principal
st.title("Analyse des annonces de véhicules d'occasion - Craigslist Cars & Trucks")
st.markdown(
    "Ce projet présente une analyse interactive d'un dataset de plus de 200 000 annonces Craigslist."
)

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_clean.csv', low_memory=False)
    # Conversion de posting_date en datetime et extraction de l'année de publication
    df['posting_date'] = pd.to_datetime(
        df['posting_date'], errors='coerce', utc=True
    ).dt.tz_convert(None)
    df['posting_year'] = df['posting_date'].dt.year
    # Normalisation de l'état
    df['state'] = df['state'].str.upper()
    return df

df = load_data()

# 1. Présentation du dataset
st.header("1. Présentation du dataset")
st.markdown(f"- **Observations :** {df.shape[0]} lignes")
st.markdown(f"- **Variables :** {df.shape[1]} colonnes")
st.markdown("- **Types :** numérique, catégoriel, temporel, géographique…")
st.markdown("- **Valeurs manquantes par colonne :")
st.write(df.isna().sum())

# 2. Exploration interactive
st.header("2. Exploration interactive")
min_price, max_price = st.slider(
    "Prix ($)",
    int(df['price'].min()), int(df['price'].max()),
    (1000, 50000)
)
selected_fuel = st.multiselect(
    "Type de carburant",
    options=df['fuel'].dropna().unique(),
    default=list(df['fuel'].dropna().unique())
)
filtered = df[
    (df['price'] >= min_price) &
    (df['price'] <= max_price) &
    (df['fuel'].isin(selected_fuel))
]
fig1 = px.histogram(
    filtered,
    x='price', nbins=50, color='fuel', barmode='overlay',
    labels={'price': 'Prix ($)'},
    title='Distribution des prix par type de carburant'
)
st.plotly_chart(fig1, use_container_width=True)

# 3. Décote selon l'âge du véhicule
st.header("3. Décote selon l'âge du véhicule")
# Calcul de l'âge basé sur l'année de publication et l'année du modèle
filtered = filtered.copy()
filtered['vehicle_age'] = filtered['posting_year'] - filtered['year']
fig2 = px.scatter(
    filtered,
    x='vehicle_age', y='price', color='transmission',
    hover_data=['model', 'year', 'posting_year'],
    title="Prix en fonction de l'âge du véhicule"
)
st.plotly_chart(fig2, use_container_width=True)

# 4. Analyse géographique par État
st.header("4. Analyse géographique par État")
state_price = df.groupby('state')['price'].mean().reset_index()
fig3 = px.choropleth(
    state_price,
    locations='state',
    locationmode='USA-states',
    color='price',
    scope='usa',
    labels={'price': 'Prix moyen ($)'},
    title='Prix moyen des annonces par État'
)
st.plotly_chart(fig3, use_container_width=True)

# 5. Configurations techniques vs prix
st.header("5. Configurations techniques vs prix")
fig4 = px.box(
    filtered,
    x='drive', y='price',
    labels={'drive': 'Transmission', 'price': 'Prix ($)'},
    title='Prix en fonction du type de transmission'
)
st.plotly_chart(fig4, use_container_width=True)

# 6. Évolution mensuelle du volume d'annonces en 2021
st.header("6. Évolution mensuelle du volume d'annonces")
# Le dataset ne contient que l'année 2021 : on filtre directement

df_2021 = df[df['posting_year'] == 2021].copy()
# Extraire le mois

df_2021['month'] = df_2021['posting_date'].dt.month
monthly = (
    df_2021.groupby('month')
    .size()
    .reset_index(name='count')
)
# Créer une date fictive pour l'axe X (1er jour du mois)

monthly['month_label'] = pd.to_datetime(
    dict(year=2021, month=monthly['month'], day=1)
)
fig5 = px.line(
    monthly,
    x='month_label',
    y='count',
    labels={'month_label': 'Mois', 'count': "Nombre d'annonces"},
    title="Nombre d'annonces par mois en 2021"
)
st.plotly_chart(fig5, use_container_width=True)

# Pied de page
st.markdown("---")
st.markdown("© 2025 Sorbonne Data Analytics - Projet par Waï Lekone & Damien Kohler")
st.markdown("---")
st.markdown("© 2025 Sorbonne Data Analytics - Projet par Waï Lekone & Damien Kohler")
