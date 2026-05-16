# ================================
# Script : lancer-agent-ia.ps1
# Auteur : Philippe Thomas Savard
# Objectif : Lancer l'agent IA local via Docker
# ================================

Write-Host "=== Démarrage du setup Docker pour l'agent IA ===" -ForegroundColor Cyan

# 1. Vérifier que Docker Desktop est lancé
Write-Host "Vérification de Docker Desktop..."
$dockerProcess = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue

if (-not $dockerProcess) {
    Write-Host "Docker Desktop n'est pas lancé. Démarrage..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

    Write-Host "Attente du démarrage de Docker Desktop..." -ForegroundColor Yellow
    Start-Sleep -Seconds 12
} else {
    Write-Host "Docker Desktop est déjà lancé." -ForegroundColor Green
}

# 2. Aller dans le dossier de ton agent
Set-Location "C:\agent-local-ia-carre\local_ai_agent"
Write-Host "Dossier de l'agent chargé." -ForegroundColor Green

# 3. Arrêter les conteneurs existants
Write-Host "Arrêt des conteneurs existants..." -ForegroundColor Yellow
docker compose down 2>$null

# 4. Reconstruire l'environnement
Write-Host "Reconstruction de l'environnement Docker..." -ForegroundColor Yellow
docker compose build 2>$null

# 5. Lancer l'agent IA
Write-Host "Lancement de l'agent IA..." -ForegroundColor Yellow
docker compose up -d 2>$null

# 6. Connexion automatique au conteneur
Write-Host "Connexion au conteneur..." -ForegroundColor Cyan
$containerName = "math-agent-cli"

# Vérifier que le conteneur est bien démarré
$running = docker ps --format "{{.Names}}" | Select-String $containerName

if ($running) {
    Write-Host "Connexion au conteneur $containerName..." -ForegroundColor Green
    docker exec -it $containerName bash
} else {
    Write-Host "ERREUR : Le conteneur $containerName n'est pas en cours d'exécution." -ForegroundColor Red
    Write-Host "Utilise 'docker ps -a' pour vérifier l'état des conteneurs." -ForegroundColor Yellow
}
