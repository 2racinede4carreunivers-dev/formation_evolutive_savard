#!/bin/bash
# Run script for Linux/macOS

echo "Demarrage de l'Agent IA Mathematique..."
echo

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERREUR: Environnement virtuel non trouve."
    echo "Executez d'abord: ./install.sh"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "ERREUR: Fichier .env manquant."
    echo "Copiez .env.example vers .env et configurez vos cles API."
    exit 1
fi

# Run application
python main.py
