import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timezone

# --- Bahnelemente (ungefähr für Epoche J2000) ---
PLANETS = {
    "Mercury": {"a": 0.3871, "e": 0.2056, "i": 7.005, "om": 48.331, "w": 29.124, "M0": 174.795},
    "Venus":   {"a": 0.7233, "e": 0.0067, "i": 3.394, "om": 76.680, "w": 54.884, "M0": 50.115},
    "Earth":   {"a": 1.0000, "e": 0.0167, "i": 0.000, "om": -11.260, "w": 114.207, "M0": 357.529},
    "Mars":    {"a": 1.5237, "e": 0.0934, "i": 1.850, "om": 49.558, "w": 286.502, "M0": 19.412},
    "Jupiter": {"a": 5.2028, "e": 0.0484, "i": 1.303, "om": 100.464, "w": 273.867, "M0": 20.020},
    "Saturn":  {"a": 9.5388, "e": 0.0542, "i": 2.485, "om": 113.665, "w": 339.392, "M0": 317.020},
    "Uranus":  {"a": 19.191, "e": 0.0472, "i": 0.770, "om": 74.006,  "w": 96.998,  "M0": 142.238},
    "Neptune": {"a": 30.068, "e": 0.0086, "i": 1.770, "om": 131.784, "w": 272.846, "M0": 256.228},
}


def solve_kepler(M, e, tol=1e-8):
    """Löst die Kepler-Gleichung M = E - e*sin(E) für die exzentrische Anomalie E."""
    E = M if e < 0.8 else np.pi
    while True:
        dE = (M - (E - e*np.sin(E))) / (1 - e*np.cos(E))
        E += dE
        if abs(dE) < tol:
            break
    return E


def add_planet_orbits(fig, planets):
    """Zeichnet Planetenbahnen, berechnet aktuelle Positionen und fügt Sonne hinzu."""
    now = datetime.now(timezone.utc)
    epoch = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    days_since = (now - epoch).total_seconds() / (3600 * 24)
    
    # Jahre seit J2000 für genauere Berechnung
    years_since = days_since / 365.25

    for name, el in planets.items():
        a, e = el["a"], el["e"]
        i, om, w, M0 = map(np.radians, [el["i"], el["om"], el["w"], el["M0"]])

        # --- Orbit-Kurve ---
        theta = np.linspace(0, 2*np.pi, 400)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
        x_orb, y_orb = r * np.cos(theta), r * np.sin(theta)

        X_orb = (np.cos(om)*np.cos(w)-np.sin(om)*np.sin(w)*np.cos(i))*x_orb + \
                (-np.cos(om)*np.sin(w)-np.sin(om)*np.cos(w)*np.cos(i))*y_orb
        Y_orb = (np.sin(om)*np.cos(w)+np.cos(om)*np.sin(w)*np.cos(i))*x_orb + \
                (-np.sin(om)*np.sin(w)+np.cos(om)*np.cos(w)*np.cos(i))*y_orb
        Z_orb = (np.sin(w)*np.sin(i))*x_orb + (np.cos(w)*np.sin(i))*y_orb

        fig.add_trace(go.Scatter3d(
            x=X_orb, y=Y_orb, z=Z_orb,
            mode="lines", line=dict(width=1), name=f"{name} Orbit"
        ))

        # --- aktuelle Position ---
        # Vereinfachte Berechnung: mittlere Anomalie für heutiges Datum
        # Umlaufzeit in Jahren: P = a^(3/2)
        P_years = a ** 1.5  # Keplers drittes Gesetz
        
        # Mittlere Anomalie in Grad für heutiges Datum
        M_deg = (M0 + (360 / P_years) * years_since) % 360
        M = np.radians(M_deg)
        
        # Exzentrische Anomalie mit Kepler-Gleichung
        E = solve_kepler(M, e)
        
        # Wahre Anomalie
        v = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                           np.sqrt(1 - e) * np.cos(E / 2))
        
        # Entfernung
        r_now = a * (1 - e * np.cos(E))
        
        # Position in der Bahnebene
        x0, y0 = r_now * np.cos(v), r_now * np.sin(v)

        # Rotation ins ekliptische Koordinatensystem
        X0 = (np.cos(om)*np.cos(w)-np.sin(om)*np.sin(w)*np.cos(i))*x0 + \
             (-np.cos(om)*np.sin(w)-np.sin(om)*np.cos(w)*np.cos(i))*y0
        Y0 = (np.sin(om)*np.cos(w)+np.cos(om)*np.sin(w)*np.cos(i))*x0 + \
             (-np.sin(om)*np.sin(w)+np.cos(om)*np.cos(w)*np.cos(i))*y0
        Z0 = (np.sin(w)*np.sin(i))*x0 + (np.cos(w)*np.sin(i))*y0

        fig.add_trace(go.Scatter3d(
            x=[X0], y=[Y0], z=[Z0],
            mode="markers+text",
            marker=dict(size=5),
            text=[name],
            textposition="top center",
            name=name
        ))

    # --- Sonne ---
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers+text",
        marker=dict(size=8, color="gold"),
        text=["Sun"],
        textposition="top center",
        name="Sun"
    ))