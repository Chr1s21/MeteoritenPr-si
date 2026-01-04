#!/bin/bash

# ---------------------------------------------------------
# 1. Virtual Environment aktivieren (WICHTIG: Vor dem Download!)
# ---------------------------------------------------------
# Wir aktivieren es hier schon, damit wir Python-Tools zum Downloaden nutzen können
if [ ! -d "venv" ]; then
    echo "⚠️ venv nicht gefunden! Erstelle neues venv..."
    python3 -m venv venv
fi

source venv/bin/activate

# ---------------------------------------------------------
# 2. Datei herunterladen (Mit gdown statt curl)
# ---------------------------------------------------------
FILEID="10Pm21pJpeCZxCkcwVyEgUJmRlsD5t66k"
FILENAME="csv/raw_data.csv"

# Ordner erstellen
mkdir -p csv

if [ ! -f "$FILENAME" ]; then
    echo "⬇️ Datei nicht gefunden. Starte Download..."
    
    # gdown installieren (kleines Tool, das Google Drive Links repariert)
    pip install -q gdown
    
    # Download mit automatischer Viren-Bestätigung
    gdown "${FILEID}" -O "${FILENAME}"
else
    echo "✅ Datei $FILENAME ist bereits vorhanden."
fi

# ---------------------------------------------------------
# 3. Abhängigkeiten installieren
# ---------------------------------------------------------
echo "📦 Installiere Abhängigkeiten..."

# Upgrade pip, um Installationsfehler zu vermeiden
pip install --upgrade pip

# Restliche Requirements
pip install -r requirements.txt

# ---------------------------------------------------------
# 5. Streamlit starten
# ---------------------------------------------------------
echo "🚀 Starte Solar System Visualizer..."
streamlit run app.py