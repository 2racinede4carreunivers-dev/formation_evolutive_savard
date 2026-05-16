@echo off
echo Demarrage de l'Agent IA Mathematique...
echo.

REM Activer l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERREUR: Environnement virtuel non trouve.
    echo Executez d'abord install.bat
    pause
    exit /b 1
)

REM Verifier le fichier .env
if not exist ".env" (
    echo ERREUR: Fichier .env manquant.
    echo Copiez .env.example vers .env et configurez vos cles API.
    pause
    exit /b 1
)

REM Lancer l'application
python main.py

pause
