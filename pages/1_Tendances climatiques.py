import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import streamlit as st

@st.cache_data
def load_data():
    # Obtenir le dossier racine du projet (là où se trouve app.py)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construire les chemins vers les datasets
    datasets = {
        "df1": "GlobalLandTemperaturesByCity.csv",
        "df2": "decadal-average-annual-number-of-deaths-from-disasters.csv",
        "df3": "number-of-natural-disaster-events.csv"
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

    return dataframes["df1"], dataframes["df2"], dataframes["df3"]

# Charger les datasets
df, df_2, df_3 = load_data()

# Nettoyage des données
df.dropna(inplace=True)
df_2.dropna(inplace=True)
df_3.dropna(inplace=True)

# Affichage des premiers enregistrements de chaque dataset pour l'aperçu
st.subheader("Aperçu des Données Chargées")

st.subheader("Températures Globales par Ville")
st.write(df.head())

st.subheader("Moyenne Décennale des Décès dus aux Catastrophes Naturelles")
st.write(df_2.head())

st.subheader("Nombre d'Événements de Catastrophes Naturelles")
st.write(df_3.head())


st.title("🌍 Analyse des tendances climatiques et catastrophes naturelles")

# Nettoyage et filtrage des données
france_data = df[df["Country"] == "France"].copy()
france_data.dropna(inplace=True)
france_data['dt'] = pd.to_datetime(france_data['dt'], errors='coerce')
france_data['year'] = france_data['dt'].dt.year
annual_avg = france_data.groupby('year')['AverageTemperature'].mean().reset_index()

# Filtrage mondial
world_data = df.copy()
world_data.dropna(inplace=True)
world_data['dt'] = pd.to_datetime(world_data['dt'], errors='coerce')
world_data['year'] = world_data['dt'].dt.year
annual_avg_world = world_data.groupby('year')['AverageTemperature'].mean().reset_index()
annual_avg_world.rename(columns={'year': 'Year'}, inplace=True)



# Section 5: Graphique des températures en France
st.subheader("Évolution des températures en France")

# Créer un graphique interactif avec plotly
fig_temp = px.line(annual_avg[annual_avg['year'] >= 1950], x='year', y='AverageTemperature',
                   title='Température Moyenne Annuelle en France', 
                   labels={'year': 'Année', 'AverageTemperature': 'Température Moyenne (°C)'})

# Afficher le graphique interactif
st.plotly_chart(fig_temp)


# Chargement des décès liés aux catastrophes
DeathFrance = df_2[df_2["Country name"] == "France"].copy()
DeathFrance.dropna(inplace=True)

# Section : Nombre de morts dus aux catastrophes naturelles en France
st.subheader("Nombre de morts dus aux catastrophes naturelles en France")

# Filtrer les données à partir de 1980
DeathFrance_filtered = DeathFrance[DeathFrance['Year'] >= 1980]

# Créer un graphique interactif avec plotly
fig_deaths = px.line(DeathFrance_filtered, x='Year', y='Number of deaths from disasters',
                     title='Nombre annuel moyen de décès en France (depuis 1980)',
                     labels={'Year': 'Année', 'Number of deaths from disasters': 'Nombre de décès'},
                     line_shape='linear', markers=True, color_discrete_sequence=['red'])

# Afficher le graphique interactif
st.plotly_chart(fig_deaths)

# Catastrophes naturelles mondiales
DisastersWorld = df_3[df_3["Entity"].isin(["All disasters", "Flood"])].copy()

st.subheader("Catastrophes naturelles dans le monde")
fig = px.line(DisastersWorld, x="Year", y="Disasters", color="Entity", title="Nombre de catastrophes naturelles par an")
st.plotly_chart(fig)

# Création du premier graphique (aire empilée)
st.title("Analyse des Catastrophes Naturelles")
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

ax.fill_between(
    DisastersWorld[DisastersWorld['Entity'] == 'All disasters']['Year'], 
    DisastersWorld[DisastersWorld['Entity'] == 'All disasters']['Disasters'], 
    color='blue', alpha=0.6, label='All disasters'
)
ax.fill_between(
    DisastersWorld[DisastersWorld['Entity'] == 'Flood']['Year'], 
    DisastersWorld[DisastersWorld['Entity'] == 'Flood']['Disasters'], 
    color='red', alpha=0.6, label='Flood'
)
ax.set_title('Évolution des catastrophes naturelles (empilées)')
ax.set_xlabel('Année')
ax.set_ylabel('Nombre de catastrophes')
ax.legend()
ax.grid(True)

# Afficher la première figure dans Streamlit
st.pyplot(fig)

# Création du deuxième graphique (Boxplot)
fig_boxplot, ax_boxplot = plt.subplots(figsize=(10, 6))
sns.boxplot(y=DisastersWorld[DisastersWorld['Entity'] == 'All disasters']['Disasters'], 
            data=DisastersWorld, ax=ax_boxplot, color='lightblue')
ax_boxplot.set_title('Boxplot pour All disasters')

# Afficher le boxplot dans Streamlit
st.pyplot(fig_boxplot)

# ---- HEATMAP ----
heatmap_data = DisastersWorld[(DisastersWorld['Entity'] == 'All disasters') & (DisastersWorld['Year'] >= 1970)]
heatmap_data = heatmap_data.pivot(index="Year", columns="Entity", values="Disasters")

# Générer le heatmap
fig_heatmap, ax_heatmap = plt.subplots(figsize=(12, 8))
sns.heatmap(
    heatmap_data, cmap="coolwarm", annot=True, fmt=".1f", linewidths=0.5,
    annot_kws={"color": "black", "weight": "bold", "fontsize": 7}, ax=ax_heatmap
)
ax_heatmap.set_title('Carte de chaleur des catastrophes naturelles (All disasters seulement à partir de 1970)')
ax_heatmap.set_xlabel('Catastrophes')
ax_heatmap.set_ylabel('Année')
ax_heatmap.invert_yaxis()

# Afficher le heatmap dans Streamlit
st.pyplot(fig_heatmap)

# Fusion et corrélation entre température et catastrophes naturelles
DisastersWorld_filtered = DisastersWorld[DisastersWorld['Entity'] == 'All disasters'][['Year', 'Disasters']]
merged_df = pd.merge(DisastersWorld_filtered, annual_avg_world, on='Year')
correlation = merged_df[['Disasters', 'AverageTemperature']].corr()

st.subheader("Corrélation entre température et catastrophes")
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
st.pyplot(fig)

st.write("Corrélation entre la température moyenne et le nombre de catastrophes naturelles dans le monde")
