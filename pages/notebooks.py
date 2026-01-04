import streamlit as st
import nbformat

st.set_page_config(page_title="Notebook Viewer", layout="wide")
st.title("📓 Notebook Viewer")

# Notebook-Datei auswählen
notebook_file = st.selectbox(
    "Wähle ein Notebook aus:",
    ["clustering/kometVsAsteroid.ipynb", "clustering/asteroidFamilies.ipynb"],
)

# Notebook laden und anzeigen
try:
    with open(notebook_file, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    st.markdown("### Notebook-Inhalt")
    for i, cell in enumerate(notebook.cells):
        if cell.cell_type == "markdown":
            st.markdown(cell.source)
        elif cell.cell_type == "code":
            st.code(cell.source, language="python")
            if st.button(f"Ausführen: Zelle {i+1}"):
                try:
                    exec(cell.source, globals())
                    st.success("Code erfolgreich ausgeführt!")
                except Exception as e:
                    st.error(f"Fehler beim Ausführen: {str(e)}")
except FileNotFoundError:
    st.error(f"Die Datei {notebook_file} wurde nicht gefunden.")
