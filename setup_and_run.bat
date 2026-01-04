@echo off

REM Virtuelle Umgebung erstellen
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
)

REM Aktivieren
call venv\Scripts\activate

REM Abhängigkeiten installieren
echo Installiere Abhängigkeiten...
pip install -r requirements.txt

REM Starten
echo Starte Solar System Visualizer...
streamlit run app.py