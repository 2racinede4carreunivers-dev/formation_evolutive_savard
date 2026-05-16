# Guide d'Installation Docker - Agent IA Mathematique

Ce guide explique comment installer et executer l'Agent IA Mathematique avec Docker.

## Avantages de Docker

- **Isolation**: L'agent tourne dans un environnement isole
- **Portabilite**: Fonctionne sur Windows, macOS, Linux
- **Simplicite**: Pas besoin d'installer Python, dependances, etc.
- **Ollama inclus**: Le LLM local est automatiquement configure
- **Mise a jour facile**: `docker compose pull && docker compose up -d`

## Prerequis

### 1. Installer Docker Desktop

| Systeme | Lien |
|---------|------|
| **Windows** | https://www.docker.com/products/docker-desktop/ |
| **macOS** | https://www.docker.com/products/docker-desktop/ |
| **Linux** | https://docs.docker.com/engine/install/ |

### 2. Configuration Systeme Recommandee

- **RAM**: 16 GB minimum (8 GB pour Ollama + 4 GB pour l'agent)
- **Stockage**: 20 GB libres (pour les modeles Ollama)
- **GPU** (optionnel): NVIDIA avec drivers CUDA pour acceleration

## Installation Rapide

### Windows

```batch
# 1. Clonez le repository
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO/local_ai_agent

# 2. Configurez vos cles API
copy .env.example .env
notepad .env

# 3. Lancez
docker-start.bat
```

### Linux / macOS

```bash
# 1. Clonez le repository
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO/local_ai_agent

# 2. Configurez vos cles API
cp .env.example .env
nano .env

# 3. Rendez le script executable
chmod +x docker-start.sh

# 4. Lancez
./docker-start.sh
```

## Modes de Fonctionnement

### Mode CLI (Recommande pour Docker)

Le mode CLI est plus leger et ne necessite pas d'affichage graphique.

```bash
# Lancer en mode CLI
docker compose -f docker-compose.cli.yml up -d

# Interagir avec l'agent
docker compose -f docker-compose.cli.yml run --rm math-agent-cli
```

### Mode GUI (Interface Graphique)

Necessite X11 sur Linux ou XQuartz sur macOS.

```bash
# Linux uniquement - autoriser X11
xhost +local:docker

# Lancer
docker compose up -d
```

## Configuration

### Fichier .env

```env
# Obligatoire pour les taches complexes
OPENAI_API_KEY=sk-proj-xxx

# Optionnel - calculs avances
WOLFRAM_APP_ID=xxx

# Optionnel - emails
EMAIL_ADDRESS=vous@gmail.com
EMAIL_APP_PASSWORD=xxx

# Optionnel - GitHub
GITHUB_TOKEN=ghp_xxx
```

### GPU NVIDIA (Optionnel)

Pour activer l'acceleration GPU, editez `docker-compose.yml`:

```yaml
ollama:
  # Decommenter ces lignes:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

Prerequis: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## Commandes Utiles

### Gestion des Services

```bash
# Demarrer tous les services
docker compose up -d

# Arreter tous les services
docker compose down

# Voir les logs
docker compose logs -f

# Voir le status
docker compose ps

# Redemarrer un service
docker compose restart math-agent
```

### Gestion des Modeles Ollama

```bash
# Telecharger un modele supplementaire
docker compose exec ollama ollama pull mistral

# Lister les modeles installes
docker compose exec ollama ollama list

# Supprimer un modele
docker compose exec ollama ollama rm mistral
```

### Maintenance

```bash
# Mettre a jour les images
docker compose pull
docker compose up -d

# Reconstruire l'image de l'agent (apres modification du code)
docker compose build --no-cache math-agent

# Nettoyer les ressources inutilisees
docker system prune -f
```

### Sauvegarde des Donnees

```bash
# Les donnees sont dans des volumes Docker
docker volume ls | grep math-agent

# Sauvegarder les donnees
docker run --rm -v math-agent-data:/data -v $(pwd):/backup alpine tar cvf /backup/agent-data.tar /data

# Restaurer
docker run --rm -v math-agent-data:/data -v $(pwd):/backup alpine tar xvf /backup/agent-data.tar -C /
```

## Depannage

### Ollama ne demarre pas

```bash
# Verifier les logs
docker compose logs ollama

# Redemarrer Ollama
docker compose restart ollama

# Verifier la memoire disponible
docker stats
```

### Erreur "Out of Memory"

Augmentez la memoire allouee a Docker:
- **Docker Desktop** > Settings > Resources > Memory > 16 GB

### Les modeles ne se telechargent pas

```bash
# Telecharger manuellement
docker compose exec ollama ollama pull llama3.2

# Verifier l'espace disque
docker system df
```

### Interface graphique ne s'affiche pas (Linux)

```bash
# Autoriser les connexions X11
xhost +local:docker

# Verifier DISPLAY
echo $DISPLAY  # Doit afficher :0 ou similaire
```

## Architecture Docker

```
┌─────────────────────────────────────────────┐
│              Docker Network                  │
│                                             │
│  ┌─────────────┐      ┌─────────────────┐  │
│  │ math-agent  │──────│     ollama      │  │
│  │  (Python)   │      │ (LLM local)     │  │
│  └─────────────┘      └─────────────────┘  │
│         │                     │             │
│         ▼                     ▼             │
│  ┌─────────────┐      ┌─────────────────┐  │
│  │ agent-data  │      │  ollama-data    │  │
│  │  (Volume)   │      │   (Volume)      │  │
│  └─────────────┘      └─────────────────┘  │
└─────────────────────────────────────────────┘
```

## Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Ollama](https://ollama.com/docs)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)

---

*Pour toute question, consultez les logs avec `docker compose logs -f`*
