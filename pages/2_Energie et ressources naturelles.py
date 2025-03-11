import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Fonction pour charger les données
@st.cache_data
def load_data():
    # Obtenir le dossier racine du projet (là où se trouve app.py)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construire les chemins vers les datasets
    datasets = {
        "electricity_generation": "electricity-generation.csv",
        "primary_consumption": "primary-energy-cons.csv",
        "change_energy_consumption": "change-energy-consumption.csv",
        "change_energy_consumption_ch": "change-energy-consumption_ch.csv"
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
data = load_data()
electricity_generation = data["electricity_generation"]
primary_consumption = data["primary_consumption"]
annual_change_fr = data["change_energy_consumption"]
annual_change_ch = data["change_energy_consumption_ch"]

# Nettoyage et aperçu des données
electricity_generation.dropna(inplace=True)
primary_consumption.dropna(inplace=True)
annual_change_fr.dropna(inplace=True)
annual_change_ch.dropna(inplace=True)

# Affichage des premiers enregistrements de chaque dataset pour l'aperçu
st.subheader('Aperçu de la production d\'électricité en France')
st.write(electricity_generation.head())

st.subheader('Aperçu de la consommation d\'énergie primaire en France')
st.write(primary_consumption.head())

st.subheader('Aperçu du changement annuel de la consommation d\'énergie en France')
st.write(annual_change_fr.head())

# Graphiques
st.title("Analyse de l'Énergie et des Ressources Naturelles")

# Production d'électricité
st.subheader("Production d'Électricité en France (TWh)")
electricity_generation_plot = electricity_generation[['Year', 'Electricity generation - TWh']]
fig1, ax1 = plt.subplots(figsize=(10,6))
electricity_generation_plot.plot(x='Year', y='Electricity generation - TWh', ax=ax1, legend=True)
st.pyplot(fig1)

# Boxplot de la production d'électricité
st.subheader("Boxplot de la Production d'Électricité")
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.boxplot(y='Electricity generation - TWh', data=electricity_generation, ax=ax2)
st.pyplot(fig2)

# Consommation d'énergie primaire
st.subheader("Consommation d'Énergie Primaire en France (TWh)")
energy_consumption = primary_consumption[['Year', 'Primary energy consumption (TWh)']]
fig3, ax3 = plt.subplots(figsize=(10,6))
energy_consumption.plot(x='Year', y='Primary energy consumption (TWh)', ax=ax3, legend=True)
st.pyplot(fig3)

# Boxplot de la consommation d'énergie primaire
st.subheader("Boxplot de la Consommation d'Énergie Primaire")
fig4, ax4 = plt.subplots(figsize=(10,6))
sns.boxplot(y='Primary energy consumption (TWh)', data=primary_consumption, ax=ax4)
st.pyplot(fig4)

# Corrélation entre la production d'électricité et la consommation d'énergie primaire
st.subheader("Carte thermique de la corrélation entre la production d'électricité et la consommation d'énergie primaire")
merged_df = pd.merge(electricity_generation, primary_consumption, on='Year')
correlation = merged_df[['Electricity generation - TWh', 'Primary energy consumption (TWh)']].corr()
fig5, ax5 = plt.subplots(figsize=(10,5))
sns.heatmap(correlation, cmap='coolwarm', annot=True, fmt='.2f', ax=ax5)
ax5.set_title('Corrélation entre la production d\'électricité et la consommation d\'énergie primaire')
st.pyplot(fig5)

# Fluctuation de la consommation d'énergie primaire en France
st.subheader("Fluctuation annuelle de la consommation d'énergie primaire en France")
fig6, ax6 = plt.subplots(figsize=(10,6))
sns.histplot(annual_change_fr['Annual change in primary energy consumption (%)'], kde=True, ax=ax6)
st.pyplot(fig6)

# Comparaison entre la France et la Chine
st.subheader("Comparaison entre la France et la Chine : Changement annuel de la consommation d'énergie primaire")
fig7, ax7 = plt.subplots(1, 2, figsize=(15,6))

sns.histplot(annual_change_fr['Annual change in primary energy consumption (%)'], kde=True, ax=ax7[0])
ax7[0].set_title('France')
sns.histplot(annual_change_ch['Annual change in primary energy consumption (%)'], kde=True, ax=ax7[1])
ax7[1].set_title('Chine')
st.pyplot(fig7)

# Comparaison des courbes pour la France et la Chine
st.subheader("Comparaison des courbes de consommation d'énergie primaire")
fig8, ax8 = plt.subplots(figsize=(10, 5))
plt.plot(annual_change_fr['Year'], annual_change_fr['Annual change in primary energy consumption (%)'], 
         label='France', color='blue', marker='o')
plt.plot(annual_change_ch['Year'], annual_change_ch['Annual change in primary energy consumption (%)'], 
         label='Chine', color='red', marker='o')
plt.xlabel("Année")
plt.ylabel("Changement annuel (%)")
plt.title("Évolution du changement annuel de la consommation d'énergie primaire")
plt.legend()
plt.grid(True)
st.pyplot(fig8)
