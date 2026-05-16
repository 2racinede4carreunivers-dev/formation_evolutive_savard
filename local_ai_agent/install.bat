@echo off
echo =============================================
echo   Installation - Agent IA Mathematique
echo =============================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Telechargez Python depuis: https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

echo [1/5] Python detecte
python --version

REM Creer l'environnement virtuel
echo.
echo [2/5] Creation de l'environnement virtuel...
if not exist "venv" (
    python -m venv venv
)

REM Activer l'environnement
echo.
echo [3/5] Activation de l'environnement...
call venv\Scripts\activate.bat

REM Installer les dependances
echo.
echo [4/5] Installation des dependances (cela peut prendre quelques minutes)...
pip install --upgrade pip
pip install -r requirements.txt

REM Verifier le fichier .env
echo.
echo [5/5] Verification de la configuration...
if not exist ".env" (
    echo.
    echo ATTENTION: Le fichier .env n'existe pas!
    echo Copie du fichier exemple...
    copy .env.example .env
    echo.
    echo IMPORTANT: Editez le fichier .env avec vos cles API avant de lancer l'application
    echo Ouvrez .env avec Notepad et remplissez les valeurs
)

echo.
echo =============================================
echo   Installation terminee!
echo =============================================
echo.
echo Prochaines etapes:
echo 1. Editez le fichier .env avec vos cles API
echo 2. Lancez l'application avec: run.bat
echo.
pause
