#!/bin/bash
# ===========================================
# Installation et lancement Docker - Linux/macOS
# ===========================================

set -e

echo ""
echo "============================================="
echo "  Agent IA Mathematique - Docker Setup"
echo "============================================="
echo ""

# Verifier Docker
if ! command -v docker &> /dev/null; then
    echo "ERREUR: Docker n'est pas installe!"
    echo ""
    echo "Installation:"
    echo "  - Linux: https://docs.docker.com/engine/install/"
    echo "  - macOS: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

echo "[OK] Docker detecte: $(docker --version)"

# Verifier Docker Compose
if ! docker compose version &> /dev/null; then
    echo "ERREUR: Docker Compose n'est pas disponible!"
    exit 1
fi

echo "[OK] Docker Compose detecte"
echo ""

# Verifier .env
if [ ! -f ".env" ]; then
    echo "[!] Fichier .env manquant - creation depuis l'exemple..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Editez le fichier .env avec vos cles API:"
    echo "  nano .env"
    echo ""
fi

# Menu
show_menu() {
    echo ""
    echo "Que voulez-vous faire?"
    echo ""
    echo "  1. Lancer l'agent (mode CLI - recommande pour Docker)"
    echo "  2. Lancer l'agent (mode GUI - necessite X11)"
    echo "  3. Arreter tous les services"
    echo "  4. Voir les logs"
    echo "  5. Reconstruire les images"
    echo "  6. Telecharger les modeles Ollama"
    echo "  7. Status des services"
    echo "  8. Quitter"
    echo ""
}

while true; do
    show_menu
    read -p "Votre choix (1-8): " choice
    
    case $choice in
        1)
            echo ""
            echo "Demarrage en mode CLI..."
            docker compose -f docker-compose.cli.yml up -d ollama
            echo "Attente du demarrage d'Ollama (30s)..."
            sleep 30
            docker compose -f docker-compose.cli.yml run --rm math-agent-cli
            ;;
        2)
            echo ""
            echo "Demarrage en mode GUI..."
            echo "Note: Necesssite X11 forwarding sur Linux"
            xhost +local:docker 2>/dev/null || true
            export DISPLAY=${DISPLAY:-:0}
            docker compose up -d
            echo ""
            echo "Services demarres!"
            ;;
        3)
            echo ""
            echo "Arret de tous les services..."
            docker compose down
            docker compose -f docker-compose.cli.yml down
            echo "Services arretes."
            ;;
        4)
            echo ""
            echo "Affichage des logs (Ctrl+C pour quitter)..."
            docker compose logs -f
            ;;
        5)
            echo ""
            echo "Reconstruction des images..."
            docker compose build --no-cache
            docker compose -f docker-compose.cli.yml build --no-cache
            echo "Images reconstruites."
            ;;
        6)
            echo ""
            echo "Telechargement des modeles Ollama..."
            docker compose up -d ollama
            sleep 10
            docker compose run --rm ollama-init
            echo "Modeles telecharges."
            ;;
        7)
            echo ""
            docker compose ps
            docker compose -f docker-compose.cli.yml ps
            ;;
        8)
            echo ""
            echo "Au revoir!"
            exit 0
            ;;
        *)
            echo "Choix invalide"
            ;;
    esac
done
