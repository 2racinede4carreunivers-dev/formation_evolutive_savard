#!/bin/bash
# Installation script for Linux/macOS

echo "============================================="
echo "  Installation - Agent IA Mathematique"
echo "============================================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python3 n'est pas installe"
    echo "Installez Python avec votre gestionnaire de paquets"
    exit 1
fi

echo "[1/5] Python detecte"
python3 --version

# Create virtual environment
echo
echo "[2/5] Creation de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate environment
echo
echo "[3/5] Activation de l'environnement..."
source venv/bin/activate

# Install dependencies
echo
echo "[4/5] Installation des dependances..."
pip install --upgrade pip
pip install -r requirements.txt

# Check .env file
echo
echo "[5/5] Verification de la configuration..."
if [ ! -f ".env" ]; then
    echo
    echo "ATTENTION: Le fichier .env n'existe pas!"
    echo "Copie du fichier exemple..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Editez le fichier .env avec vos cles API"
fi

echo
echo "============================================="
echo "  Installation terminee!"
echo "============================================="
echo
echo "Prochaines etapes:"
echo "1. Editez le fichier .env avec vos cles API"
echo "2. Lancez l'application avec: ./run.sh"
