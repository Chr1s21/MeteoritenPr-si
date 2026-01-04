# 🌌 Solar System Visualizer

Interaktive 3D-Visualisierung von Asteroiden- und Kometenbahnen mit Clustering-Analyse.

## 🚀 Schnellstart

### macOS/Linux
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Windows
```
setup_and_run.bat
```

### Manuell
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Features

1. **3D Solar System Viewer** - Interaktive Planetenbahnen und Objekte
2. **Clustering-Analyse** - Komet vs. Asteroid Unterscheidung
3. **Asteroidenfamilien** - DBSCAN-basierte Familiensuche

## 🔬 Wissenschaftlicher Hintergrund

- **Tisserand-Parameter**: Unterscheidung Komet/Asteroid bei $T_J = 3$
- **DBSCAN**: Dichtebasiertes Clustering für Asteroidenfamilien
- **K-Means**: Schnelles Clustering für binäre Klassifikation

---
*Projekt für Datenanalyse in Unternehmen, SEM6*