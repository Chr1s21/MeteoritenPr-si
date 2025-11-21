import numpy as np
import plotly.graph_objects as go

def compute_object_positions(fig, df):
    Xs, Ys, Zs, texts = [], [], [], []
    for _, row in df.iterrows():
        a, e = row["a"], row["e"]
        inc, om, w, M = np.radians(row["i"]), np.radians(row["om"]), np.radians(row["w"]), np.radians(row["M"])
        r_now = (a * (1 - e**2)) / (1 + e * np.cos(M))
        x0, y0 = r_now * np.cos(M), r_now * np.sin(M)
        X0 = (np.cos(om)*np.cos(w)-np.sin(om)*np.sin(w)*np.cos(inc))*x0 + (-np.cos(om)*np.sin(w)-np.sin(om)*np.cos(w)*np.cos(inc))*y0
        Y0 = (np.sin(om)*np.cos(w)+np.cos(om)*np.sin(w)*np.cos(inc))*x0 + (-np.sin(om)*np.sin(w)+np.cos(om)*np.cos(w)*np.cos(inc))*y0
        Z0 = (np.sin(w)*np.sin(inc))*x0 + (np.cos(w)*np.sin(inc))*y0
        Xs.append(X0)
        Ys.append(Y0)
        Zs.append(Z0)
        texts.append(row.get("full_name", "Objekt"))
    fig.add_trace(go.Scatter3d(x=Xs, y=Ys, z=Zs, mode="markers",
                               marker=dict(size=2, color="red", opacity=0.85),
                               text=texts, hoverinfo="text"))

def add_object_orbits(fig, df):
    for _, row in df.iterrows():
        a, e = row["a"], row["e"]
        inc, om, w = np.radians(row["i"]), np.radians(row["om"]), np.radians(row["w"])
        theta = np.linspace(0, 2*np.pi, 250)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
        x, y = r * np.cos(theta), r * np.sin(theta)
        X = (np.cos(om)*np.cos(w)-np.sin(om)*np.sin(w)*np.cos(inc))*x + (-np.cos(om)*np.sin(w)-np.sin(om)*np.cos(w)*np.cos(inc))*y
        Y = (np.sin(om)*np.cos(w)+np.cos(om)*np.sin(w)*np.cos(inc))*x + (-np.sin(om)*np.sin(w)+np.cos(om)*np.cos(w)*np.cos(inc))*y
        Z = (np.sin(w)*np.sin(inc))*x + (np.cos(w)*np.sin(inc))*y
        fig.add_trace(go.Scatter3d(
            x=X, y=Y, z=Z,
            mode="lines",
            line=dict(width=1),
            opacity=1,
            name=row.get("full_name", "Orbit"),   # ← Name fürs Objekt
            text=row.get("full_name", "Orbit"),   # ← Hover-Text
            hoverinfo="text",
            showlegend=False
        ))

