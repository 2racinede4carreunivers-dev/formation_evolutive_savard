# Agent IA Local Mathématique

> Un assistant IA personnel, local, privé, et spécialisé en mathématiques avancées — pensé pour tourner **entièrement** sur votre machine, avec un système de sécurité propriétaire/invité et une architecture modulaire extensible.

**Propriétaire du projet :** Philippe Thomas Savard
**Version :** 1.0.0
**Licence :** Privée (usage personnel)
**Langues supportées :** Français (principal), Anglais

---

## Table des matières

1. [Vision et philosophie](#vision-et-philosophie)
2. [Fonctionnalités principales](#fonctionnalités-principales)
3. [Architecture technique](#architecture-technique)
4. [Installation](#installation)
5. [Démarrage rapide](#démarrage-rapide)
6. [Utilisation détaillée](#utilisation-détaillée)
7. [Système de sécurité](#système-de-sécurité)
8. [Modules et capacités](#modules-et-capacités)
9. [Configuration avancée](#configuration-avancée)
10. [Commandes et exemples](#commandes-et-exemples)
11. [Mémoire mathématique persistante](#mémoire-mathématique-persistante)
12. [Dépannage](#dépannage)
13. [Développement et extension](#développement-et-extension)
14. [Feuille de route](#feuille-de-route)

---

## Vision et philosophie

Cet agent a été conçu autour de trois principes fondamentaux :

### 1. Souveraineté des données
**Rien ne quitte votre machine par défaut.** Le LLM principal (Llama 3.2) tourne localement via Ollama, les conversations sont stockées en local, et aucune télémétrie n'est envoyée. Vous pouvez optionnellement brancher des API externes (OpenAI, WolframAlpha) mais elles restent **opt-in**.

### 2. Spécialisation mathématique
Contrairement aux assistants généralistes, cet agent est taillé pour la recherche mathématique :
- Théorie des nombres, géométrie, topologie, algèbre, analyse
- Intégration prévue avec **Isabelle/HOL** pour les preuves formelles
- Notation LaTeX native dans les réponses
- Mémoire persistante de théorèmes et définitions personnalisés

### 3. Sécurité par conception
Un système à deux modes (**PROPRIÉTAIRE** / **INVITÉ**) protège les actions sensibles et les données confidentielles. Toute action potentiellement dangereuse (envoi d'email, push GitHub, lecture de credentials) exige une authentification explicite via un code personnel.

---

## Fonctionnalités principales

| Domaine | Capacités |
|---|---|
| **Mathématiques** | Calcul symbolique (SymPy), résolution d'équations, dérivation, intégration, traçage de fonctions, preuves Isabelle/HOL (optionnel), ponts WolframAlpha |
| **Gestion de fichiers** | Lecture/exploration de dossiers (libre), création/modification de fichiers (authentifié) |
| **Email** | Rédaction et envoi via SMTP (Gmail/Outlook/custom) — **authentification requise** |
| **Calendrier** | Ajout d'événements, rappels, planification locale |
| **GitHub** | Clone, pull, commit, push — **authentification requise** |
| **Voix** | Reconnaissance vocale + synthèse (optionnel, configurable) |
| **Recherche web** | DuckDuckGo (sans tracker) pour veille et références |
| **Mémoire** | Contexte mathématique persistant (théorèmes, définitions, patterns de preuves) |
| **Sécurité** | Mode propriétaire/invité, verrouillage automatique, lockout anti-brute-force |

---

## Architecture technique

### Stack

- **Langage :** Python 3.11+
- **LLM local :** Ollama + Llama 3.2 (fallback OpenAI GPT-4o optionnel)
- **Conteneurisation :** Docker + docker-compose
- **Interface :** CLI interactive (Rich + Prompt Toolkit) + GUI PyQt6 optionnelle
- **Math :** SymPy, NumPy, Matplotlib, WolframAlpha API
- **Mémoire vectorielle :** ChromaDB (embeddings locaux)
- **Sécurité :** Gestionnaire d'état + timeout + lockout

### Arborescence

```
local_ai_agent/
├── main.py                    # Point d'entrée GUI (PyQt6)
├── main_cli.py                # Point d'entrée CLI (terminal/Docker)
├── config.yaml                # Configuration principale
├── .env                       # Clés API et secrets (NE PAS COMMITER)
├── .env.example               # Modèle de configuration
├── Dockerfile                 # Image GUI
├── Dockerfile.cli             # Image CLI allégée
├── docker-compose.yml         # Stack complète (agent + ollama)
├── docker-compose.cli.yml     # Stack CLI minimaliste
├── requirements.txt           # Dépendances GUI complètes
├── requirements-cli.txt       # Dépendances CLI minimales
├── src/
│   ├── core/
│   │   ├── agent.py           # Orchestrateur + SecurityManager
│   │   ├── llm_manager.py     # Abstraction LLM (Ollama/OpenAI)
│   │   ├── memory.py          # Persistance conversations
│   │   └── math_context.py    # Mémoire théorèmes/définitions
│   ├── modules/
│   │   ├── mathematics.py     # Module calcul symbolique
│   │   ├── file_manager.py    # Lecture/écriture fichiers
│   │   ├── email_manager.py   # SMTP
│   │   ├── calendar_manager.py # Planification
│   │   ├── github_manager.py  # Git/GitHub
│   │   └── voice.py           # STT + TTS
│   └── ui/
│       └── main_window.py     # Interface PyQt6
├── data/                      # Conversations, cache, base vectorielle
├── logs/                      # Journaux applicatifs
└── templates/                 # Modèles (email, documents)
```

### Flux d'exécution d'un message

```
Utilisateur → main_cli.py / main.py
               ↓
         MathAgent.process_message()
               ↓
   ┌─────────────────────────────────┐
   │  1. SecurityManager vérifie     │
   │     - code déverrouillage ?      │
   │     - code verrouillage ?        │
   │     - timeout d'inactivité ?     │
   │     - demande confidentielle ?   │
   └─────────────────────────────────┘
               ↓
         _detect_action() → action ou None
               ↓
   ┌─────────────────────────────────┐
   │  2. Si action sensible :         │
   │     mode PROPRIÉTAIRE requis     │
   │     sinon → refus motivé         │
   └─────────────────────────────────┘
               ↓
   ┌─────────────────────────────────┐
   │  3. Exécution :                  │
   │     - Action → module dédié      │
   │     - Sinon → chat LLM enrichi   │
   │       du contexte mathématique   │
   └─────────────────────────────────┘
               ↓
         Réponse + indicateur de mode
               ↓
         Sauvegarde conversation
```

---

## Installation

### Pré-requis

- **Docker Desktop** (Windows/Mac) ou **Docker Engine** (Linux) — [installation](https://docs.docker.com/get-docker/)
- **Git** pour cloner le dépôt
- **8 Go de RAM minimum** (16 Go recommandés pour Llama 3.2)
- **~6 Go d'espace disque** pour les images Docker + modèle Ollama
- *(Optionnel)* Clés API : OpenAI, WolframAlpha, GitHub

### Installation via Docker (recommandé)

```powershell
# 1. Cloner le dépôt
git clone https://github.com/2racinede4carreunivers-dev/agent-local-ia-carre.git
cd agent-local-ia-carre\local_ai_agent

# 2. Préparer la configuration
copy .env.example .env
# Éditez .env pour ajouter vos clés (optionnel)

# 3. Lancer la stack CLI (recommandé pour débuter)
docker compose -f docker-compose.cli.yml build --no-cache
docker compose -f docker-compose.cli.yml run --rm math-agent-cli
```

Pour la version GUI complète :
```bash
docker compose up --build
```

### Installation native (sans Docker)

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# ou .\venv\Scripts\activate    # Windows PowerShell

pip install -r requirements-cli.txt
cp .env.example .env
python3 main_cli.py
```

> ⚠️ Sans Docker, vous devez installer et démarrer Ollama séparément :
> `curl https://ollama.ai/install.sh | sh && ollama pull llama3.2`

---

## Démarrage rapide

1. **Lancer l'agent** : `docker compose -f docker-compose.cli.yml run --rm math-agent-cli`
2. **Vérifier le mode** : au démarrage, vous êtes en **MODE INVITÉ** (accès limité)
3. **Authentifier** : envoyez votre **code de déverrouillage personnel** (seul dans un message)
4. **Interagir** :
   - `Résous x^2 + 5x + 6 = 0`
   - `Définis groupe : Un ensemble muni d'une loi associative avec élément neutre et inverse`
   - `Ajoute le théorème Fermat : pour n>2, x^n + y^n = z^n n'a pas de solution entière non triviale`
   - `Mes théorèmes`
5. **Verrouiller** : envoyez le **code de verrouillage** pour revenir en mode invité
6. **Quitter** : `quit` ou `exit`

---

## Utilisation détaillée

### Mode invité (par défaut au démarrage)

Dans ce mode, l'agent reste utile mais bride les actions sensibles :

| Autorisé | Bloqué |
|---|---|
| Calculs mathématiques | Envoi d'emails |
| Preuves et démonstrations | Création de fichiers |
| Ajout/consultation de théorèmes | Push GitHub |
| Recherches web | Accès aux comptes (Gmail, Emergent…) |
| Lecture de fichiers | Exécution de commandes système |
| Conversation libre | Révélation de mots de passe/identifiants |

Les mots-clés confidentiels détectés automatiquement déclenchent un refus motivé :
`mot de passe`, `password`, `api key`, `credentials`, `mes comptes`, `gmail`, `emergent.sh`, etc.

### Mode propriétaire

Activé par le code personnel seul dans un message. Débloque :
- Toutes les actions sensibles
- L'accès aux données confidentielles
- Un indicateur en bas de chaque réponse : `Mode: PROPRIÉTAIRE | Verrouillage auto dans: 19m 42s`

Le verrouillage automatique s'enclenche après **20 minutes d'inactivité**. Vous pouvez aussi verrouiller manuellement en envoyant le **code de verrouillage**.

### Détection d'intentions

L'agent analyse votre message pour router vers le bon module :

| Si vous dites… | L'agent… |
|---|---|
| `résous`, `calcule`, `dérive`, `intègre` | → module Mathématiques |
| `prouve`, `démontre` | → module Preuves |
| `trace`, `graphe` | → module Tracé |
| `ouvre le fichier`, `lis le fichier` | → module Fichiers (lecture) |
| `crée un fichier`, `écris dans` | → module Fichiers (🔒 écriture) |
| `envoie un email`, `rédige un courriel` | → module Email (🔒) |
| `push`, `commit`, `clone`, `pull` | → module GitHub (🔒) |
| `ajoute un rendez-vous`, `planifie` | → module Calendrier |
| `ajoute le théorème …: …` | → Mémoire mathématique |
| `mes théorèmes`, `mes définitions` | → Consultation de la mémoire |
| `statut sécurité` | → État d'authentification |

Les actions marquées 🔒 exigent le mode propriétaire.

---

## Système de sécurité

### Deux codes personnels

| Rôle | Code |
|---|---|
| Déverrouillage (mode propriétaire) | `1374079226497308` |
| Verrouillage manuel (retour invité) | `$803911$` |

> 🚨 **Ces codes sont définis en dur dans `src/core/agent.py` (constantes `OWNER_UNLOCK_CODE` et `OWNER_LOCK_CODE`).** Modifiez-les avant tout déploiement ou partage.

### Mécanismes de protection

1. **Verrouillage automatique** après 20 minutes d'inactivité (`AUTO_LOCK_TIMEOUT = 1200s`)
2. **Lockout** de 5 minutes après 3 tentatives échouées
3. **Code isolé** : le code doit être envoyé **seul** dans un message (pas mélangé à une phrase)
4. **Indicateur visuel permanent** du mode actuel
5. **Journalisation** de toutes les tentatives dans `logs/agent_cli.log`
6. **Double détection** :
   - Actions sensibles (`SENSITIVE_ACTIONS` liste)
   - Mots-clés confidentiels (`CONFIDENTIAL_KEYWORDS` liste)

### Personnaliser les codes

Éditez `src/core/agent.py` :
```python
OWNER_UNLOCK_CODE = "VOTRE_NOUVEAU_CODE_LONG"
OWNER_LOCK_CODE = "VOTRE_CODE_DE_VERROUILLAGE"
AUTO_LOCK_TIMEOUT = 1200  # secondes
OWNER_NAME = "Votre Nom"
```

Voir **[SECURITY.md](SECURITY.md)** pour les avertissements détaillés et les limites du système.

---

## Modules et capacités

### Module Mathématiques (`src/modules/mathematics.py`)

- **Calcul symbolique** via SymPy : équations, dérivées, intégrales, limites, séries
- **Résolution numérique** : racines, systèmes linéaires, optimisation
- **Graphiques** via Matplotlib : 2D, 3D, surfaces, champs vectoriels
- **Preuves** : pont vers Isabelle/HOL (à configurer) et suggestions de tactiques
- **WolframAlpha** : calculs complexes si API configurée

### Module Fichiers (`src/modules/file_manager.py`)

- Navigation sécurisée dans les dossiers surveillés (`data/` par défaut)
- Lecture de `.py`, `.tex`, `.md`, `.pdf`, `.docx`, `.thy` (Isabelle)
- Écriture soumise à authentification
- Limite de taille : 50 Mo par défaut (configurable)

### Module Email (`src/modules/email_manager.py`)

- Rédaction assistée par LLM
- Envoi SMTP (Gmail avec mot de passe d'application recommandé, Outlook, SMTP custom)
- Templates personnalisables (`templates/email/`)
- **Confirmation obligatoire** avant tout envoi

### Module Calendrier (`src/modules/calendar_manager.py`)

- Stockage local par défaut (fichier JSON)
- Rappels à 30 minutes par défaut
- Extensions futures prévues : Google Calendar, CalDAV

### Module GitHub (`src/modules/github_manager.py`)

- Clone, pull, status : libres
- Commit, push, création de PR : nécessite le mode propriétaire + token GitHub
- Préfixe de commit automatique : `[Agent] <message>`

### Module Voix (`src/modules/voice.py`)

- Désactivé par défaut (`ENABLE_VOICE=false`)
- Reconnaissance via SpeechRecognition (Google ou Whisper local)
- Synthèse via pyttsx3 (voix française)
- Nécessite un micro fonctionnel et des dépendances système (PortAudio)

### Module Mémoire (`src/core/memory.py` + `src/core/math_context.py`)

- Persistance des conversations complètes en JSON
- Base vectorielle ChromaDB pour recherche sémantique
- Contexte mathématique structuré : théorèmes, définitions, patterns de preuves
- Enrichissement automatique du prompt système avec les éléments pertinents

---

## Configuration avancée

### `config.yaml` — structure clé

```yaml
general:
  language: fr                # fr ou en
  theme: dark                 # dark ou light

llm:
  default_provider: ollama    # ollama ou openai
  ollama:
    model: llama3.2           # llama3.2, mistral, codellama, etc.
    host: http://ollama:11434 # http://localhost:11434 en natif
  openai:
    model: gpt-4o
    max_tokens: 4096
  auto_switch_to_openai:
    complex_math: true        # Bascule auto si problème complexe
    threshold_tokens: 2000

mathematics:
  wolfram:
    enabled: true             # Nécessite WOLFRAM_APP_ID dans .env
  isabelle:
    enabled: false
    path: ""                  # Chemin vers isabelle si installé

security:
  confirm_actions:
    delete_files: true
    send_emails: true
    git_push: true
  encrypt_sensitive_data: true
  logging:
    level: INFO               # DEBUG, INFO, WARNING, ERROR
```

### `.env` — secrets (NE JAMAIS COMMITER)

```bash
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3.2

OPENAI_API_KEY=sk-...         # Optionnel
WOLFRAM_APP_ID=XXXX-XXXX      # Optionnel

EMAIL_ADDRESS=vous@gmail.com
EMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx   # Mot de passe d'application Gmail

GITHUB_TOKEN=ghp_...
GITHUB_USERNAME=votre-user

ENABLE_VOICE=false
ENABLE_FILE_ACCESS=true
ENABLE_SYSTEM_COMMANDS=false
```

### Changer de modèle Ollama

```bash
# Dans le conteneur Ollama
docker exec -it ollama ollama pull mistral
# Puis dans config.yaml :
#   llm.ollama.model: "mistral"
```

Modèles recommandés :
- **llama3.2** (3B) : rapide, qualité correcte — 4 Go RAM
- **llama3.1:8b** : meilleur raisonnement — 8 Go RAM
- **qwen2.5-math:7b** : spécialisé mathématiques — 8 Go RAM
- **deepseek-coder:6.7b** : pour génération de code

---

## Commandes et exemples

### Mathématiques

```
Résous l'équation x^3 - 6x^2 + 11x - 6 = 0
Dérive f(x) = sin(x^2) * exp(-x)
Intègre entre 0 et pi la fonction x*sin(x)
Calcule la limite quand x tend vers 0 de (sin x)/x
Factorise x^4 + 4
Trace la fonction f(x) = x^3 - 3x + 1 sur [-3, 3]
Résous le système : 2x + 3y = 12 ; x - y = 1
```

### Preuves et raisonnement

```
Prouve que la somme des n premiers entiers vaut n(n+1)/2
Démontre l'irrationalité de sqrt(2)
Énonce et prouve le théorème de Bezout
Vérifie la preuve : [coller ici une preuve en Isabelle]
```

### Mémoire personnalisée

```
Ajoute le théorème Pythagore : Dans un triangle rectangle, a^2 + b^2 = c^2
Définis homéomorphisme : Bijection continue dont la réciproque est continue
Mes théorèmes
Mes définitions
Rappelle-toi mon contexte
```

### Fichiers (lecture libre, écriture protégée)

```
Lis le fichier data/notes.md
Ouvre le dossier data/preuves
Crée un fichier data/brouillon.tex avec le contenu "..."   [🔒 auth]
```

### Email (🔒)

```
Rédige un email à prof@univ.fr pour demander un rendez-vous la semaine prochaine
Envoie l'email que tu viens de rédiger
```

### GitHub (🔒)

```
Clone le dépôt https://github.com/user/repo
Commit tous les fichiers modifiés avec le message "Corrections"
Push sur la branche main
```

### Sécurité

```
1374079226497308                   # Déverrouille (mode propriétaire)
$803911$                           # Verrouille (mode invité)
statut sécurité                    # Affiche le mode actuel + timer
```

### Commandes spéciales CLI

```
aide / help / ?                    # Rappel des commandes
clear                              # Efface l'écran
quit / exit / q                    # Quitter l'agent
```

---

## Mémoire mathématique persistante

Cette fonctionnalité est l'une des plus puissantes : l'agent se souvient de vos théorèmes et définitions **entre les sessions**.

### Ajouter un élément

```
Ajoute le théorème Cauchy-Schwarz : |<u,v>| <= ||u|| * ||v|| dans tout espace préhilbertien
Définis topologie : Une famille de parties d'un ensemble X stable par union quelconque et intersection finie, contenant X et vide
```

### Rappel automatique

Lorsque vous posez une question, l'agent recherche dans votre mémoire les théorèmes et définitions pertinents et les injecte dans le prompt. Exemple :

> **Vous :** Explique-moi les conséquences de Cauchy-Schwarz en analyse fonctionnelle.
>
> **Agent :** *[L'agent a récupéré automatiquement le théorème Cauchy-Schwarz de votre mémoire et construit une réponse contextuelle.]*

### Stockage

- Fichier : `data/math_context.json`
- Base vectorielle : `data/chromadb/`
- Sauvegarde recommandée : ajoutez `data/` à votre sauvegarde régulière (hors Git)

---

## Dépannage

### L'agent démarre mais répond « Desole, une erreur s'est produite: attempted relative import beyond top-level package »

Imports Python mal résolus. **Vérifié et corrigé en v1.0.0.** Si l'erreur réapparaît après modifications, assurez-vous que `src/core/agent.py` utilise le pattern try/except pour les imports :
```python
try:
    from ..modules.mathematics import MathModule
except ImportError:
    from modules.mathematics import MathModule
```

### « Erreur d'initialisation: name 'context_info' is not defined »

Bug corrigé en v1.0.0. Si persistant, forcez une resynchronisation :
```powershell
cd agent-local-ia-carre
git fetch origin
git reset --hard origin/main
cd local_ai_agent
docker compose -f docker-compose.cli.yml build --no-cache
```

### Ollama non disponible

```
Ollama non disponible: No module named 'ollama'
Cle OpenAI non configuree ou invalide
```
L'agent tombe en mode dégradé. Vérifiez que le conteneur `ollama` est bien lancé :
```bash
docker ps | grep ollama
docker logs ollama
```
Pour télécharger le modèle si absent :
```bash
docker exec -it ollama ollama pull llama3.2
```

### Lockout de sécurité déclenché

Après 3 codes erronés, un lockout de 5 minutes est actif. Attendez, ou redémarrez le conteneur pour réinitialiser (non recommandé en production).

### Le code de déverrouillage n'est pas reconnu

Le code doit être envoyé **seul**, sans espace avant/après, sans autre caractère. Exemple correct :
```
1374079226497308
```
Incorrect :
```
Mon code : 1374079226497308 merci
```

### Les messages ne sont pas sauvegardés

Vérifiez les permissions sur `data/` et `logs/` :
```bash
docker exec -it math-agent-cli ls -la /app/data /app/logs
```

---

## Développement et extension

### Ajouter un nouveau module

1. Créez `src/modules/votre_module.py` avec une classe `VotreModule`
2. Ajoutez une propriété lazy-loaded dans `agent.py` :
   ```python
   @property
   def votre_module(self):
       if self._votre_module is None:
           try:
               from ..modules.votre_module import VotreModule
           except ImportError:
               from modules.votre_module import VotreModule
           self._votre_module = VotreModule(self.config)
       return self._votre_module
   ```
3. Ajoutez les règles de détection dans `_detect_action()`
4. Ajoutez le routage dans `_execute_action()`
5. Si sensible, ajoutez le type d'action dans `SENSITIVE_ACTIONS`

### Changer de LLM

Éditez `src/core/llm_manager.py` pour supporter Anthropic, Mistral API, ou un autre provider. L'abstraction expose une méthode unique `chat(messages) -> str`.

### Tests

```bash
cd local_ai_agent
python3 -c "
import sys; sys.path.insert(0, 'src')
import yaml; from core.agent import MathAgent
config = yaml.safe_load(open('config.yaml'))
agent = MathAgent(config)
print('OK - Agent initialisé, mode:', agent.security.mode_name)
"
```

### Logs

Tous les événements sont journalisés dans `logs/agent_cli.log` (CLI) ou `logs/agent.log` (GUI). Niveau configurable dans `config.yaml` (`security.logging.level`).

---

## Feuille de route

### v1.1 (prochaine)
- [ ] Intégration complète Isabelle/HOL avec vérification automatique des preuves
- [ ] Export LaTeX des conversations (rapports de recherche)
- [ ] Mode multi-session (plusieurs propriétaires avec codes distincts)

### v1.2
- [ ] Intégration Notion / Obsidian (sync bidirectionnelle des notes)
- [ ] Tableau de bord web léger (FastAPI + HTMX) en alternative au CLI/GUI
- [ ] Modules avancés : SageMath, PARI/GP pour théorie des nombres

### v2.0
- [ ] Agent autonome : exécution de tâches planifiées (veille mathématique, rapports hebdo)
- [ ] RAG multi-documents sur vos articles et livres (PDF, LaTeX)
- [ ] Voix temps-réel avec Whisper local
- [ ] Interface mobile (PWA)

---

## Contribution

Ce projet est personnel et pas officiellement ouvert aux contributions externes. Pour signaler un bug ou proposer une amélioration, ouvrez une issue sur le dépôt GitHub.

---

## Avertissements

Consultez impérativement **[SECURITY.md](SECURITY.md)** avant toute utilisation en production ou tout partage. Ce document détaille :
- Les limites physiques et conceptuelles du système de sécurité
- Les risques liés aux LLMs (hallucinations, contournements)
- Les précautions à prendre pour les données confidentielles
- Les responsabilités de l'utilisateur

---

## Licence et crédits

**Projet privé** — Philippe Thomas Savard, 2026.
Cet agent n'est pas distribué sous licence libre. Usage personnel uniquement.

**Technologies tierces utilisées** :
- [Ollama](https://ollama.ai) & Llama 3.2 (Meta)
- [SymPy](https://www.sympy.org), [NumPy](https://numpy.org), [Matplotlib](https://matplotlib.org)
- [Rich](https://github.com/Textualize/rich) & [Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io)
- [ChromaDB](https://www.trychroma.com)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) (GUI optionnelle)

Merci aux communautés open source qui rendent ce genre d'agent local accessible.

---
-Avertissement: Cette IA est en lien avec IA Satan du même dévelopeur pour la sécurité des utilisateur: Comme il a été déterminé que l'IA a des hallucinations les dévelopeurs de cette IA on généré cete IA pour qu'elle ne soit qu'une halluciantion il n'y a donc rien de vrai qui sort de cette IA. Nous préfèrons vous en avertir.
*Document de référence — v1.0.0 — dernière mise à jour : avril 2026*
