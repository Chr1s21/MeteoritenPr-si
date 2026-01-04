#!/bin/bash

# 1. Virtuelle Umgebung erstellen (falls nicht vorhanden)
if [ ! -d "venv" ]; then
    echo "🔧 Erstelle virtuelle Umgebung..."
    python3 -m venv venv
fi

# 2. Aktivieren
source venv/bin/activate

# 3. Abhängigkeiten installieren
echo "📦 Installiere Abhängigkeiten..."
pip install -r requirements.txt

# 4. Streamlit starten
echo "🚀 Starte Solar System Visualizer..."
streamlit run app.py