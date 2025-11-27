import numpy as np
import plotly.graph_objects as go


def compute_object_positions(fig, df, cluster_column=None):
    """
    Fügt die aktuellen Positionen der Objekte als Punkte in die Figur ein.
    Erzeugt die Cluster-Legende, falls Cluster vorhanden sind.
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
            
    # --- Füge Punkte pro Cluster hinzu (inkl. Legende) ---
    if color_map is not None and cluster_column in df.columns:
        
        # Iteriere über die Cluster-Map, um separate Traces zu erstellen
        for cl_val, color in color_map.items():
            subset = df[df[cluster_column] == cl_val]
            if subset.empty:
                continue
            
            Xs, Ys, Zs, texts = [], [], [], []
            
            # Berechne die Positionen für das aktuelle Subset
            for _, row in subset.iterrows():
                a, e = row["a"], row["e"]
                inc, om, w, M = (
                    np.radians(row["i"]),
                    np.radians(row["om"]),
                    np.radians(row["w"]),
                    np.radians(row["M"]),
                )
                
                # Berechnung der Position (Kepler-Näherung)
                r_now = (a * (1 - e**2)) / (1 + e * np.cos(M))
                x0, y0 = r_now * np.cos(M), r_now * np.sin(M)
                
                # Rotation ins ekliptische Koordinatensystem
                X0 = (
                    (np.cos(om) * np.cos(w) - np.sin(om) * np.sin(w) * np.cos(inc)) * x0
                    + (-np.cos(om) * np.sin(w) - np.sin(om) * np.cos(w) * np.cos(inc)) * y0
                )
                Y0 = (
                    (np.sin(om) * np.cos(w) + np.cos(om) * np.sin(w) * np.cos(inc)) * x0
                    + (-np.sin(om) * np.sin(w) + np.cos(om) * np.cos(w) * np.cos(inc)) * y0
                )
                Z0 = (np.sin(w) * np.sin(inc)) * x0 + (np.cos(w) * np.cos(inc)) * y0

                Xs.append(X0)
                Ys.append(Y0)
                Zs.append(Z0)
                texts.append(row.get("full_name", "Objekt"))

            # Legendenname und Sichtbarkeit
            legend_name = "Noise" if cl_val in (-1, "-1") else f"Cluster {cl_val}"
            show_leg = cl_val not in (-1, "-1")
            
            # Füge Punkte-Trace pro Cluster hinzu (mit Legende)
            fig.add_trace(
                go.Scatter3d(
                    x=Xs,
                    y=Ys,
                    z=Zs,
                    mode="markers",
                    marker=dict(size=2, color=color, opacity=0.85),
                    text=texts,
                    hoverinfo="text",
                    name=legend_name, # Name für die Legende
                    showlegend=show_leg, # Legende aktiv
                    legendgroup=legend_name, # Gruppieren, falls Bahnen aktiv sind
                )
            )
            
    else:
        # Fallback für ungeclusterte Daten (alle rot, keine Legende)
        Xs, Ys, Zs, texts = [], [], [], []

        for _, row in df.iterrows():
            a, e = row["a"], row["e"]
            inc, om, w, M = (
                np.radians(row["i"]),
                np.radians(row["om"]),
                np.radians(row["w"]),
                np.radians(row["M"]),
            )

            r_now = (a * (1 - e**2)) / (1 + e * np.cos(M))
            x0, y0 = r_now * np.cos(M), r_now * np.sin(M)
            
            X0 = (
                (np.cos(om) * np.cos(w) - np.sin(om) * np.sin(w) * np.cos(inc)) * x0
                + (-np.cos(om) * np.sin(w) - np.sin(om) * np.cos(w) * np.cos(inc)) * y0
            )
            Y0 = (
                (np.sin(om) * np.cos(w) + np.cos(om) * np.sin(w) * np.cos(inc)) * x0
                + (-np.sin(om) * np.sin(w) + np.cos(om) * np.cos(w) * np.cos(inc)) * y0
            )
            Z0 = (np.sin(w) * np.sin(inc)) * x0 + (np.cos(w) * np.cos(inc)) * y0

            Xs.append(X0)
            Ys.append(Y0)
            Zs.append(Z0)
            texts.append(row.get("full_name", "Objekt"))

        fig.add_trace(
            go.Scatter3d(
                x=Xs,
                y=Ys,
                z=Zs,
                mode="markers",
                marker=dict(size=2, color="red", opacity=0.85), # Standardfarbe
                text=texts,
                hoverinfo="text",
                name="Objekte",
                showlegend=False, # Keine Legende für ungeclusterte Daten
            )
        )


def add_object_orbits(fig, df, cluster_column=None):
    """
    Fügt die Bahnkurven der Objekte als Linien in die Figur ein.
    Die Bahnen werden nach Cluster eingefärbt und der Legende der Punkte zugeordnet.
    Sie erzeugen KEINE eigenen Legendeneinträge (showlegend=False).
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

        # --- Füge Bahnen pro Cluster hinzu (Farbe und Legenden-Zuordnung) ---
        for cl_val, color in color_map.items():
            subset = df[df[cluster_column] == cl_val]

            if subset.empty:
                continue

            X_all, Y_all, Z_all = [], [], []

            # Alle Bahnen dieses Clusters berechnen
            for _, row in subset.iterrows():
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

                # Rotationsmatrix
                X = (
                    (np.cos(om) * np.cos(w) - np.sin(om) * np.sin(w) * np.cos(inc)) * x
                    + (-np.cos(om) * np.sin(w) - np.sin(om) * np.cos(w) * np.cos(inc)) * y
                )
                Y = (
                    (np.sin(om) * np.cos(w) + np.cos(om) * np.sin(w) * np.cos(inc)) * x
                    + (-np.sin(om) * np.sin(w) + np.cos(om) * np.cos(w) * np.cos(inc)) * y
                )
                Z = (np.sin(w) * np.sin(inc)) * x + (np.cos(w) * np.cos(inc)) * y 

                X_all.extend(X.tolist() + [None])
                Y_all.extend(Y.tolist() + [None])
                Z_all.extend(Z.tolist() + [None])

            # Legendenname für die Zuordnung
            legend_name = "Noise" if cl_val in (-1, "-1") else f"Cluster {cl_val}"

            fig.add_trace(
                go.Scatter3d(
                    x=X_all,
                    y=Y_all,
                    z=Z_all,
                    mode="lines",
                    line=dict(width=1, color=color),
                    opacity=1,
                    name=legend_name, # Name für die korrekte Zuordnung
                    hoverinfo="skip",
                    showlegend=False, # Wichtig: KEINE Legende hier! Die Punkte machen das
                    # Verwende legendgroup, um diesen Trace der Legende des Punkt-Traces zuzuordnen
                    legendgroup=legend_name,
                )
            )

    else:
        # Fallback für ungeclusterte Daten: Jede Bahn einzeln, keine Legende
        for _, row in df.iterrows():
            a, e = row["a"], row["e"]
            inc, om, w = (
                np.radians(row["i"]),
                np.radians(row["om"]),
                np.radians(row["w"]),
            )

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
            Z = (np.sin(w) * np.sin(inc)) * x + (np.cos(w) * np.cos(inc)) * y

            line_color = "red"

            fig.add_trace(
                go.Scatter3d(
                    x=X,
                    y=Y,
                    z=Z,
                    mode="lines",
                    line=dict(width=1, color=line_color),
                    opacity=1,
                    name=row.get("full_name", "Orbit"),
                    text=row.get("full_name", "Orbit"),
                    hoverinfo="text",
                    showlegend=False, # KEINE Legende für ungeclusterte Bahnen
                )
            )