import pandas as pd
import numpy as np

INPUT_FILE = "sbdb_query_results.csv"
OUTPUT_FILE = "objekte_ausserhalb_jupiter_aktuell.csv"
JUPITER_A = 5.2  # AE

# --- CSV laden ---
for sep in [",", ";", "\t"]:
    try:
        df = pd.read_csv(INPUT_FILE, sep=sep, low_memory=False)
        if "a" in df.columns:
            break
    except Exception:
        continue
else:
    raise ValueError("❌ Konnte Datei nicht laden – überprüfe das Trennzeichen.")

# --- Spalten normalisieren ---
df.columns = [c.strip().lower() for c in df.columns]

# Manche CSVs nennen 'm' anders (z. B. 'ma' oder 'mean_anomaly')
if "m" not in df.columns:
    if "ma" in df.columns:
        df["m"] = df["ma"]
    elif "mean_anomaly" in df.columns:
        df["m"] = df["mean_anomaly"]
    else:
        raise ValueError("❌ Keine Spalte 'm' oder 'ma' (mittlere Anomalie) gefunden!")

# --- numerische Spalten konvertieren ---
for col in ["a", "e", "m"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Kepler-Gleichung lösen ---
def solve_kepler(M, e, tol=1e-8):
    M = np.radians(M % 360)
    E = M if e < 0.8 else np.pi
    while True:
        dE = (M - (E - e * np.sin(E))) / (1 - e * np.cos(E))
        E += dE
        if np.all(np.abs(dE) < tol):
            break
    return E

def current_distance(a, e, M):
    E = solve_kepler(M, e)
    v = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                       np.sqrt(1 - e) * np.cos(E / 2))
    return a * (1 - e * np.cos(E))

# --- Aktuelle Sonnenentfernung berechnen ---
df["r"] = df.apply(lambda row: current_distance(row["a"], row["e"], row["m"]), axis=1)

# --- Filter: außerhalb der Jupiterbahn ---
outside = df[df["r"] > JUPITER_A].copy()

# --- Speichern ---
outside.to_csv(OUTPUT_FILE, index=False)

print(f"✅ {len(outside):,} Objekte außerhalb der Jupiterbahn gespeichert in '{OUTPUT_FILE}'")

# --- Zusatzinformationen ---
print(f"Gesamtobjekte: {len(df):,}")
print(f"Innerhalb Jupiterbahn: {(df['r'] <= JUPITER_A).sum():,}")
print(f"Außerhalb Jupiterbahn: {(df['r'] > JUPITER_A).sum():,}")
