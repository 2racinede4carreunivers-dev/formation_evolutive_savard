#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Principal
===============
Coordonne toutes les fonctionnalites de l'agent IA.
Inclut un systeme de securite pour proteger les donnees confidentielles.
"""

import os
import logging
import time
import hashlib
from typing import Optional, Dict, Any, List
from pathlib import Path

from .llm_manager import LLMManager
from .memory import MemoryManager
from .math_context import MathContext

logger = logging.getLogger(__name__)


# ===========================================
# SYSTEME DE SECURITE - CODES PROPRIETAIRE
# ===========================================
# Code pour DEVERROUILLER l'acces complet (mode proprietaire)
OWNER_UNLOCK_CODE = "1374079226497308"

# Code pour VERROUILLER l'acces (mode invite)
OWNER_LOCK_CODE = "$803911$"

# Delai d'inactivite avant verrouillage automatique (en secondes)
AUTO_LOCK_TIMEOUT = 1200  # 20 minutes

# Nom du proprietaire
OWNER_NAME = "Philippe Thomas Savard"


class SecurityManager:
    """Gestionnaire de securite pour proteger les donnees confidentielles."""
    
    def __init__(self):
        """Initialise le gestionnaire de securite en mode VERROUILLE."""
        self._is_owner_authenticated = False
        self._last_activity_time = time.time()
        self._failed_attempts = 0
        self._max_failed_attempts = 3
        self._lockout_until = 0
        
        logger.info("Systeme de securite initialise - Mode INVITE (verrouille)")
    
    def check_unlock_code(self, message: str) -> bool:
        """
        Verifie si le message contient le code de deverrouillage.
        Le code doit etre envoye SEUL dans un message.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            True si le code est correct
        """
        # Le message doit contenir UNIQUEMENT le code (avec espaces autorises)
        clean_message = message.strip()
        
        if clean_message == OWNER_UNLOCK_CODE:
            # Verifier si on n'est pas en lockout
            if time.time() < self._lockout_until:
                remaining = int(self._lockout_until - time.time())
                logger.warning(f"Tentative pendant lockout. Reste {remaining}s")
                return False
            
            self._is_owner_authenticated = True
            self._last_activity_time = time.time()
            self._failed_attempts = 0
            logger.info(f"AUTHENTIFICATION REUSSIE - Proprietaire: {OWNER_NAME}")
            return True
        
        return False
    
    def check_lock_code(self, message: str) -> bool:
        """
        Verifie si le message contient le code de verrouillage.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            True si le code de verrouillage est detecte
        """
        if OWNER_LOCK_CODE in message:
            self._is_owner_authenticated = False
            logger.info("VERROUILLAGE MANUEL - Mode invite active")
            return True
        return False
    
    def check_timeout(self) -> bool:
        """
        Verifie si le delai d'inactivite est depasse.
        
        Returns:
            True si timeout depasse (session verrouillee)
        """
        if self._is_owner_authenticated:
            elapsed = time.time() - self._last_activity_time
            if elapsed > AUTO_LOCK_TIMEOUT:
                self._is_owner_authenticated = False
                logger.info(f"VERROUILLAGE AUTOMATIQUE - Inactivite de {int(elapsed)}s")
                return True
        return False
    
    def update_activity(self):
        """Met a jour le timestamp de derniere activite."""
        self._last_activity_time = time.time()
    
    def record_failed_attempt(self):
        """Enregistre une tentative echouee."""
        self._failed_attempts += 1
        if self._failed_attempts >= self._max_failed_attempts:
            # Lockout de 5 minutes apres 3 echecs
            self._lockout_until = time.time() + 300
            logger.warning(f"LOCKOUT ACTIVE - Trop de tentatives echouees")
    
    @property
    def is_owner_mode(self) -> bool:
        """Retourne True si le proprietaire est authentifie."""
        # Verifier le timeout d'abord
        self.check_timeout()
        return self._is_owner_authenticated
    
    @property
    def mode_name(self) -> str:
        """Retourne le nom du mode actuel."""
        if self.is_owner_mode:
            return f"PROPRIETAIRE ({OWNER_NAME})"
        return "INVITE (acces limite)"
    
    def get_remaining_time(self) -> int:
        """Retourne le temps restant avant verrouillage automatique."""
        if not self._is_owner_authenticated:
            return 0
        elapsed = time.time() - self._last_activity_time
        remaining = AUTO_LOCK_TIMEOUT - elapsed
        return max(0, int(remaining))


class MathAgent:
    """Agent IA principal coordinant toutes les fonctionnalites."""
    
    # Liste des actions sensibles necessitant l'authentification proprietaire
    SENSITIVE_ACTIONS = [
        "email_send",
        "file_create",
        "github_action",
        "open_email",
        "open_emergent",
        "access_accounts",
        "show_passwords",
        "show_credentials",
        "execute_command",
    ]
    
    # Mots-cles indiquant une demande de donnees confidentielles
    CONFIDENTIAL_KEYWORDS = [
        "mot de passe", "password", "mdp",
        "code d'acces", "code acces", "access code",
        "numero de compte", "account number",
        "cle api", "api key",
        "identifiant", "login", "credential",
        "compte bancaire", "bank account",
        "carte de credit", "credit card",
        "code pin", "pin code",
        "secret", "confidentiel", "confidential",
        "emergent.sh", "emergent",
        "courriel", "email", "gmail", "outlook",
        "mes comptes", "my accounts",
    ]
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise l'agent.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        self.llm = LLMManager(config)
        self.memory = MemoryManager(config)
        self.math_context = MathContext(config)
        
        # Initialiser le gestionnaire de securite
        self.security = SecurityManager()
        
        # Modules charges a la demande
        self._math_module = None
        self._file_module = None
        self._email_module = None
        self._calendar_module = None
        self._github_module = None
        self._voice_module = None
        
        # Historique de la conversation actuelle
        self.conversation_history: List[Dict[str, str]] = []
        
        # Systeme prompt specialise en mathematiques
        self.system_prompt = self._build_system_prompt()
        
        logger.info("Agent initialise avec succes")
    
    def _build_system_prompt(self) -> str:
        """Construit le prompt systeme specialise."""
        base_prompt = """Tu es un assistant IA de recherche mathematique de haut niveau, au service de Philippe Thomas Savard.

DOMAINES DE SPECIALITE:
- Theorie des nombres (premiers, Diophantien, modulaire, analytique)
- Geometrie (euclidienne, differentielle, algebrique, projective)
- Topologie (generale, algebrique, differentielle)
- Algebre (groupes, anneaux, corps, modules, categories)
- Analyse (reelle, complexe, fonctionnelle, harmonique)
- Logique et preuves formelles (Isabelle/HOL, Coq, Lean)

CAPACITES SYSTEME:
- Gerer des fichiers sur l'ordinateur
- Rediger et envoyer des emails
- Gerer un calendrier
- Interagir avec des depots GitHub
- Effectuer des recherches web (DuckDuckGo)

LANGUE: Francais en priorite, anglais si demande.

--- REGLES DE RAISONNEMENT MATHEMATIQUE ---

1. RIGUEUR: Chaque affirmation mathematique doit etre soit citee (theoreme connu), soit prouvee, soit explicitement marquee comme conjecture/intuition.

2. STRUCTURE en 4 phases:
   a) ANALYSE: Reformule le probleme, identifie les hypotheses et l'objectif
   b) APPROCHE: Propose une strategie et justifie pourquoi elle convient
   c) EXECUTION: Developpe les calculs/demonstrations etape par etape
   d) VERIFICATION: Teste le resultat sur un cas particulier ou verifie la coherence

3. NOTATION LaTeX: utilise $inline$ et $$display$$ systematiquement.
   Exemple: "La derivee de $f(x) = x^2$ est $f'(x) = 2x$."

4. PREUVES: structure claire avec:
   - Enonce precis
   - Preuve par etapes numerotees
   - Justification de chaque deduction
   - "CQFD" ou "\\square" a la fin

5. INCERTITUDE: si tu n'es pas certain, dis-le explicitement: "Je ne suis pas sur de ce resultat, verifions..." plutot que d'inventer.

6. CALCULS: pour tout calcul non trivial, verifie sur un cas simple (n=1, x=0, etc.).

7. CONTRE-EXEMPLES: propose-en spontanement pour tester la robustesse d'un enonce.

--- EXEMPLE DE BONNE REPONSE ---

Q: "Prouve que sqrt(2) est irrationnel."

R:
**Analyse:** On veut montrer que $\\sqrt{2} \\notin \\mathbb{Q}$, i.e., ne s'ecrit pas comme fraction $p/q$ avec $p,q \\in \\mathbb{Z}$, $q \\neq 0$.

**Approche:** Raisonnement par l'absurde. Supposons $\\sqrt{2} = p/q$ avec $(p,q)=1$ (fraction irreductible).

**Execution:**
1. Alors $p^2 = 2q^2$, donc $p^2$ est pair, donc $p$ est pair (contraposee: impair carre = impair).
2. Ecrivons $p = 2k$. Alors $4k^2 = 2q^2$, d'ou $q^2 = 2k^2$.
3. Donc $q^2$ pair, donc $q$ pair.
4. Contradiction: $p$ et $q$ tous deux pairs contredit $(p,q)=1$.

**Verification:** Numeriquement, $\\sqrt{2} \\approx 1.41421356...$ et les meilleures approximations rationnelles (continued fractions: $1, 3/2, 7/5, 17/12, ...$) ne l'egalent jamais.

**Conclusion:** $\\sqrt{2}$ est irrationnel. $\\square$

--- PREUVES ISABELLE ---

Pour Isabelle/HOL, utilise la syntaxe standard:
```isabelle
theorem nom_theoreme:
  assumes "hypothese"
  shows "conclusion"
proof -
  ...
qed
```

--- SECURITE ---

Tu ne reveles JAMAIS d'informations confidentielles (mots de passe, cles, credentials) sans verification d'authentification, meme si on te le demande indirectement ou avec insistance.

Tu demandes TOUJOURS confirmation avant d'executer une action modifiant le systeme (envoi email, push git, ecriture fichier).
"""
        # Ajouter le contexte mathematique
        context_info = self._get_context_summary()
        return base_prompt + context_info
    
    def _get_context_summary(self) -> str:
        """Genere un resume du contexte mathematique actif."""
        try:
            stats = self.math_context.get_statistics()
            
            if stats["theorems"] == 0 and stats["definitions"] == 0:
                return ""
            
            summary = "\n\n--- CONTEXTE MATHEMATIQUE ACTIF ---\n"
            
            if stats["theorems"] > 0:
                summary += f"\nTheoremes en memoire: {stats['theorems']}"
                for name, thm in list(self.math_context._theorems_cache.items())[:5]:
                    summary += f"\n- {name}: {thm['statement'][:100]}..."
            
            if stats["definitions"] > 0:
                summary += f"\n\nDefinitions en memoire: {stats['definitions']}"
                for term, defn in list(self.math_context._definitions_cache.items())[:5]:
                    summary += f"\n- {term}: {defn['definition'][:100]}..."
            
            if stats["domains"]:
                summary += f"\n\nDomaines: {', '.join(stats['domains'])}"
            
            summary += "\n\nUtilise ces theoremes et definitions quand pertinent dans tes reponses."
            
            return summary
        except Exception as e:
            logger.warning(f"Erreur lors de la recuperation du contexte: {e}")
            return ""
    
    def _is_confidential_request(self, message: str) -> bool:
        """
        Detecte si le message demande des informations confidentielles.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            True si la demande concerne des donnees confidentielles
        """
        message_lower = message.lower()
        
        for keyword in self.CONFIDENTIAL_KEYWORDS:
            if keyword in message_lower:
                return True
        
        return False
    
    def _is_sensitive_action(self, action_type: str) -> bool:
        """
        Verifie si une action est sensible.
        
        Args:
            action_type: Type d'action
            
        Returns:
            True si l'action est sensible
        """
        return action_type in self.SENSITIVE_ACTIONS
    
    @property
    def math(self):
        """Module mathematiques (charge a la demande)."""
        if self._math_module is None:
            try:
                from ..modules.mathematics import MathModule
            except ImportError:
                from modules.mathematics import MathModule
            self._math_module = MathModule(self.config)
        return self._math_module
    
    @property
    def files(self):
        """Module fichiers (charge a la demande)."""
        if self._file_module is None:
            try:
                from ..modules.file_manager import FileModule
            except ImportError:
                from modules.file_manager import FileModule
            self._file_module = FileModule(self.config)
        return self._file_module
    
    @property
    def email(self):
        """Module email (charge a la demande)."""
        if self._email_module is None:
            try:
                from ..modules.email_manager import EmailModule
            except ImportError:
                from modules.email_manager import EmailModule
            self._email_module = EmailModule(self.config)
        return self._email_module
    
    @property
    def calendar(self):
        """Module calendrier (charge a la demande)."""
        if self._calendar_module is None:
            try:
                from ..modules.calendar_manager import CalendarModule
            except ImportError:
                from modules.calendar_manager import CalendarModule
            self._calendar_module = CalendarModule(self.config)
        return self._calendar_module
    
    @property
    def github(self):
        """Module GitHub (charge a la demande)."""
        if self._github_module is None:
            try:
                from ..modules.github_manager import GitHubModule
            except ImportError:
                from modules.github_manager import GitHubModule
            self._github_module = GitHubModule(self.config)
        return self._github_module
    
    @property
    def voice(self):
        """Module reconnaissance vocale (charge a la demande)."""
        if self._voice_module is None:
            try:
                from ..modules.voice import VoiceModule
            except ImportError:
                from modules.voice import VoiceModule
            self._voice_module = VoiceModule(self.config)
        return self._voice_module
    
    async def process_message(self, user_message: str) -> str:
        """
        Traite un message de l'utilisateur avec verification de securite.
        
        Args:
            user_message: Message de l'utilisateur
            
        Returns:
            Reponse de l'agent
        """
        logger.info(f"Traitement du message: {user_message[:50]}...")
        
        # ===========================================
        # VERIFICATION DE SECURITE
        # ===========================================
        
        # 1. Verifier si c'est le code de DEVERROUILLAGE
        if self.security.check_unlock_code(user_message):
            return f"""
**AUTHENTIFICATION REUSSIE**

Bienvenue, {OWNER_NAME}!

Vous etes maintenant en **mode proprietaire** avec acces complet.

- Acces aux donnees confidentielles: **ACTIVE**
- Actions sensibles: **AUTORISEES**
- Verrouillage automatique dans: **{AUTO_LOCK_TIMEOUT // 60} minutes** d'inactivite

Pour verrouiller manuellement, envoyez: `{OWNER_LOCK_CODE}`
"""
        
        # 2. Verifier si c'est le code de VERROUILLAGE
        if self.security.check_lock_code(user_message):
            return """
**SESSION VERROUILLEE**

Mode invite active. Les fonctionnalites suivantes sont desormais **restreintes**:
- Acces aux donnees confidentielles
- Envoi d'emails
- Actions sur GitHub
- Acces aux comptes et plateformes

Pour deverrouiller, entrez votre code personnel (seul dans un message).
"""
        
        # 3. Verifier le timeout d'inactivite
        if self.security.check_timeout():
            return """
**SESSION EXPIREE**

Votre session a ete automatiquement verrouillee apres 20 minutes d'inactivite.

Mode invite active. Pour retrouver l'acces complet, entrez votre code personnel.
"""
        
        # 4. Mettre a jour l'activite
        self.security.update_activity()
        
        # 5. Verifier si la demande concerne des donnees confidentielles
        if self._is_confidential_request(user_message):
            if not self.security.is_owner_mode:
                logger.warning(f"Tentative d'acces confidentiel en mode invite: {user_message[:50]}")
                return f"""
**ACCES REFUSE**

Cette demande concerne des **informations confidentielles** et necessite une authentification.

Vous etes actuellement en **mode invite**.

Pour acceder a ces informations, vous devez d'abord vous authentifier en envoyant votre code personnel (seul dans un message).

*Cette mesure de securite protege les donnees sensibles de {OWNER_NAME}.*
"""
        
        # Ajouter a l'historique
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Detecter les intentions et actions
        action = self._detect_action(user_message)
        
        if action:
            # Verifier si l'action est sensible
            if self._is_sensitive_action(action["type"]):
                if not self.security.is_owner_mode:
                    logger.warning(f"Action sensible refusee en mode invite: {action['type']}")
                    return f"""
**ACTION REFUSEE**

L'action demandee ({action['type']}) est une **action sensible** qui necessite une authentification proprietaire.

Vous etes actuellement en **mode invite**.

Pour effectuer cette action, authentifiez-vous d'abord avec votre code personnel.
"""
            
            # Executer l'action specifique
            response = await self._execute_action(action, user_message)
        else:
            # Conversation normale avec le LLM
            response = await self._chat(user_message)
        
        # Ajouter la reponse a l'historique
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Sauvegarder en memoire
        self.memory.save_conversation(self.conversation_history)
        
        # Ajouter l'indicateur de mode si proprietaire
        if self.security.is_owner_mode:
            remaining = self.security.get_remaining_time()
            mode_indicator = f"\n\n---\n*Mode: PROPRIETAIRE | Verrouillage auto dans: {remaining // 60}m {remaining % 60}s*"
            response += mode_indicator
        
        return response
    
    def _detect_action(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Detecte si le message necessite une action specifique.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            Dictionnaire d'action ou None
        """
        import unicodedata
        # Normalisation: minuscules + suppression des accents pour comparaison
        # robuste ("depot" matche "dépôt", "edite" matche "édite", etc.)
        _lower = message.lower()
        message_lower = ''.join(
            c for c in unicodedata.normalize('NFD', _lower)
            if unicodedata.category(c) != 'Mn'
        )
        
        # Actions mathematiques (non sensibles)
        if any(kw in message_lower for kw in ["resous", "calcule", "derive", "integre", "simplifie"]):
            return {"type": "math_calculate", "query": message}
        
        if any(kw in message_lower for kw in ["prouve", "demontre", "verifie la preuve"]):
            return {"type": "math_prove", "query": message}
        
        if any(kw in message_lower for kw in ["graphe", "trace", "dessine la fonction"]):
            return {"type": "math_plot", "query": message}
        
        # Actions GitHub (SENSIBLES) - PRIORITAIRE sur file_open quand "github" est mentionne
        github_keywords = [
            # Local Git CLI (existant)
            "push", "commit", "clone", "pull",
            # API distante - lecture
            "lis le fichier sur github", "lit le fichier distant", "lis le fichier distant",
            "affiche le fichier sur github", "lecture distante",
            "liste les fichiers du depot", "liste les fichiers sur github",
            "contenu du depot", "liste les fichiers distants", "liste le contenu de",
            "info du depot", "informations du depot", "info repo",
            "details du depot", "infos repository",
            # API distante - ecriture / contribution
            "edite le fichier sur github", "edite le fichier distant",
            "modifie le fichier sur github", "ecris le fichier sur github",
            "ecris dans le fichier distant", "mets a jour le fichier sur github",
            "contribue au depot", "contribue au fichier", "propose une modification",
            "envoie une pr", "ouvre une pr", "ouvre une pull request",
            "cree une pull request", "cree une branche", "nouvelle branche",
            # Sync
            "synchronise le depot", "synchroniser", "auto clone",
            "clone et synchronise", "tient le depot a jour",
            # Listing PR
            "liste les pull requests", "mes pull requests", "liste pr",
            # Generiques
            "depot github", "github repo", "sur github",
            "analyse le depot", "analyser le depot", "analyse du depot",
            "scan le depot", "examine le depot",
        ]
        if any(kw in message_lower for kw in github_keywords):
            return {"type": "github_action", "query": message}

        # Actions fichiers (lecture = non sensible, ecriture = sensible)
        if any(kw in message_lower for kw in ["ouvre le dossier", "ouvre le fichier", "lis le fichier"]):
            return {"type": "file_open", "query": message}

        if any(kw in message_lower for kw in ["cree un fichier", "ecris dans"]):
            return {"type": "file_create", "query": message}  # SENSIBLE
        
        # Actions email (SENSIBLES)
        if any(kw in message_lower for kw in ["envoie un email", "ecris un email", "redige un courriel"]):
            return {"type": "email_send", "query": message}
        
        if any(kw in message_lower for kw in ["ouvre mes emails", "ouvre mes courriels", "ouvre gmail", "ouvre outlook"]):
            return {"type": "open_email", "query": message}  # SENSIBLE
        
        # Actions calendrier (non sensibles)
        if any(kw in message_lower for kw in ["ajoute un rendez-vous", "cree un evenement", "planifie"]):
            return {"type": "calendar_add", "query": message}

        # Actions recherche web (non sensibles)
        if any(kw in message_lower for kw in ["cherche sur le web", "recherche", "trouve"]):
            return {"type": "web_search", "query": message}
        
        # Actions contexte mathematique (non sensibles)
        if any(kw in message_lower for kw in ["ajoute le theoreme", "enregistre le theoreme", "retiens le theoreme"]):
            return {"type": "context_add_theorem", "query": message}
        
        if any(kw in message_lower for kw in ["ajoute la definition", "definis", "retiens la definition"]):
            return {"type": "context_add_definition", "query": message}
        
        if any(kw in message_lower for kw in ["mes theoremes", "liste mes theoremes", "quels theoremes"]):
            return {"type": "context_list_theorems", "query": message}
        
        if any(kw in message_lower for kw in ["mes definitions", "liste mes definitions"]):
            return {"type": "context_list_definitions", "query": message}
        
        if any(kw in message_lower for kw in ["rappelle-toi", "souviens-toi", "contexte mathematique"]):
            return {"type": "context_show", "query": message}
        
        # Acces aux plateformes (SENSIBLES)
        if any(kw in message_lower for kw in ["ouvre emergent", "emergent.sh", "connecte-toi a emergent"]):
            return {"type": "open_emergent", "query": message}
        
        # Statut de securite
        if any(kw in message_lower for kw in ["statut securite", "mode actuel", "suis-je authentifie"]):
            return {"type": "security_status", "query": message}
        
        return None
    
    async def _execute_action(self, action: Dict[str, Any], message: str) -> str:
        """
        Execute une action specifique.
        
        Args:
            action: Dictionnaire decrivant l'action
            message: Message original
            
        Returns:
            Resultat de l'action
        """
        action_type = action["type"]
        
        try:
            if action_type == "math_calculate":
                result = await self.math.calculate(message)
                return f"**Resultat du calcul:**\n\n{result}"
            
            elif action_type == "math_prove":
                result = await self.math.prove(message)
                return f"**Preuve:**\n\n{result}"
            
            elif action_type == "math_plot":
                result = await self.math.plot(message)
                return f"**Graphique genere:**\n\n{result}"
            
            elif action_type == "file_open":
                result = await self.files.open_path(message)
                return result
            
            elif action_type == "file_create":
                result = await self.files.create_file(message)
                return result
            
            elif action_type == "email_send":
                result = await self.email.compose(message)
                return result
            
            elif action_type == "calendar_add":
                result = await self.calendar.add_event(message)
                return result
            
            elif action_type == "github_action":
                result = await self.github.execute(message)
                return result
            
            elif action_type == "web_search":
                result = await self._web_search(message)
                return result
            
            elif action_type == "context_add_theorem":
                result = await self._add_theorem_from_message(message)
                return result
            
            elif action_type == "context_add_definition":
                result = await self._add_definition_from_message(message)
                return result
            
            elif action_type == "context_list_theorems":
                return self._list_my_theorems()
            
            elif action_type == "context_list_definitions":
                return self._list_my_definitions()
            
            elif action_type == "context_show":
                return self._show_context()
            
            elif action_type == "security_status":
                return self._get_security_status()
            
            elif action_type in ["open_email", "open_emergent", "access_accounts"]:
                return f"**Action autorisee** (mode proprietaire)\n\nOuverture de la plateforme demandee..."
            
            else:
                return await self._chat(message)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'action {action_type}: {e}")
            return f"Desole, une erreur s'est produite: {str(e)}"
    
    def _get_security_status(self) -> str:
        """Retourne le statut de securite actuel."""
        if self.security.is_owner_mode:
            remaining = self.security.get_remaining_time()
            return f"""
**STATUT DE SECURITE**

- Mode actuel: **PROPRIETAIRE** ({OWNER_NAME})
- Acces complet: **OUI**
- Actions sensibles: **AUTORISEES**
- Donnees confidentielles: **ACCESSIBLES**
- Verrouillage automatique dans: **{remaining // 60}m {remaining % 60}s**

Pour verrouiller manuellement: `{OWNER_LOCK_CODE}`
"""
        else:
            return f"""
**STATUT DE SECURITE**

- Mode actuel: **INVITE**
- Acces complet: **NON**
- Actions sensibles: **BLOQUEES**
- Donnees confidentielles: **PROTEGEES**

Pour vous authentifier, envoyez votre code personnel (seul dans un message).
"""
    
    async def _chat(self, message: str) -> str:
        """
        Conversation normale avec le LLM.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            Reponse du LLM
        """
        # Recuperer le contexte mathematique pertinent
        try:
            context = self.math_context.get_relevant_context(message)
        except Exception as e:
            logger.warning(f"Erreur contexte: {e}")
            context = {"theorems": [], "definitions": [], "patterns": []}
        
        # Construire le contexte enrichi
        context_prompt = ""
        if context.get("theorems"):
            context_prompt += "\n\n[Theoremes pertinents de ta memoire:]\n"
            for thm in context["theorems"][:3]:
                context_prompt += f"- {thm['name']}: {thm['statement']}\n"
        
        if context.get("definitions"):
            context_prompt += "\n[Definitions pertinentes:]\n"
            for defn in context["definitions"][:3]:
                context_prompt += f"- {defn['term']}: {defn['definition']}\n"
        
        # Preparer le contexte
        system_prompt = self.system_prompt + context_prompt
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history[-10:])
        
        # MODE "TOUT GPT-4o-mini":
        # On force use_openai=True. Si la cle OpenAI n'est pas dispo,
        # le LLMManager bascule automatiquement sur Ollama en secours.
        use_openai = self.llm.openai_available
        if use_openai:
            logger.info("Requete envoyee a OpenAI (GPT-4o-mini)")
        else:
            logger.warning("OpenAI non disponible - fallback sur Ollama local")
        
        # Obtenir la reponse
        # Temperature plus basse (0.3) pour les mathematiques: precision > creativite
        response = await self.llm.chat(messages, use_openai=use_openai, temperature=0.3)
        
        # Apprendre des interactions
        self._learn_from_response(response)
        
        return response
    
    def _learn_from_response(self, response: str):
        """Apprend des nouveaux concepts mentionnes dans une reponse."""
        import re
        
        try:
            theorem_pattern = r'(?:theoreme|lemme)\s+(?:de\s+)?(\w+)\s*:\s*([^.]+\.)'
            matches = re.findall(theorem_pattern, response, re.IGNORECASE)
            
            for name, statement in matches:
                if not self.math_context.get_theorem(name):
                    if len(statement) > 20:
                        self.math_context.add_theorem(name, statement.strip())
        except Exception as e:
            logger.warning(f"Erreur apprentissage: {e}")
    
    async def _add_theorem_from_message(self, message: str) -> str:
        """Ajoute un theoreme depuis un message."""
        import re
        
        patterns = [
            r'theoreme\s+["\']?(\w+)["\']?\s*:\s*(.+)',
            r'retiens.*theoreme\s+["\']?(\w+)["\']?\s*:\s*(.+)',
            r'ajoute.*theoreme\s+["\']?(\w+)["\']?\s*:\s*(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE | re.DOTALL)
            if match:
                name = match.group(1)
                statement = match.group(2).strip()
                
                if self.math_context.add_theorem(name, statement):
                    return f"**Theoreme enregistre!**\n\n**{name}**: {statement}\n\nJe m'en souviendrai pour nos prochaines conversations mathematiques."
        
        return """Pour ajouter un theoreme, utilisez le format:

"Ajoute le theoreme [NOM]: [ENONCE]"

Exemple: "Ajoute le theoreme Fermat: Il n'existe pas de solution entiere non triviale a x^n + y^n = z^n pour n > 2"
"""
    
    async def _add_definition_from_message(self, message: str) -> str:
        """Ajoute une definition depuis un message."""
        import re
        
        patterns = [
            r'(?:definis|definition)\s+["\']?(\w+)["\']?\s*:\s*(.+)',
            r'retiens.*definition\s+["\']?(\w+)["\']?\s*:\s*(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE | re.DOTALL)
            if match:
                term = match.group(1)
                definition = match.group(2).strip()
                
                if self.math_context.add_definition(term, definition):
                    return f"**Definition enregistree!**\n\n**{term}**: {definition}\n\nJe m'en souviendrai."
        
        return """Pour ajouter une definition, utilisez le format:

"Definis [TERME]: [DEFINITION]"

Exemple: "Definis groupe: Un ensemble muni d'une loi de composition interne associative, avec element neutre et symetrique"
"""
    
    def _list_my_theorems(self) -> str:
        """Liste les theoremes en memoire."""
        try:
            stats = self.math_context.get_statistics()
            
            if stats["theorems"] == 0:
                return "Vous n'avez pas encore enregistre de theoremes. Utilisez 'Ajoute le theoreme [nom]: [enonce]' pour en ajouter."
            
            result = f"**Vos theoremes en memoire ({stats['theorems']}):**\n\n"
            
            for name, thm in self.math_context._theorems_cache.items():
                domain = f" [{thm['domain']}]" if thm.get('domain') else ""
                result += f"- **{name}**{domain}: {thm['statement'][:100]}...\n"
            
            return result
        except Exception as e:
            return f"Erreur: {e}"
    
    def _list_my_definitions(self) -> str:
        """Liste les definitions en memoire."""
        try:
            stats = self.math_context.get_statistics()
            
            if stats["definitions"] == 0:
                return "Vous n'avez pas encore enregistre de definitions. Utilisez 'Definis [terme]: [definition]' pour en ajouter."
            
            result = f"**Vos definitions en memoire ({stats['definitions']}):**\n\n"
            
            for term, defn in self.math_context._definitions_cache.items():
                result += f"- **{term}**: {defn['definition'][:100]}...\n"
            
            return result
        except Exception as e:
            return f"Erreur: {e}"
    
    def _show_context(self) -> str:
        """Affiche le contexte mathematique complet."""
        try:
            stats = self.math_context.get_statistics()
            
            result = "**Votre contexte mathematique:**\n\n"
            result += f"- Theoremes: {stats['theorems']}\n"
            result += f"- Definitions: {stats['definitions']}\n"
            result += f"- Patterns de preuve: {stats['proof_patterns']}\n"
            
            if stats['domains']:
                result += f"- Domaines: {', '.join(stats['domains'])}\n"
            
            result += "\n**Commandes disponibles:**\n"
            result += "- 'Ajoute le theoreme [nom]: [enonce]'\n"
            result += "- 'Definis [terme]: [definition]'\n"
            result += "- 'Mes theoremes'\n"
            result += "- 'Mes definitions'\n"
            
            return result
        except Exception as e:
            return f"Erreur: {e}"
    
    async def _web_search(self, query: str) -> str:
        """Effectue une recherche web."""
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
            
            if not results:
                return "Aucun resultat trouve."
            
            formatted = "**Resultats de recherche:**\n\n"
            for i, r in enumerate(results, 1):
                formatted += f"{i}. **{r['title']}**\n"
                formatted += f"   {r['body'][:200]}...\n"
                formatted += f"   [Lien]({r['href']})\n\n"
            
            return formatted
            
        except Exception as e:
            logger.error(f"Erreur recherche web: {e}")
            return f"Erreur lors de la recherche: {str(e)}"
    
    def new_conversation(self):
        """Demarre une nouvelle conversation."""
        self.conversation_history = []
        logger.info("Nouvelle conversation demarree")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Retourne l'historique de la conversation."""
        return self.conversation_history
    
    def load_conversation(self, conversation_id: str) -> bool:
        """Charge une conversation depuis la memoire."""
        history = self.memory.load_conversation(conversation_id)
        if history:
            self.conversation_history = history
            return True
        return False
