@echo off
echo === Lancement de ton agent IA local ===

REM Vérification de Docker Desktop
echo Vérification de Docker Desktop...
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Docker Desktop n'est pas lancé. Lancement...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Attente du démarrage de Docker...
    timeout /t 10 >nul
)

REM Aller dans le dossier de l agent
cd /d "C:\agent-local-ia-carre\local_ai_agent"

REM Lancer les services
echo Démarrage des services Docker...
docker compose -f docker-compose.cli.yml up -d

REM Lancer l agent en mode CLI
echo Lancement de l agent IA...
docker compose -f docker-compose.cli.yml run --rm math-agent-cli
