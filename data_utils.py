import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path):
    try:
        df = pd.read_csv(path, low_memory=False)
    except Exception:
        try:
            df = pd.read_csv(path, sep=";", low_memory=False)
        except Exception:
            df = pd.read_csv(path, sep="\t", low_memory=False)
    df = df.rename(columns={"ma": "M"})
    return df

def prepare_dataframe(df):
    # prüfe & bereinige Spalten
    required = ["a", "e"]
    for col in required:
        if col not in df.columns:
            st.error(f"❌ CSV benötigt die Spalte '{col}'")
            st.stop()
    for col in ["a", "e", "i", "om", "w", "M"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["a", "e"])
    return df
