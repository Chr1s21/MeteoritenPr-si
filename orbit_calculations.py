import numpy as np
import plotly.graph_objects as go


def compute_object_positions(fig, df, cluster_column=None):
    """
    Fügt die aktuellen Positionen der Objekte als Punkte in die Figur ein.

    - fig: Plotly-Figure
    - df: DataFrame mit Bahnelementen (a, e, i, om, w, M, ...)
    - cluster_column: Name der Spalte mit Cluster-Labels (z.B. "cluster" oder "dbscan_cluster").
                      Wenn None oder Spalte nicht vorhanden -> alle Punkte gleiche Farbe.
    """

    # Basis-Farbpalette für Cluster
    base_colors = [
        "red", "deepskyblue", "lime", "yellow", "magenta",
        "orange", "cyan", "white", "purple", "pink",
        "brown", "gold"
    ]

    color_map = None
    if cluster_column is not None and cluster_column in df.columns:
        clusters = df[cluster_column].dropna().unique()

        color_map = {}

        # Noise-Cluster (z.B. -1 bei DBSCAN) grau einfärben
        noise_labels = [c for c in clusters if c in (-1, "-1")]
        for n in noise_labels:
            color_map[n] = "gray"

        # Restliche Cluster sortiert durchgehen und Farben zuweisen
        ordered_clusters = [c for c in sorted(clusters, key=str) if c not in noise_labels]
        for i, cl in enumerate(ordered_clusters):
            color_map[cl] = base_colors[i % len(base_colors)]

    Xs, Ys, Zs, texts, colors = [], [], [], [], []

    for _, row in df.iterrows():
        a, e = row["a"], row["e"]
        inc, om, w, M = (
            np.radians(row["i"]),
            np.radians(row["om"]),
            np.radians(row["w"]),
            np.radians(row["M"]),
        )

        # aktuelle Entfernung r und Position im Bahnebene-System
        r_now = (a * (1 - e**2)) / (1 + e * np.cos(M))
        x0, y0 = r_now * np.cos(M), r_now * np.sin(M)

        # Rotationsmatrix ins ekliptische Koordinatensystem
        X0 = (
            (np.cos(om) * np.cos(w) - np.sin(om) * np.sin(w) * np.cos(inc)) * x0
            + (-np.cos(om) * np.sin(w) - np.sin(om) * np.cos(w) * np.cos(inc)) * y0
        )
        Y0 = (
            (np.sin(om) * np.cos(w) + np.cos(om) * np.sin(w) * np.cos(inc)) * x0
            + (-np.sin(om) * np.sin(w) + np.cos(om) * np.cos(w) * np.cos(inc)) * y0
        )
        Z0 = (np.sin(w) * np.sin(inc)) * x0 + (np.cos(w) * np.sin(inc)) * y0

        Xs.append(X0)
        Ys.append(Y0)
        Zs.append(Z0)
        texts.append(row.get("full_name", "Objekt"))

        # Farbe bestimmen (Cluster-basiert oder Standard)
        if color_map is not None and cluster_column in df.columns:
            cl_val = row.get(cluster_column)
            colors.append(color_map.get(cl_val, "red"))
        else:
            colors.append("red")

    fig.add_trace(
        go.Scatter3d(
            x=Xs,
            y=Ys,
            z=Zs,
            mode="markers",
            marker=dict(size=2, color=colors, opacity=0.85),
            text=texts,
            hoverinfo="text",
        )
    )


def add_object_orbits(fig, df, cluster_column=None):
    """
    Fügt die Bahnkurven der Objekte als Linien in die Figur ein.

    - fig: Plotly-Figure
    - df: DataFrame mit Bahnelementen (a, e, i, om, w, ...)
    - cluster_column: Name der Spalte mit Cluster-Labels (z.B. "cluster" oder "dbscan_cluster").
                      Wenn None oder Spalte nicht vorhanden -> alle Orbits gleiche Farbe.
    """

    base_colors = [
        "red", "deepskyblue", "lime", "yellow", "magenta",
        "orange", "cyan", "white", "purple", "pink",
        "brown", "gold"
    ]

    color_map = None
    if cluster_column is not None and cluster_column in df.columns:
        clusters = df[cluster_column].dropna().unique()

        color_map = {}

        # Noise-Cluster (z.B. -1 bei DBSCAN) grau einfärben
        noise_labels = [c for c in clusters if c in (-1, "-1")]
        for n in noise_labels:
            color_map[n] = "gray"

        # Restliche Cluster sortiert durchgehen und Farben zuweisen
        ordered_clusters = [c for c in sorted(clusters, key=str) if c not in noise_labels]
        for i, cl in enumerate(ordered_clusters):
            color_map[cl] = base_colors[i % len(base_colors)]

    for _, row in df.iterrows():
        a, e = row["a"], row["e"]
        inc, om, w = (
            np.radians(row["i"]),
            np.radians(row["om"]),
            np.radians(row["w"]),
        )

        # Punkte entlang der Bahn
        theta = np.linspace(0, 2 * np.pi, 250)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
        x, y = r * np.cos(theta), r * np.sin(theta)

        X = (
            (np.cos(om) * np.cos(w) - np.sin(om) * np.sin(w) * np.cos(inc)) * x
            + (-np.cos(om) * np.sin(w) - np.sin(om) * np.cos(w) * np.cos(inc)) * y
        )
        Y = (
            (np.sin(om) * np.cos(w) + np.cos(om) * np.sin(w) * np.cos(inc)) * x
            + (-np.sin(om) * np.sin(w) + np.cos(om) * np.cos(w) * np.cos(inc)) * y
        )
        Z = (np.sin(w) * np.sin(inc)) * x + (np.cos(w) * np.sin(inc)) * y

        # Farbe bestimmen (Cluster-basiert oder Standard)
        if color_map is not None and cluster_column in df.columns:
            cl_val = row.get(cluster_column)
            line_color = color_map.get(cl_val, "red")
        else:
            line_color = "red"

        fig.add_trace(
            go.Scatter3d(
                x=X,
                y=Y,
                z=Z,
                mode="lines",
                line=dict(width=1, color=line_color),
                opacity=1,
                name=row.get("full_name", "Orbit"),  # Name fürs Objekt
                text=row.get("full_name", "Orbit"),  # Hover-Text
                hoverinfo="text",
                showlegend=False,
            )
        )
