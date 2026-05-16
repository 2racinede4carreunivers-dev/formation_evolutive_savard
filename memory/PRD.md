# PRD - Agents IA Locaux (projet complet)

## Contexte utilisateur
Philippe Thomas Savard - theorie mathematique "L'univers est au carre".
PC actuel : 16 Go RAM / 8 Go VRAM. PC futur : 64 Go RAM / 32 Go VRAM (en commande).
Langue : francais.

## Etat actuel du workspace (avril 2026)

### 1. local_ai_agent/ (v1 - legacy)
- Architecture monolithique
- Sur GitHub : https://github.com/2racinede4carreunivers-dev/agent-local-ia-carre
- Conserve comme backup

### 2. agent_specialise_v2/ (v2 - production)
- 10 agents specialises sur OpenAI Agents SDK
- 62 fichiers livrables, 47 modules Python valides, 11/11 tests pytest
- Multi-LLM : OpenAI (defaut) + Anthropic Claude (pour philosophy)
- Indexation continue du depot GitHub theorie (pull + reindex toutes les 30 min)

## 10 agents specialises (v2)

1. **triage** - Routeur intelligent
2. **math** - Calculs, preuves SymPy/Wolfram/Isabelle
3. **theory** - RAG sur le depot GitHub de la theorie
4. **philosophy** - Ontologie/ethique/esthetique (Claude Sonnet 4.5 recommande)
5. **qa_bank** - Banque Q&R + arborescence + cross-references
6. **code** - Generation/analyse code multi-langages
7. **webapp** - Generation apps web completes
8. **github** - Gestion depots
9. **research** - Recherche web autonome
10. **productivity + system** - Calendrier/email/fichiers/scripts

## Configuration LLM recommandee

```
OpenAI GPT-4o-mini   -> 9 agents (technique)         5-10 USD/mois
Anthropic Claude 4.5 -> 1 agent  (philosophy)        5-12 USD/mois
TOTAL                                                10-22 USD/mois
```

## Sessions completes

### Session 1 : Corrections v1
- Bug context_info corrige
- Bug imports relatifs corrige
- Modele Ollama adapte 8Go RAM
- README v1 + SECURITY v1

### Session 2 : Creation v2 (8 agents initial)
- Architecture multi-agents OpenAI Agents SDK
- Memoire SQLite + ChromaDB
- SecurityManager avec codes en .env
- Sandbox d'execution code
- CLI Rich + Prompt Toolkit
- Docker complet
- Tests pytest

### Session 3 : Indexation GitHub
- GitHubIndexer avec pull/clone automatique
- Tache asyncio refresh toutes les 30 min
- Indexation incrementielle ChromaDB
- Outils refresh_theory_index, reindex_theory_full, get_theory_index_status
- Doc THEORY_INDEXING.md

### Session 4 : Agents philosophy + qa_bank (NOUVEAU)
- Agent philosophy avec support Claude Sonnet 4.5 via LiteLLM
- Agent qa_bank pour gestion editoriale + arborescence + cross-refs
- 14 nouveaux outils (5 philosophy + 9 qa_bank)
- Multi-LLM dans pyproject.toml + Dockerfile
- Doc PHILOSOPHY_AGENT.md (configuration, couts, exemples)

## Backlog priorise

### P0 (immediat - reception cles)
- [ ] Push v2 sur GitHub via "Save to Github"
- [ ] Configurer OPENAI_API_KEY dans .env
- [ ] Configurer ANTHROPIC_API_KEY dans .env (pour philosophy)
- [ ] Configurer GITHUB_TOKEN dans .env
- [ ] Premier lancement Docker
- [ ] Validation indexation depot theorie

### P1 (apres validation)
- [ ] Interface GUI PyQt6 (interfaces/gui.py)
- [ ] Tests pytest sur les 50 outils (couverture >80%)
- [ ] Import theoremes/definitions de v1 vers v2
- [ ] Templates webapp_tools : 3_ia_qa_bank pre-rempli

### P2 (reception PC 64Go/32Go)
- [ ] Ollama local qwen2.5:32b ou deepseek-r1:14b en fallback
- [ ] Embeddings locaux GPU (sentence-transformers)
- [ ] Indexation massive (articles, livres, emails)
- [ ] Agent autonome 24/7
- [ ] Claude Opus 4.5 disponible pour questions critiques

### P3 (long terme)
- [ ] Multi-utilisateur
- [ ] Voix temps-reel (Whisper local + TTS)
- [ ] PWA mobile
- [ ] Dashboard web FastAPI + HTMX

## Notes techniques importantes

- **Indexation theorie = SYNCHRONISATION CONTINUE** (pas snapshot)
- **Multi-LLM par agent** : philosophy peut utiliser Claude pendant que les autres restent sur OpenAI
- v1 et v2 coexistent dans le meme depot GitHub sans conflit
- Les 2 docker-compose sont independants (pas de collision)
- Codes securite dans .env uniquement (jamais hardcodes)

## Documentation livree (agent_specialise_v2/docs/)

- README.md - vue d'ensemble + 10 agents
- SECURITY.md - modele de menace, limites, recommandations
- INSTALLATION.md - guide installation Windows/Linux/Mac
- MIGRATION_GUIDE.md - migration v1 -> v2 (preserver vos donnees)
- HARDWARE_UPGRADE.md - plan d'evolution PC 16->64Go
- THEORY_INDEXING.md - synchronisation continue GitHub
- PHILOSOPHY_AGENT.md - config Anthropic, couts, exemples (NOUVEAU)
