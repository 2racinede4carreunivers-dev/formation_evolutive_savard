@echo off
REM ===========================================
REM Installation et lancement Docker - Windows
REM ===========================================

echo.
echo =============================================
echo   Agent IA Mathematique - Docker Setup
echo =============================================
echo.

REM Verifier Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Docker n'est pas installe!
    echo.
    echo Telechargez Docker Desktop depuis:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

echo [OK] Docker detecte
docker --version
echo.

REM Verifier Docker Compose
docker compose version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Docker Compose n'est pas disponible!
    pause
    exit /b 1
)

echo [OK] Docker Compose detecte
echo.

REM Verifier le fichier .env
if not exist ".env" (
    echo [!] Fichier .env manquant - creation depuis l'exemple...
    copy .env.example .env
    echo.
    echo IMPORTANT: Editez le fichier .env avec vos cles API avant de continuer!
    echo.
    notepad .env
    pause
)

REM Menu
echo.
echo Que voulez-vous faire?
echo.
echo   1. Lancer l'agent (mode GUI - interface graphique)
echo   2. Lancer l'agent (mode CLI - ligne de commande)
echo   3. Arreter tous les services
echo   4. Voir les logs
echo   5. Reconstruire les images
echo   6. Quitter
echo.

set /p choice="Votre choix (1-6): "

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto rebuild
if "%choice%"=="6" goto end

:gui
echo.
echo Demarrage en mode GUI...
echo (Ollama sera telecharge si necessaire - cela peut prendre quelques minutes)
echo.
docker compose up -d
echo.
echo Services demarres! L'interface devrait s'ouvrir.
echo Pour voir les logs: docker compose logs -f math-agent
pause
goto end

:cli
echo.
echo Demarrage en mode CLI...
echo.
docker compose -f docker-compose.cli.yml up -d ollama ollama-init
echo Attente du demarrage d'Ollama...
timeout /t 30 /nobreak
docker compose -f docker-compose.cli.yml run --rm math-agent-cli
goto end

:stop
echo.
echo Arret de tous les services...
docker compose down
docker compose -f docker-compose.cli.yml down
echo Services arretes.
pause
goto end

:logs
echo.
echo Affichage des logs (Ctrl+C pour quitter)...
docker compose logs -f
goto end

:rebuild
echo.
echo Reconstruction des images...
docker compose build --no-cache
echo Images reconstruites.
pause
goto end

:end
echo.
