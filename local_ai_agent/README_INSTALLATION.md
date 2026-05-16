# Guide d'Installation Complet - Agent IA Local Mathematique

## Table des Matieres
1. [Prerequis Systeme](#1-prerequis-systeme)
2. [Installation Python](#2-installation-python)
3. [Installation Ollama (LLM Local)](#3-installation-ollama-llm-local)
4. [Installation Isabelle/HOL](#4-installation-isabellehol)
5. [Configuration des Cles API](#5-configuration-des-cles-api)
6. [Installation des Dependances Python](#6-installation-des-dependances-python)
7. [Configuration de l'Agent](#7-configuration-de-lagent)
8. [Premier Demarrage](#8-premier-demarrage)
9. [Guide d'Utilisation](#9-guide-dutilisation)
10. [Depannage](#10-depannage)

---

## 1. Prerequis Systeme

### Configuration Minimale Requise
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 16 GB minimum (32 GB recommande pour les modeles locaux)
- **Stockage**: 50 GB d'espace libre (pour Ollama et les modeles)
- **Processeur**: Intel i5/AMD Ryzen 5 ou superieur
- **GPU** (optionnel mais recommande): NVIDIA avec 8GB+ VRAM pour acceleration

### Logiciels a Installer
| Logiciel | Version | Lien de Telechargement |
|----------|---------|------------------------|
| Python | 3.11+ | https://www.python.org/downloads/windows/ |
| Git | Latest | https://git-scm.com/download/win |
| Ollama | Latest | https://ollama.com/download/windows |
| Isabelle | 2024 | https://isabelle.in.tum.de/installation.html |
| Visual Studio Build Tools | 2022 | https://visualstudio.microsoft.com/visual-cpp-build-tools/ |

---

## 2. Installation Python

### Etape 2.1: Telecharger Python
1. Allez sur https://www.python.org/downloads/windows/
2. Cliquez sur "Download Python 3.11.x" (ou version superieure)
3. Telechargez l'installateur Windows (64-bit)

### Etape 2.2: Installer Python
1. Lancez l'installateur telecharge
2. **IMPORTANT**: Cochez "Add Python to PATH" en bas de la fenetre
3. Cliquez sur "Customize installation"
4. Cochez toutes les options
5. Cliquez "Next"
6. Cochez "Install for all users"
7. Cliquez "Install"

### Etape 2.3: Verifier l'installation
Ouvrez PowerShell ou CMD et tapez:
```powershell
python --version
pip --version
```
Vous devriez voir les versions affichees.

---

## 3. Installation Ollama (LLM Local)

### Etape 3.1: Telecharger Ollama
1. Allez sur https://ollama.com/download/windows
2. Cliquez sur "Download for Windows"
3. Telechargez OllamaSetup.exe

### Etape 3.2: Installer Ollama
1. Lancez OllamaSetup.exe
2. Suivez les instructions d'installation
3. Redemarrez votre ordinateur apres l'installation

### Etape 3.3: Telecharger les Modeles Recommandes
Ouvrez PowerShell et executez ces commandes une par une:

```powershell
# Modele principal pour conversations (7B parametres, ~4GB)
ollama pull llama3.2

# Modele pour le code et les mathematiques (7B, ~4GB)
ollama pull qwen2.5-coder:7b

# Modele plus puissant si vous avez 32GB+ RAM (70B, ~40GB)
# ollama pull llama3.1:70b

# Modele specialise mathematiques (optionnel)
ollama pull deepseek-coder:6.7b
```

### Etape 3.4: Verifier Ollama
```powershell
ollama list
ollama run llama3.2 "Bonjour, ca fonctionne?"
```

---

## 4. Installation Isabelle/HOL

### Etape 4.1: Telecharger Isabelle
1. Allez sur https://isabelle.in.tum.de/installation.html
2. Sous "Current stable release", cliquez sur "Isabelle2024" pour Windows
3. Telechargez le fichier .exe (~1.5 GB)

### Etape 4.2: Installer Isabelle
1. Lancez l'installateur Isabelle2024.exe
2. Choisissez le dossier d'installation (notez ce chemin!)
   - Recommande: `C:\Isabelle2024`
3. Completez l'installation

### Etape 4.3: Configurer le PATH Isabelle
1. Ouvrez le menu Demarrer, cherchez "Variables d'environnement"
2. Cliquez sur "Modifier les variables d'environnement systeme"
3. Cliquez sur "Variables d'environnement..."
4. Dans "Variables systeme", trouvez "Path" et cliquez "Modifier"
5. Cliquez "Nouveau" et ajoutez: `C:\Isabelle2024\bin`
6. Cliquez OK partout

### Etape 4.4: Verifier Isabelle
```powershell
isabelle version
```

---

## 5. Configuration des Cles API

### Etape 5.1: Cle OpenAI (Vous l'avez deja)
1. Allez sur https://platform.openai.com/api-keys
2. Copiez votre cle API existante
3. Elle ressemble a: `sk-proj-xxxxxxxxxxxxxxxxxxxx`

### Etape 5.2: Cle WolframAlpha (Gratuit)
1. Allez sur https://developer.wolframalpha.com/
2. Cliquez "Sign up" et creez un compte
3. Une fois connecte, cliquez "Get an AppID"
4. Selectionnez "Full Results API"
5. Donnez un nom a votre app (ex: "MathAgent")
6. Copiez l'AppID genere (ressemble a: `XXXXXX-XXXXXXXXXX`)

### Etape 5.3: Creer le Fichier de Configuration
1. Dans le dossier de l'agent, trouvez le fichier `.env.example`
2. Copiez-le et renommez la copie en `.env`
3. Ouvrez `.env` avec Notepad et remplissez:

```env
# OpenAI API (vous l'avez deja)
OPENAI_API_KEY=sk-proj-votre-cle-ici

# WolframAlpha API
WOLFRAM_APP_ID=votre-appid-ici

# Chemin Isabelle (ajustez si different)
ISABELLE_PATH=C:\Isabelle2024

# Configuration Email (optionnel - Gmail)
EMAIL_ADDRESS=votre.email@gmail.com
EMAIL_APP_PASSWORD=votre-mot-de-passe-application

# GitHub Token (optionnel)
GITHUB_TOKEN=ghp_votre_token_ici
```

### Etape 5.4: Configurer Gmail (Optionnel)
Pour permettre a l'agent d'envoyer des emails:
1. Allez sur https://myaccount.google.com/security
2. Activez "Verification en 2 etapes" si ce n'est pas fait
3. Allez sur https://myaccount.google.com/apppasswords
4. Selectionnez "Mail" et "Windows Computer"
5. Cliquez "Generer"
6. Copiez le mot de passe de 16 caracteres dans `.env`

### Etape 5.5: Configurer GitHub Token (Optionnel)
Pour permettre a l'agent de gerer vos depots:
1. Allez sur https://github.com/settings/tokens
2. Cliquez "Generate new token (classic)"
3. Donnez un nom (ex: "MathAgent")
4. Selectionnez les scopes: `repo`, `workflow`, `read:org`
5. Cliquez "Generate token"
6. Copiez le token dans `.env`

---

## 6. Installation des Dependances Python

### Etape 6.1: Ouvrir PowerShell en tant qu'Administrateur
1. Clic droit sur le menu Demarrer
2. Selectionnez "Windows PowerShell (Admin)"

### Etape 6.2: Naviguer vers le Dossier de l'Agent
```powershell
cd C:\chemin\vers\local_ai_agent
```

### Etape 6.3: Creer un Environnement Virtuel
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si vous obtenez une erreur de politique d'execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Etape 6.4: Installer les Dependances
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Etape 6.5: Installer PyAudio pour la Reconnaissance Vocale
PyAudio necessite une installation speciale sur Windows:
```powershell
pip install pipwin
pipwin install pyaudio
```

Si ca ne fonctionne pas, telechargez manuellement:
1. Allez sur https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Telechargez `PyAudio-0.2.14-cp311-cp311-win_amd64.whl` (pour Python 3.11)
3. Installez avec: `pip install chemin\vers\PyAudio-0.2.14-cp311-cp311-win_amd64.whl`

---

## 7. Configuration de l'Agent

### Etape 7.1: Configuration Generale
Ouvrez `config.yaml` et ajustez selon vos preferences:

```yaml
# Langue par defaut
language: "fr"

# Modele LLM par defaut (local)
default_model: "llama3.2"

# Utiliser OpenAI pour les taches complexes
use_openai_for_complex: true
openai_model: "gpt-4o"

# Dossiers a surveiller
watched_folders:
  - "C:\\Users\\VotreNom\\Documents"
  - "C:\\Users\\VotreNom\\Desktop"
  - "C:\\Users\\VotreNom\\GitHub"

# Calendrier par defaut
calendar_provider: "outlook"  # ou "google"
```

### Etape 7.2: Configurer les Permissions
L'agent demandera des permissions au premier demarrage pour:
- Acces au systeme de fichiers
- Acces au microphone
- Execution de commandes systeme
- Acces reseau

---

## 8. Premier Demarrage

### Etape 8.1: Activer l'Environnement Virtuel
```powershell
cd C:\chemin\vers\local_ai_agent
.\venv\Scripts\Activate.ps1
```

### Etape 8.2: Lancer l'Agent
```powershell
python main.py
```

### Etape 8.3: Premier Demarrage
Au premier lancement:
1. L'agent verifiera toutes les dependances
2. Il testera la connexion a Ollama
3. Il verifiera vos cles API
4. L'interface graphique s'ouvrira

### Etape 8.4: Test Initial
Dans l'interface, essayez ces commandes:
- "Bonjour, presente-toi"
- "Resous l'equation x^2 + 5x + 6 = 0"
- "Ouvre mon dossier Documents"
- "Cree une preuve simple en Isabelle"

---

## 9. Guide d'Utilisation

### 9.1 Commandes de Base
| Commande | Action |
|----------|--------|
| "Ouvre [dossier]" | Navigue vers un dossier |
| "Lis le fichier [nom]" | Lit et affiche le contenu |
| "Cree un fichier [nom]" | Cree un nouveau fichier |
| "Envoie un email a [destinataire]" | Compose et envoie un email |
| "Ajoute un rendez-vous [details]" | Ajoute au calendrier |
| "Push vers GitHub" | Git commit et push |

### 9.2 Commandes Mathematiques
| Commande | Action |
|----------|--------|
| "Resous [equation]" | Resolution avec WolframAlpha |
| "Prouve que [theoreme]" | Lance une preuve Isabelle |
| "Verifie ma preuve [fichier.thy]" | Verification Isabelle |
| "Explique [concept math]" | Explication detaillee |
| "Graphe la fonction [f(x)]" | Genere un graphique |

### 9.3 Commandes de Memoire Mathematique
| Commande | Action |
|----------|--------|
| "Ajoute le theoreme [nom]: [enonce]" | Sauvegarde un theoreme |
| "Definis [terme]: [definition]" | Sauvegarde une definition |
| "Mes theoremes" | Liste vos theoremes enregistres |
| "Mes definitions" | Liste vos definitions |
| "Contexte mathematique" | Affiche tout votre contexte |

L'agent utilise automatiquement vos theoremes et definitions lors des conversations mathematiques!

### 9.4 Commandes Vocales
1. Cliquez sur l'icone microphone ou dites "Hey Agent"
2. Parlez naturellement en francais ou anglais
3. L'agent transcrira et executera

### 9.4 Raccourcis Clavier
| Raccourci | Action |
|-----------|--------|
| Ctrl+Enter | Envoyer le message |
| Ctrl+M | Activer/desactiver microphone |
| Ctrl+N | Nouvelle conversation |
| Ctrl+S | Sauvegarder la conversation |
| Ctrl+O | Ouvrir un fichier |
| F1 | Aide |

---

## 10. Depannage

### Probleme: Ollama ne repond pas
```powershell
# Verifier que Ollama tourne
ollama serve

# Dans un autre terminal, tester
ollama run llama3.2 "test"
```

### Probleme: Erreur de module Python
```powershell
# Reinstaller les dependances
pip install --force-reinstall -r requirements.txt
```

### Probleme: Isabelle non trouve
1. Verifiez le chemin dans `.env`
2. Verifiez que le PATH est configure
3. Redemarrez PowerShell

### Probleme: Microphone non detecte
1. Verifiez les permissions Windows: Parametres > Confidentialite > Microphone
2. Reinstallez PyAudio

### Probleme: Erreur OpenAI API
1. Verifiez votre cle dans `.env`
2. Verifiez votre credit sur https://platform.openai.com/usage

### Probleme: Interface ne s'affiche pas
```powershell
# Verifier PyQt6
pip install --force-reinstall PyQt6
```

---

## Ressources Supplementaires

### Documentation Officielle
- Ollama: https://ollama.com/docs
- Isabelle: https://isabelle.in.tum.de/documentation.html
- OpenAI API: https://platform.openai.com/docs
- WolframAlpha API: https://products.wolframalpha.com/api/documentation

### Communaute et Support
- GitHub Issues: [Votre repo]/issues
- Discord Ollama: https://discord.gg/ollama
- Forum Isabelle: https://isabelle.zulipchat.com/

### Tutoriels Video Recommandes
- "Getting Started with Ollama on Windows" - YouTube
- "Isabelle/HOL Tutorial for Beginners" - YouTube
- "Building AI Agents with Python" - YouTube

---

## Notes de Version

**Version 1.0.0** - Janvier 2026
- Interface graphique Windows complete
- Integration Ollama + OpenAI
- Support Isabelle/HOL pour preuves mathematiques
- Integration WolframAlpha
- Gestion fichiers, emails, calendrier, GitHub
- Reconnaissance vocale
- Memoire persistante des conversations
- Support multilingue (FR/EN)

---

*Ce guide a ete cree pour vous accompagner pas a pas. En cas de difficulte, n'hesitez pas a consulter les ressources supplementaires ou a poser des questions.*
