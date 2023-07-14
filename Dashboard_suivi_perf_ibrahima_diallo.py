import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def merge_data(data_files):
    if len(data_files) < 2:
        return {'error': 'Veuillez fournir au moins deux fichiers de données.'}

    data_frames = []
    for file in data_files:
        if file.name.endswith('.csv'):
            data_frames.append(pd.read_csv(file))
        elif file.name.endswith('.xlsx'):
            data_frames.append(pd.read_excel(file))
        else:
            return {'error': 'Format de fichier non pris en charge. Veuillez utiliser des fichiers CSV ou Excel.'}

    merged_data = data_frames[0]  # Prend le premier DataFrame comme point de départ de la fusion
    for i in range(1, len(data_frames)):
        merged_data = pd.merge(merged_data, data_frames[i], on="cookie_id")
    return merged_data

def create_charts(data):
    st.subheader("Box plot de l'âge moyen en fonction des product_id")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="product_id", y="age", data=data)
    plt.xlabel("product_id")
    plt.ylabel("Âge moyen")
    plt.title("Distribution de l'âge moyen en fonction des product_id")
    st.pyplot(fig)

    st.subheader("Histogramme des clics sur les bannières")
    histo = px.histogram(data, x="product_id", y="price")
    fig, ax = plt.subplots()
    ax.bar(histo.data[0].x, histo.data[0].y)
    plt.xlabel("product_id")
    plt.ylabel("Nombre de clics")
    plt.title("Histogramme des clics sur les bannières")
    st.pyplot(fig)

    # Conversion de la colonne 'dept' en numérique
    data['dept'] = pd.to_numeric(data['dept'], errors='coerce')

    # Diagramme circulaire des dépenses totales en fonction du genre
    st.subheader("Dépenses totales en fonction du genre")
    total_expenses = data.groupby('gender')['dept'].sum().reset_index()
    fig = px.pie(total_expenses, values='dept', names='gender', title='Dépenses totales en fonction du genre')
    st.plotly_chart(fig)

def main():
    st.title("IBRAHIMA DIALLO ISE2")
    st.write("Veuillez sélectionner au moins deux fichiers de données pour la fusion.")

    data_files = st.file_uploader("Télécharger les fichiers de données", accept_multiple_files=True)
    if data_files:
        base_fusion = merge_data(data_files)
        st.write("Données fusionnées :")
        st.write(base_fusion)

        # Filtrage des données
        st.sidebar.subheader("Filtrer les données")
        product_id_filter = st.sidebar.multiselect("Product ID", base_fusion['product_id'].unique())
        gender_filter = st.sidebar.multiselect("Genre", base_fusion['gender'].unique())

        filtered_data = base_fusion[
            (base_fusion['product_id'].isin(product_id_filter)) &
            (base_fusion['gender'].isin(gender_filter))
        ]

        # Affichage des données filtrées
        st.write("Données filtrées :")
        st.write(filtered_data)

        chiffre_daff = filtered_data['price'].sum()
        chiffre_daff_euro = f"{chiffre_daff} €"
        st.info(f"Chiffre d'affaire : **{chiffre_daff_euro}**")

        # Création des graphiques en fonction des données filtrées
        create_charts(filtered_data)

        # Enregistrer les données filtrées dans un fichier CSV
        st.subheader("Enregistrer les données filtrées")
        save_csv = st.button("Enregistrer en CSV")
        if save_csv:
            filtered_data.to_csv("donnees_filtrees.csv", index=False)
            st.success("Les données filtrées ont été enregistrées avec succès dans le fichier donnees_filtrees.csv")

if __name__ == "__main__":
    main()
