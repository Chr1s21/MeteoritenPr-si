import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_utils import load_data, prepare_dataframe
from planets import PLANETS, add_planet_orbits
from orbit_calculations import compute_object_positions, add_object_orbits
from plot_utils import setup_plot

st.set_page_config(page_title="Solar System Visualizer", layout="wide")
st.title("🌌 3D Solar System Visualizer")
st.markdown("Visualisierung von Planetenbahnen und Asteroiden/Kometenbahnen aus deiner CSV-Datei.")

# --- MAPPING: Anzeigename zu Dateipfad ---
FILE_MAPPING = {
    "1. Alle Objekte (Ungeclustert)": "sbdb_query_results.csv",
    "2. Familien (DBSCAN Cluster)": "csvs/clustered_families_dbscan.csv",
    "3. Familien (K-Means Cluster)": "csvs/clustered_families_kmeans.csv",
    "4. Komet vs. Asteroid (K-Means)": "csvs/clustered_kometVsAsteroid_kmeans.csv",
    "5. Komet vs. Asteroid (DBSCAN)": "csvs/clustered_kometVsAsteroid_dbscan.csv"
}
# --- ENDE MAPPING ---

# --- CSV-Auswahl in der Sidebar ---
st.sidebar.header("📂 Datenquelle")

# Zeige nur die Anzeigenamen in der Selectbox
display_name = st.sidebar.selectbox(
    "Welche CSV soll verwendet werden?",
    list(FILE_MAPPING.keys()), # Liste der Anzeigenamen
    index=0,
)

# Verwende das Mapping, um den tatsächlichen Dateipfad zu erhalten
csv_file = FILE_MAPPING[display_name]

cluster_column = "cluster"

# --- Daten laden ---
df = load_data(csv_file)
df = prepare_dataframe(df)

# --- Sidebar ---
st.sidebar.header("🔍 Anzeigeoptionen")
show_orbits = st.sidebar.toggle("Asteroiden-/Kometenbahnen anzeigen", value=False)

# --- NEUER FILTER: Extremer Winkel / Hohe Inklination (Feste Auswahl) ---

INCLINATION_OPTIONS = {
    "Alle Objekte (i ≥ 0°)": 0,
    "Hohe Inklination (i ≥ 45°)": 45,
    "Extrem/Retrograd (i ≥ 90°)": 90
}

selected_option_label = st.sidebar.selectbox(
    "Filtern: Minimaler Neigungswinkel",
    list(INCLINATION_OPTIONS.keys()),
    index=0 # Setze den Standardwert auf 0° (Alle Objekte)
)

min_inclination = INCLINATION_OPTIONS[selected_option_label]

# Führe den Filter durch
if min_inclination > 0:
    # Die Spalte 'i' (Inklination) muss in Grad vorliegen
    df = df[df["i"] >= min_inclination]
# --- ENDE NEUER FILTER ---


only_tg422 = st.sidebar.toggle("Nur TG422 anzeigen", value=False)

if only_tg422:
    df = df[df["full_name"].str.contains("TG422", case=False, na=False)]


# --- Level of Detail ---
inner = df[df["a"] <= 5]
outer = df[df["a"] > 5]

# Gesamtlimit – wenn Bahnen aktiv, kleinere Menge für Performance
# HINWEIS: Hier wurde MAX_TOTAL auf 10000/2000 belassen.
MAX_TOTAL = 10000 if not show_orbits else 2000

# 🎯 Exakte Zielwerte statt Verhältnis
# Du kannst diese beiden Werte direkt anpassen:
TARGET_INNER = 200
TARGET_OUTER = 6800

# --- Automatische Begrenzung auf vorhandene Daten ---
target_inner = min(len(inner), TARGET_INNER)
target_outer = min(len(outer), TARGET_OUTER)


# --- Stichproben ziehen ---
if len(inner) > 0:
    inner_sample = inner.sample(n=target_inner, random_state=42)
else:
    inner_sample = inner # leer
    
if len(outer) > 0:
    outer_sample = outer.sample(n=target_outer, random_state=42)
else:
    outer_sample = outer # leer

objs = pd.concat([inner_sample, outer_sample])

# --- Bahnen nur für kleine Teilmenge (Performance) ---
if show_orbits:
    objs_orbits = objs.sample(min(len(objs), 400), random_state=1)
else:
    objs_orbits = objs

# --- Sidebar-Infos ---
st.sidebar.markdown(f"**Gefiltert:** {len(df):,}")
st.sidebar.markdown(f"**Innere Objekte:** {len(inner_sample):,}")
st.sidebar.markdown(f"**Äußere Objekte:** {len(outer_sample):,}")
st.sidebar.markdown(f"**Aktuell gezeichnet:** {len(objs):,}")
st.sidebar.markdown(f"**Gesamt verfügbar (ungf.):** {len(load_data(csv_file)):,}")


# --- Plot aufbauen ---
fig = setup_plot()
add_planet_orbits(fig, PLANETS)
compute_object_positions(fig, objs, cluster_column=cluster_column)
if show_orbits:
    add_object_orbits(fig, objs_orbits, cluster_column=cluster_column)

st.plotly_chart(fig, config={"responsive": True, "displayModeBar": True})