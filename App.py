import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
from datetime import datetime
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Projet Craigslist Cars & Trucks",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Création de la bannière
img = Image.open("Images/banner-car.jpg").resize((1200, 150))
st.image(img, use_container_width=True)



# Barre latérale
st.sidebar.title("Formation Sorbonne Data Analytics")
st.sidebar.subheader("Session 6 2025/2026")
st.sidebar.markdown(
    """
**Projet Streamlit - SDA 2025/2026**  
Module : *Data Management & Visualisation*  
Objectif : Construire une app interactive autour d’un dataset volumineux (> 200 000 lignes)

**Réalisé par :**  
- Waï Lekone  
- Damien Kohler

**Données utilisées :**  
Craigslist Cars & Trucks (Kaggle)  
- ~400 000 annonces  
- Véhicules d’occasion - USA

**Traitement effectué :**  
- Nettoyage des colonnes non pertinentes  
- Suppression des doublons  
- Filtrage des prix, années, kilométrages incohérents  
- Imputation des valeurs manquantes selon le modèle
- Création de : `vehicle_age`, `posting_year`

**Axes analysés :**  
- Distribution des prix  
- Décote selon l’âge  
- Répartition géographique par État  
- Relation prix vs kilométrage  
- Top modèles
"""
)

# Titre principal et introduction
st.title("Analyse des annonces de véhicules d'occasion - Craigslist Cars & Trucks")
st.markdown(
    "Cette application permet de nettoyer, explorer et visualiser un jeu de données de plus de 400 000 annonces Craigslist."
)

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_clean.csv', low_memory=False)
    df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce', utc=True).dt.tz_convert(None)
    df['posting_year'] = df['posting_date'].dt.year
    df['vehicle_age'] = df['posting_year'] - df['year']
    df['state'] = df['state'].str.upper()
    return df

df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Nombre d’annonces", f"{len(df):,}")
col2.metric("Prix moyen", f"${df['price'].mean():,.0f}")
col3.metric("Modèles uniques", df['model'].nunique())

st.markdown("---")

# Création des onglets
all_tabs = [
    "Exploration dataset",
    "Distribution des prix",
    "Décote selon l'âge",
    "Répartition géographique",
    "Prix vs kilométrage",
    "Analyse par modèle"
]
tabs = st.tabs(all_tabs)

# 0. Exploration initiale du dataset
tab0 = tabs[0]
with tab0:
    st.header("Exploration du dataset")
    st.subheader("Aperçu des données brutes")
    st.dataframe(df.head(100))
    st.subheader("Informations générales")
    buf = io.StringIO()
    df.info(buf=buf)
    info_str = buf.getvalue()
    st.text(info_str)
    st.subheader("Statistiques descriptives")
    st.write(df.describe(include='all'))

# 1. Distribution des prix
tab1 = tabs[1]
with tab1:
    st.header("1. Distribution des prix")
    min_p, max_p = st.slider(
        "Plage de prix ($)", int(df['price'].min()), int(df['price'].max()), (1000, 50000)
    )
    df_price = df[(df['price'] >= min_p) & (df['price'] <= max_p)]
    fig_price = px.histogram(
        df_price, x='price', nbins=40,
        title="Histogramme des prix filtré",
        labels={'price': 'Prix ($)'}
    )
    st.plotly_chart(fig_price, use_container_width=True)

# 2. Décote selon l'âge du véhicule
tab2 = tabs[2]
with tab2:
    st.header("2. Décote selon l'âge du véhicule")
    sample = df[df['vehicle_age'] >= 0].sample(n=min(len(df),20000), random_state=42)
    fig_decote = px.scatter(
        sample, x='vehicle_age', y='price', opacity=0.5, trendline='ols',
        title="Prix en fonction de l'âge du véhicule",
        labels={'vehicle_age': "Âge (ans)", 'price': 'Prix ($)'}
    )
    st.plotly_chart(fig_decote, use_container_width=True)

# 3. Répartition géographique par État
tab3 = tabs[3]
with tab3:
    st.header("3. Répartition géographique par État")
    state_counts = df['state'].value_counts().reset_index()
    state_counts.columns = ['state','count']
    fig_geo = px.choropleth(
        state_counts, locations='state', locationmode='USA-states',
        color='count', color_continuous_scale='Blues', scope='usa',
        title="Nombre d'annonces par État",
        labels={'count':'Nombre d\'annonces'}
    )
    st.plotly_chart(fig_geo, use_container_width=True)

# 4. Relation prix vs kilométrage
tab4 = tabs[4]
with tab4:
    st.header("4. Relation prix vs kilométrage")
    sample2 = df.sample(n=min(len(df),10000), random_state=42)
    fig_km = px.scatter(
        sample2,
        x='odometer', y='price',
        color='condition',
        opacity=0.6,
        title="Prix vs Kilométrage par condition",
        labels={'odometer':'Kilométrage (miles)', 'price':'Prix ($)', 'condition':'État du véhicule'}
    )
    st.plotly_chart(fig_km, use_container_width=True)


# 5. Analyse par modèle avec filtres
tab5 = tabs[5]
with tab5:
    st.header("5. Analyse par modèle")
    with st.expander("Filtres", expanded=False):
        # Filtres alignés en 2 colonnes
        col1, col2 = st.columns(2)
        with col1:
            fuels = sorted(df['fuel'].dropna().unique())
            sel_fuel = st.multiselect('Carburants', fuels, default=[])
            cyls = sorted(df['cylinders'].dropna().unique())
            sel_cyl = st.multiselect('Cylindres', cyls, default=[])
            cond = sorted(df['condition'].dropna().unique())
            sel_cond = st.multiselect('Condition', cond, default=[])

        with col2:
            trans = sorted(df['transmission'].dropna().unique())
            sel_trans = st.multiselect('Transmission', trans, default=[])
            drives = sorted(df['drive'].dropna().unique())
            sel_drive = st.multiselect('Roues motrices', drives, default=[])
            size = sorted(df['size'].dropna().unique())
            sel_size = st.multiselect('Taille', size, default=[])

        top_n = st.slider('Top N modèles', 5, 20, 10)

    # Application des filtres
    df_mod = df
    if sel_fuel: df_mod = df_mod[df_mod['fuel'].isin(sel_fuel)]
    if sel_cyl: df_mod = df_mod[df_mod['cylinders'].isin(sel_cyl)]
    if sel_trans: df_mod = df_mod[df_mod['transmission'].isin(sel_trans)]
    if sel_drive: df_mod = df_mod[df_mod['drive'].isin(sel_drive)]

    top_models = (
        df_mod.groupby('model')['price']
        .mean().reset_index().nlargest(top_n, 'price')
    )
    fig_mod = px.bar(
        top_models, x='model', y='price',
        title=f"Top {top_n} modèles par prix moyen",
        labels={'model':'Modèle','price':'Prix moyen ($)'}
    )
    st.plotly_chart(fig_mod, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; margin-bottom:5px; color:grey;'>"
    "<strong>Waï Lekone & Damien Kohler</strong>"
    "</div>", unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align:center; color:grey;'>\
    © 2025 Sorbonne Data Analytics — \
    <a href='https://github.com/waigenius/dataviz_sda/blob/main/data_analysing.ipynb'>GitHub</a>\
    </div>", unsafe_allow_html=True
)