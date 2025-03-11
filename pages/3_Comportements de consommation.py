import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objs as go
import plotly.graph_objs as go
import streamlit as st
from plotly.subplots import make_subplots
import seaborn as sns

# Utilisation de cache pour améliorer les performances de chargement des données
@st.cache_data
def load_data():
    # Obtenir le dossier racine du projet (là où se trouve app.py)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construire les chemins vers les datasets
    datasets = {
        "df": "GlobalLandTemperaturesByCity.csv",
        "electricity_generation": "electricity-generation.csv",
        "primary_consumption": "primary-energy-cons.csv",
        "electricity_imports": "net-electricity-imports.csv",
        "global_consumption": "primary-energy-cons-fr-eu-ch.csv",
        "consumption_co2_per_capita": "consumption-co2-per-capita.csv"
    }

    # Charger les fichiers
    dataframes = {}
    for key, filename in datasets.items():
        csv_path = os.path.join(root_dir, "dataset", filename)
        
        if os.path.exists(csv_path):
            dataframes[key] = pd.read_csv(csv_path)
            print(f"✅ {filename} chargé avec succès !")
        else:
            print(f"⚠️ ERREUR : Fichier introuvable à {csv_path}")
            dataframes[key] = None  # Évite un plantage en cas d'erreur

    return dataframes

# Charger les datasets
dataframes = load_data()

# Extraire les données individuelles
df = dataframes["df"]
electricity_generation = dataframes["electricity_generation"]
primary_consumption = dataframes["primary_consumption"]
electricity_imports = dataframes["electricity_imports"]
global_consumption = dataframes["global_consumption"]
emissions_co2 = dataframes["consumption_co2_per_capita"]

# Nettoyage des données
electricity_generation.dropna(inplace=True)
primary_consumption.dropna(inplace=True)
electricity_imports.dropna(inplace=True)
global_consumption.dropna(inplace=True)
emissions_co2.dropna(inplace=True)

# Affichage des premiers enregistrements de chaque dataset pour l'aperçu
st.subheader("Aperçu des Données Chargées")

st.subheader("Production d'Électricité")
st.write(electricity_generation.head())

st.subheader("Consommation d'Énergie Primaire")
st.write(primary_consumption.head())

st.subheader("Importation d'Électricité")
st.write(electricity_imports.head())

st.subheader("Consommation d'Énergie Globale")
st.write(global_consumption.head())

st.subheader("Émissions de CO2 par Personne")
st.write(emissions_co2.head())


# Application Streamlit
st.title("Analyse de la Consommation d'Énergie et des Émissions de CO2")

# Section 1: Émissions de CO2 par personne
st.header("Emissions de CO2 par personne")
st.write("Comparaison des émissions de CO2 par personne entre la Chine, l'Europe et les États-Unis.")
china_data_emis = emissions_co2[emissions_co2['Entity'] == 'China']
europe_data_emis = emissions_co2[emissions_co2['Code'] == 'EU']
us_data_emis = emissions_co2[emissions_co2['Entity'] == 'United States']

fig = go.Figure()

# Ajouter la trace pour la Chine
fig.add_trace(go.Scatter(x=china_data_emis['Year'], 
                         y=china_data_emis['Per capital consumption-based CO₂ emissions (t)'],
                         mode='lines', 
                         name='China', 
                         line=dict(color='red')))

# Ajouter la trace pour l'Europe
fig.add_trace(go.Scatter(x=europe_data_emis['Year'], 
                         y=europe_data_emis['Per capital consumption-based CO₂ emissions (t)'],
                         mode='lines', 
                         name='Europe', 
                         line=dict(color='blue')))

# Ajouter la trace pour les États-Unis
fig.add_trace(go.Scatter(x=us_data_emis['Year'], 
                         y=us_data_emis['Per capital consumption-based CO₂ emissions (t)'],
                         mode='lines', 
                         name='United States', 
                         line=dict(color='green')))

# Mise en forme du graphique
fig.update_layout(
    title='CO₂ Emissions per capita Over Time',
    xaxis_title='Year',
    yaxis_title='CO₂ Emissions per capita (t)',
    showlegend=True
)

# Affichage du graphique interactif dans Streamlit
st.plotly_chart(fig)


# Section 2: Production et Importation d'Électricité en France
st.header("Production et Importation d'Électricité en France")
df_france = electricity_imports[electricity_imports["Entity"] == "France"]
electricity_generation_fr = electricity_generation[['Year', 'Electricity generation - TWh']]
electricity_importation = df_france[['Year', 'Net imports - TWh']]

# Fusionner les données
df_merged = pd.merge(electricity_generation_fr, electricity_importation, on="Year")

# Créer le graphique interactif
fig_france = go.Figure()

# Graphique de la production d'électricité
fig_france.add_trace(go.Scatter(
    x=df_merged["Year"],
    y=df_merged["Electricity generation - TWh"],
    mode='lines+markers',
    name="Électricité produite (TWh)",
    line=dict(color='blue'),
))

# Graphique de l'importation d'électricité
fig_france.add_trace(go.Scatter(
    x=df_merged["Year"],
    y=df_merged["Net imports - TWh"],
    mode='lines+markers',
    name="Électricité importée (TWh)",
    line=dict(color='purple'),
))

# Mise à jour de la mise en page
fig_france.update_layout(
    title="Production et Importation d'Électricité en France",
    xaxis_title="Année",
    yaxis_title="TWh",
    showlegend=True,
    height=500
)

# Afficher le graphique interactif
st.plotly_chart(fig_france)

# Section 3: Consommation d'Énergie Primaire
st.header("Consommation d'Énergie Primaire")
st.write("Comparaison de la consommation d'énergie primaire entre la Chine, l'Europe et les États-Unis.")

# Extraire les données pour chaque pays
china_data = global_consumption[global_consumption['Entity'] == 'China']
europe_data = global_consumption[global_consumption['Code'] == 'EU']
us_data = global_consumption[global_consumption['Entity'] == 'United States']

# Créer la figure
fig = go.Figure()

# Ajouter une trace pour la Chine
fig.add_trace(go.Scatter(
    x=china_data['Year'], 
    y=china_data['Primary energy consumption (TWh)'],
    mode='lines',
    name='China',
    line=dict(color='red')
))

# Ajouter une trace pour l'Europe
fig.add_trace(go.Scatter(
    x=europe_data['Year'], 
    y=europe_data['Primary energy consumption (TWh)'],
    mode='lines',
    name='Europe',
    line=dict(color='blue')
))

# Ajouter une trace pour les États-Unis
fig.add_trace(go.Scatter(
    x=us_data['Year'], 
    y=us_data['Primary energy consumption (TWh)'],
    mode='lines',
    name='United States',
    line=dict(color='green')
))

# Mettre à jour la mise en page
fig.update_layout(
    title='Primary Energy Consumption Over Time',
    xaxis_title='Year',
    yaxis_title='Primary Energy Consumption (TWh)',
    legend_title='Countries',
    hovermode='x unified'
)

# Afficher le graphique interactif dans Streamlit
st.plotly_chart(fig)


# Section 4: Graphiques Complexes
st.header("Graphiques Complexes")
energy_china = global_consumption[global_consumption['Entity'] == 'China']
energy_europe = global_consumption[global_consumption['Entity'] == 'Europe']
energy_am = global_consumption[global_consumption['Entity'] == 'United States']

# Graphique 1 : Consommation d'énergie en Chine
fig_china = go.Figure()
fig_china.add_trace(go.Scatter(
    x=energy_china['Year'], 
    y=energy_china['Primary energy consumption (TWh)'],
    mode='markers',
    name='China',
    marker=dict(color='red')
))

fig_china.update_layout(
    title="Primary Energy Consumption in China",
    xaxis_title="Year",
    yaxis_title="Primary Energy Consumption (TWh)",
    showlegend=True,
    height=400,
)

# Afficher le graphique interactif pour la Chine
st.plotly_chart(fig_china)

# Graphique 2 : Consommation d'énergie en Europe
fig_europe = go.Figure()
fig_europe.add_trace(go.Scatter(
    x=energy_europe['Year'], 
    y=energy_europe['Primary energy consumption (TWh)'],
    mode='markers',
    name='Europe',
    marker=dict(color='blue')
))

fig_europe.update_layout(
    title="Primary Energy Consumption in Europe",
    xaxis_title="Year",
    yaxis_title="Primary Energy Consumption (TWh)",
    showlegend=True,
    height=400,
)

# Afficher le graphique interactif pour l'Europe
st.plotly_chart(fig_europe)

# Graphique 3 : Consommation d'énergie aux États-Unis
fig_us = go.Figure()
fig_us.add_trace(go.Scatter(
    x=energy_am['Year'], 
    y=energy_am['Primary energy consumption (TWh)'],
    mode='markers',
    name='United States',
    marker=dict(color='green')
))

fig_us.update_layout(
    title="Primary Energy Consumption in the United States",
    xaxis_title="Year",
    yaxis_title="Primary Energy Consumption (TWh)",
    showlegend=True,
    height=400,
)

# Afficher le graphique interactif pour les États-Unis
st.plotly_chart(fig_us)

# Filtrer les données pour la France
france_data = df[df["Country"] == "France"].copy()
france_data.dropna(inplace=True)

# Convertir la colonne 'dt' en datetime
france_data['dt'] = pd.to_datetime(france_data['dt'], errors='coerce')

# Extraire l'année et calculer la moyenne des températures par année
france_data['year'] = france_data['dt'].dt.year
annual_avg = france_data.groupby('year')['AverageTemperature'].mean().reset_index()
annual_avg_filtered = annual_avg[annual_avg['year'] >= 1950]

# Filtrer les données pour la consommation d'énergie de la Chine, l'Europe et les États-Unis
global_energy_data = global_consumption[global_consumption['Entity'].isin(['China', 'Europe', 'United States'])]

# Regrouper par année et sommer la consommation
global_energy_avg = global_energy_data.groupby('Year')['Primary energy consumption (TWh)'].sum().reset_index()

# Renommer la colonne pour correspondre à celle de `annual_avg_filtered`
global_energy_avg.rename(columns={'Year': 'year'}, inplace=True)

# Filtrer les données de consommation à partir de 1950
global_energy_avg = global_energy_avg[global_energy_avg['year'] >= 1950]

# Fusionner les données avec les températures
merged_data = pd.merge(annual_avg_filtered, global_energy_avg, on='year')

# Calculer la corrélation entre la température moyenne et la consommation d'énergie
temp_energy_correlation = merged_data[['AverageTemperature', 'Primary energy consumption (TWh)']].corr()

# Afficher la corrélation dans Streamlit
st.write("### Corrélation entre la Température Moyenne et la Consommation d'Énergie Primaire")
st.write(temp_energy_correlation)

# Visualisation des tendances
fig, ax1 = plt.subplots(figsize=(10, 6))

# Tracer la température (axe gauche)
ax1.set_xlabel('Année')
ax1.set_ylabel('Température Moyenne (°C)', color='black')
sns.lineplot(data=merged_data, x='year', y='AverageTemperature', marker='o', color='black', ax=ax1)
ax1.tick_params(axis='y', labelcolor='black')

# Créer un second axe pour la consommation d'énergie (axe droit)
ax2 = ax1.twinx()
ax2.set_ylabel('Consommation d\'énergie primaire (TWh)', color='blue')
sns.lineplot(data=merged_data, x='year', y='Primary energy consumption (TWh)', marker='s', color='blue', ax=ax2)
ax2.tick_params(axis='y', labelcolor='blue')

# Ajouter un titre
plt.title("Corrélation entre la Température Moyenne et la Consommation d'Énergie Primaire")

# Afficher le graphique dans Streamlit
st.pyplot(fig)
