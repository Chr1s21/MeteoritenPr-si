import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
import time

st.set_page_config(page_title="Clustering Analyse", layout="wide")
st.title("🔬 Clustering-Analyse: Kometen vs. Asteroiden")

# --- Tabs für verschiedene Analysen ---
tab1, tab2, tab3 = st.tabs(["Komet vs. Asteroid", "Asteroidenfamilien", "Erklärung"])

# --- Überprüfen, ob die erforderlichen Dateien vorhanden sind ---
required_files = [
    "csv/clustered_kometVsAsteroid_kmeans.csv",
    "csv/clustered_kometVsAsteroid_dbscan.csv",
    "csv/clustered_families_kmeans.csv",
    "csv/clustered_families_dbscan.csv",
]

missing_files = [file for file in required_files if not os.path.exists(file)]
if missing_files:
    st.error(f"Die folgenden Dateien fehlen: {', '.join(missing_files)}")

with tab1:
    st.header("Tisserand-Parameter Clustering")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("K-Means Clustering")
        try:
            with st.spinner("Lade K-Means-Daten..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)  # Simuliert Ladezeit
                    progress.progress(i + 1)

                df_kmeans = pd.read_csv("csv/clustered_kometVsAsteroid_kmeans.csv")
                # Sample für Performance
                df_plot = (
                    df_kmeans[["t_jup", "i", "cluster"]]
                    .dropna()
                    .sample(n=min(20000, len(df_kmeans)), random_state=42)
                )

                fig = px.scatter(
                    df_plot,
                    x="t_jup",
                    y="i",
                    color="cluster",
                    color_continuous_scale="RdBu",
                    title="K-Means: Komet vs. Asteroid",
                    labels={"t_jup": "Tisserand-Parameter", "i": "Inklination [°]"},
                )
                fig.add_vline(
                    x=3.0,
                    line_dash="dash",
                    line_color="black",
                    annotation_text="Kometen-Grenze T_J=3",
                )
                st.plotly_chart(fig, use_container_width=True)
        except FileNotFoundError:
            st.error(
                "Datei nicht gefunden. Bitte führe zuerst das Clustering-Notebook aus."
            )

    with col2:
        st.subheader("DBSCAN Clustering")
        try:
            with st.spinner("Lade DBSCAN-Daten..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)  # Simuliert Ladezeit
                    progress.progress(i + 1)

                df_dbscan = pd.read_csv("csv/clustered_kometVsAsteroid_dbscan.csv")
                df_plot = (
                    df_dbscan[["t_jup", "i", "cluster"]]
                    .dropna()
                    .sample(n=min(20000, len(df_dbscan)), random_state=42)
                )

                fig = px.scatter(
                    df_plot,
                    x="t_jup",
                    y="i",
                    color="cluster",
                    color_continuous_scale="Viridis",
                    title="DBSCAN: Komet vs. Asteroid (Rauschen = -1)",
                    labels={"t_jup": "Tisserand-Parameter", "i": "Inklination [°]"},
                )
                fig.add_vline(x=3.0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        except FileNotFoundError:
            st.error("Datei nicht gefunden.")

with tab2:
    st.header("Asteroidenfamilien im Hauptgürtel")

    # Auswahl zwischen K-Means und DBSCAN
    clustering_method = st.radio("Wähle die Clustering-Methode:", ("K-Means", "DBSCAN"))

    try:
        with st.spinner(f"Lade {clustering_method}-Daten..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)  # Simuliert Ladezeit
                progress.progress(i + 1)

            if clustering_method == "K-Means":
                df_families = pd.read_csv("csv/clustered_families_kmeans.csv")
            else:
                df_families = pd.read_csv("csv/clustered_families_dbscan.csv")

            df_plot = df_families[["a", "i", "cluster"]].dropna()
            df_plot = df_plot[(df_plot["a"] > 1.5) & (df_plot["a"] < 4.5)]
            df_plot = df_plot.sample(n=min(50000, len(df_plot)), random_state=42)

            fig = px.scatter(
                df_plot,
                x="a",
                y="i",
                color="cluster",
                color_continuous_scale="Spectral",
                title=f"Asteroidenfamilien ({clustering_method})",
                labels={"a": "Große Halbachse [AU]", "i": "Inklination [°]"},
            )
            st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error(
            "Datei nicht gefunden. Bitte führe zuerst das Clustering-Notebook aus."
        )

with tab3:
    st.header("📚 Was zeigt diese Analyse?")

    st.markdown(
        """
    ### Tisserand-Parameter
    Der **Tisserand-Parameter** $T_J$ ist ein Maß für die Bahnenergie eines Objekts 
    relativ zu Jupiter:
    
    $$T_J = \\frac{a_J}{a} + 2\\cos(i)\\sqrt{\\frac{a}{a_J}(1-e^2)}$$
    
    - **$T_J < 3$**: Wahrscheinlich ein **Komet** (Jupiter-Kreuzend)
    - **$T_J > 3$**: Wahrscheinlich ein **Asteroid**
    
    ### Clustering-Methoden
    | Methode | Vorteile | Nachteile |
    |---------|----------|-----------|
    | **K-Means** | Schnell, einfach | Braucht vorgegebene Cluster-Anzahl |
    | **DBSCAN** | Findet beliebige Formen, erkennt Rauschen | Parameter-sensitiv |
    """
    )
