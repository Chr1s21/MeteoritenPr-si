#!/bin/bash

# 1. Architektur prüfen
ARCH=$(uname -m)
if [ "$ARCH" == "arm64" ]; then
    echo "🔍 Detektiert: Apple Silicon (ARM64)"
    echo "⚠️ Hinweis: Einige Abhängigkeiten könnten Rosetta 2 benötigen."

    # Prüfen, ob das Skript bereits im x86_64-Modus läuft
    if [ -z "$ROSETTA" ]; then
        echo "🔄 Starte das Skript im Rosetta-Modus (x86_64)..."
        # Skript im x86_64-Modus neu starten
        arch -x86_64 /bin/bash "$0"
        exit 0
    fi
else
    echo "🔍 Detektiert: $ARCH"
fi

# 2. Ordner erstellen, falls nicht vorhanden
mkdir -p csv

# 3. Prüfen, ob raw_data.csv existiert
if [ ! -f "csv/raw_data.csv" ]; then
    echo "📥 Lade raw_data.csv herunter..."
    curl -L -o csv/raw_data.csv "https://drive.usercontent.google.com/download?id=10Pm21pJpeCZxCkcwVyEgUJmRlsD5t66k&export=download&authuser=0"
    echo "✅ raw_data.csv wurde heruntergeladen."
else
    echo "✅ raw_data.csv ist bereits vorhanden."
fi

# 4. Virtuelle Umgebung erstellen (falls nicht vorhanden)
if [ ! -d "venv" ]; then
    echo "🔧 Erstelle virtuelle Umgebung..."
    python3 -m venv venv
fi

# 5. Aktivieren
source venv/bin/activate

# 6. Abhängigkeiten installieren
echo "📦 Installiere Abhängigkeiten..."
pip install --only-binary=:all: pyarrow
pip install -r requirements.txt

# 7. Streamlit starten
echo "🚀 Starte Solar System Visualizer..."
streamlit run app.py