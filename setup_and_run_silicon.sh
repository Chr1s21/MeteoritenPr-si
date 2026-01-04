#!/bin/bash

# ---------------------------------------------------------
# 1. Architektur prüfen (Apple Silicon Check)
# ---------------------------------------------------------
ARCH=$(uname -m)
if [ "$ARCH" == "arm64" ]; then
    echo "🔍 Detektiert: Apple Silicon (ARM64)"
    echo "⚠️ Hinweis: Einige Abhängigkeiten könnten Rosetta 2 benötigen."

    # Prüfen, ob das Skript bereits im x86_64-Modus läuft
    if [ -z "$ROSETTA" ]; then
        echo "🔄 Starte das Skript im Rosetta-Modus (x86_64)..."
        export ROSETTA=1
        arch -x86_64 /bin/bash "$0"
        exit 0
    fi
else
    echo "🔍 Detektiert: $ARCH"
fi

# ---------------------------------------------------------
# 2. Virtual Environment aktivieren (WICHTIG: Vor dem Download!)
# ---------------------------------------------------------
# Wir aktivieren es hier schon, damit wir Python-Tools zum Downloaden nutzen können
if [ ! -d "venv" ]; then
    echo "⚠️ venv nicht gefunden! Erstelle neues venv..."
    python3 -m venv venv
fi

source venv/bin/activate

# ---------------------------------------------------------
# 3. Datei herunterladen (Mit gdown statt curl)
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
# 4. Abhängigkeiten installieren
# ---------------------------------------------------------
echo "📦 Installiere Abhängigkeiten..."

# Upgrade pip, um Installationsfehler zu vermeiden
pip install --upgrade pip

# PyArrow als Binary erzwingen (dein Fix für den Kompilier-Fehler)
pip install --only-binary=:all: pyarrow

# Restliche Requirements
pip install -r requirements.txt

# ---------------------------------------------------------
# 5. Streamlit starten
# ---------------------------------------------------------
echo "🚀 Starte Solar System Visualizer..."
streamlit run app.py