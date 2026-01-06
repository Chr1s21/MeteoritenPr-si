@echo off
setlocal

REM Datei-ID definieren
set "FILEID=10Pm21pJpeCZxCkcwVyEgUJmRlsD5t66k"
set "FILENAME=csv\raw_data.csv"

REM 1. Ordner erstellen, falls nicht vorhanden
if not exist "csv" (
    mkdir csv
)

REM 2. Virtuelle Umgebung erstellen (falls nicht vorhanden)
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
)

REM 3. Aktivieren der Umgebung (WICHTIG: Bevor wir pip nutzen)
call venv\Scripts\activate

REM 4. Prüfen, ob raw_data.csv existiert
if not exist "%FILENAME%" (
    echo Datei fehlt. Installiere Download-Tool...
    
    REM gdown installieren (löst das Google Drive Problem)
    pip install gdown
    
    echo Starte Download von Google Drive...
    REM -O steht für Output, unter Windows Backslashes beachten
    gdown %FILEID% -O %FILENAME%
) else (
    echo raw_data.csv ist bereits vorhanden.
)

REM 5. Abhängigkeiten installieren
echo Installiere Abhängigkeiten...

REM Upgrade pip zur Sicherheit
python -m pip install --upgrade pip

REM Restliche Pakete
pip install -r requirements.txt

REM Optional: Zusätzliche Pakete installieren
.\venv\Scripts\python.exe -m pip install nbconvert
.\venv\Scripts\python.exe -m pip install ipykernel
.\venv\Scripts\python.exe -m ipykernel install --user --name python3 --display-name "Python 3 (venv)"

REM 6. Streamlit starten
echo Starte Solar System Visualizer...
streamlit run app.py

pause