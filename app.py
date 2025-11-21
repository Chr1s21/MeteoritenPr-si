import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_utils import load_data, prepare_dataframe
from planets import PLANETS, add_planet_orbits
from orbit_calculations import compute_object_positions, add_object_orbits
from plot_utils import setup_plot

# --- Streamlit Setup ---
st.set_page_config(page_title="Solar System Visualizer", layout="wide")
st.title("🌌 3D Solar System Visualizer")
st.markdown("Visualisierung von Planetenbahnen und Asteroiden/Kometenbahnen aus deiner CSV-Datei.")

# --- Daten laden ---
df = load_data("sbdb_query_results.csv")
df = prepare_dataframe(df)




# --- Sidebar ---
st.sidebar.header("🔍 Anzeigeoptionen")
show_orbits = st.sidebar.toggle("Asteroiden-/Kometenbahnen anzeigen", value=False)

only_tg422 = st.sidebar.toggle("Nur TG422 anzeigen", value=False)

if only_tg422:
    df = df[df["full_name"].str.contains("TG422", case=False, na=False)]



# --- Level of Detail ---
inner = df[df["a"] <= 5]
outer = df[df["a"] > 5]

# Gesamtlimit – wenn Bahnen aktiv, kleinere Menge für Performance
MAX_TOTAL = 10000 if not show_orbits else 2000

# 🎯 Exakte Zielwerte statt Verhältnis
# Du kannst diese beiden Werte direkt anpassen:
TARGET_INNER = 200
TARGET_OUTER = 6800

# --- Automatische Begrenzung auf vorhandene Daten ---
target_inner = min(len(inner), TARGET_INNER)
target_outer = min(len(outer), TARGET_OUTER)


# --- Stichproben ziehen ---
inner_sample = inner.sample(n=target_inner, random_state=42)
outer_sample = outer.sample(n=target_outer, random_state=42)
objs = pd.concat([inner_sample, outer_sample])

# --- Bahnen nur für kleine Teilmenge (Performance) ---
if show_orbits:
    objs_orbits = objs.sample(min(len(objs), 400), random_state=1)
else:
    objs_orbits = objs

# --- Sidebar-Infos ---
st.sidebar.markdown(f"**Innere Objekte:** {len(inner_sample):,}")
st.sidebar.markdown(f"**Äußere Objekte:** {len(outer_sample):,}")
st.sidebar.markdown(f"**Gesamt:** {len(objs):,}")
st.sidebar.markdown(f"**Gesamt verfügbar:** {len(df):,}")

# --- Plot aufbauen ---
fig = setup_plot()
add_planet_orbits(fig, PLANETS)
compute_object_positions(fig, objs)
if show_orbits:
    add_object_orbits(fig, objs_orbits)

st.plotly_chart(fig, config={"responsive": True, "displayModeBar": True})

