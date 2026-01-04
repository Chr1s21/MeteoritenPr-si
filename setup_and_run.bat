@echo off

REM 1. Ordner erstellen, falls nicht vorhanden
if not exist "csv" (
    mkdir csv
)

REM 2. Prüfen, ob raw_data.csv existiert
if not exist "csv\raw_data.csv" (
    echo Lade raw_data.csv herunter...
    curl -L -o csv/raw_data.csv "https://drive.usercontent.google.com/download?id=10Pm21pJpeCZxCkcwVyEgUJmRlsD5t66k&export=download&authuser=0"
    echo raw_data.csv wurde heruntergeladen.
) else (
    echo raw_data.csv ist bereits vorhanden.
)

REM 3. Virtuelle Umgebung erstellen (falls nicht vorhanden)
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
)

REM 4. Aktivieren
call venv\Scripts\activate

REM 5. Abhängigkeiten installieren
echo Installiere Abhängigkeiten...
pip install -r requirements.txt

REM 6. Streamlit starten
echo Starte Solar System Visualizer...
streamlit run app.py