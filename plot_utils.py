import plotly.graph_objects as go

def setup_plot():
    fig = go.Figure()
    fig.update_layout(
        title="3D Solar System – Alle Objekte",
        scene=dict(
            aspectmode="data",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False)
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        hoverlabel=dict(bgcolor="rgba(0,0,0,0.9)", font_size=14, font_color="white"),
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white"),
        # Kamera senkrecht von oben auf die XY-Ebene
        scene_camera=dict(eye=dict(x=0, y=0, z=1))
    )
    return fig
