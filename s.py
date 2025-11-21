import pandas as pd
import numpy as np

INPUT_FILE = "sbdb_query_results.csv"
OUTPUT_FILE = "objekte_mit_aktueller_entfernung.csv"

# --- Grenzen der Planetenbahnen (in AE) ---
PLANETS = {
    "Jupiter": 5.2,
    "Saturn": 9.58,
    "Uranus": 19.2,
    "Neptun": 30.1,
}

# --- CSV laden (mit automatischer Trennzeichenerkennung) ---
for sep in [",", ";", "\t"]:
    try:
        df = pd.read_csv(INPUT_FILE, sep=sep, low_memory=False)
        if "a" in df.columns:
            break
    except Exception:
        continue
else:
    raise ValueError("❌ Konnte Datei nicht laden – überprüfe das Trennzeichen.")

# --- Spaltennamen normalisieren ---
df.columns = [c.strip().lower() for c in df.columns]

# --- 'm' (mittlere Anomalie) anpassen ---
if "m" not in df.columns:
    if "ma" in df.columns:
        df["m"] = df["ma"]
    elif "mean_anomaly" in df.columns:
        df["m"] = df["mean_anomaly"]
    else:
        raise ValueError("❌ Keine Spalte 'm' oder 'ma' gefunden!")

# --- numerische Werte sicherstellen ---
for col in ["a", "e", "m"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Kepler-Gleichung zum Berechnen der wahren Anomalie ---
def solve_kepler(M, e, tol=1e-8):
    """Löst M = E - e*sin(E) nach E (exzentrische Anomalie)."""
    M = np.radians(M % 360)
    E = M if e < 0.8 else np.pi
    while True:
        dE = (M - (E - e * np.sin(E))) / (1 - e * np.cos(E))
        E += dE
        if np.all(np.abs(dE) < tol):
            break
    return E

def current_distance(a, e, M):
    """Berechnet momentane Sonnenentfernung r aus a, e, M."""
    if pd.isna(a) or pd.isna(e) or pd.isna(M):
        return np.nan
    E = solve_kepler(M, e)
    return a * (1 - e * np.cos(E))

# --- Momentane Sonnenentfernung berechnen ---
df["r"] = df.apply(lambda row: current_distance(row["a"], row["e"], row["m"]), axis=1)

# --- Statistik berechnen ---
total = len(df)
inside_jupiter = (df["r"] <= PLANETS["Jupiter"]).sum()
between_jup_sat = ((df["r"] > PLANETS["Jupiter"]) & (df["r"] <= PLANETS["Saturn"])).sum()
between_sat_ura = ((df["r"] > PLANETS["Saturn"]) & (df["r"] <= PLANETS["Uranus"])).sum()
between_ura_nep = ((df["r"] > PLANETS["Uranus"]) & (df["r"] <= PLANETS["Neptun"])).sum()
outside_neptune = (df["r"] > PLANETS["Neptun"]).sum()

print("🌞 Aktuelle Verteilung der Objekte nach Sonnenentfernung (in AE):")
print(f"Gesamtobjekte:       {total:,}")
print(f"  ≤ Jupiter ({PLANETS['Jupiter']} AE):        {inside_jupiter:,}")
print(f"  Jupiter–Saturn ({PLANETS['Saturn']} AE):    {between_jup_sat:,}")
print(f"  Saturn–Uranus ({PLANETS['Uranus']} AE):     {between_sat_ura:,}")
print(f"  Uranus–Neptun ({PLANETS['Neptun']} AE):     {between_ura_nep:,}")
print(f"  > Neptun:                                  {outside_neptune:,}")

# --- CSV speichern (optional) ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n✅ Datei '{OUTPUT_FILE}' gespeichert – enthält Spalte 'r' (aktuelle Entfernung in AE).")
