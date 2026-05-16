#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent IA Local Mathematique - Mode CLI
======================================
Interface en ligne de commande pour Docker
Inclut le systeme de securite proprietaire
Test spectral + logique HOL via modules.test_spectral
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

# -------------------------------------------------------------------
#  CHEMINS DE BASE
# -------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# -------------------------------------------------------------------
#  IMPORT MODULE ISABELLE (interface_isabelle.py)
# -------------------------------------------------------------------
CORPUS_ACTIONS_DIR = ROOT_DIR / "corpus_actions"
if str(CORPUS_ACTIONS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_ACTIONS_DIR))

console = Console()

try:
    from interface_isabelle import IsabelleInterface
    ISABELLE_AVAILABLE = True
except Exception as e:
    console.print(f"[yellow]Module Isabelle indisponible: {e}[/yellow]")
    ISABELLE_AVAILABLE = False

# -------------------------------------------------------------------
#  IMPORT MODULE SPECTRAL (HOL + Zêta)
# -------------------------------------------------------------------
try:
    from modules.test_spectral import (
        run_spectral_test,
        test_zeta_value,
    )
    SPECTRAL_AVAILABLE = True
except Exception as e:
    console.print(
        f"[yellow]Module spectral indisponible (modules.test_spectral): {e}[/yellow]"
    )
    SPECTRAL_AVAILABLE = False

# -------------------------------------------------------------------
#  BANNIÈRE PERSONNALISÉE : Fonction Zêta de Philippôt
# -------------------------------------------------------------------
def afficher_banniere():
    console.print(
        r"""
███████╗ ██████╗ ███╗   ██╗ ██████╗████████╗██╗ ██████╗ ██████╗ 
██╔════╝██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗██╔══██╗
█████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██████╔╝
██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██╔══██╗
██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═╝

              ███████╗███████╗████████╗ █████╗ 
              ██╔════╝██╔════╝╚══██╔══╝██╔══██╗
              █████╗  ███████╗   ██║   ███████║
              ██╔══╝  ╚════██║   ██║   ██╔══██║
              ███████╗███████║   ██║   ██║  ██║
              ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝

                 *** Fonction Zêta de Philippôt ***
      Hypercube 4D • Rotation Spectrale • Projection Orthogonale
"""
    )

# -------------------------------------------------------------------
#  LOGGING
# -------------------------------------------------------------------
def setup_logging() -> logging.Logger:
    """Configure le logging."""
    log_dir = ROOT_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "agent_cli.log", encoding="utf-8"),
        ],
    )
    return logging.getLogger("math-agent-cli")

# -------------------------------------------------------------------
#  ENVIRONNEMENT
# -------------------------------------------------------------------
def check_env():
    """Charge et verifie l'environnement."""
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    console.print(f"[dim]Ollama: {ollama_host}[/dim]")

# -------------------------------------------------------------------
#  MESSAGE DE BIENVENUE
# -------------------------------------------------------------------
def print_welcome():
    """Affiche le message de bienvenue."""
    welcome = """
# Agent IA Mathematique - Mode CLI

Bienvenue! Je suis votre assistant mathematique.

## Commandes disponibles:
- **Calculs**: "Resous x^2 + 5x + 6 = 0"
- **Theoremes**: "Ajoute le theoreme [nom]: [enonce]"
- **Definitions**: "Definis [terme]: [definition]"
- **Contexte**: "Mes theoremes", "Mes definitions"
- **Securite**: "statut securite"
- **Test Spectral**: "test_agent_local"
- **Test Zêta**: "test zeta n P"
- **Isabelle**:
    - `/isabelle_check <fichier.thy>`
    - `/isabelle_safe_update <fichier.thy> <section> <nouveau_texte>`
- **Aide**: "aide" ou "help"
- **Quitter**: "quit" ou "exit"
"""
    console.print(
        Panel(
            Markdown(welcome),
            title="[bold blue]Math Agent[/bold blue]",
            border_style="blue",
        )
    )

# -------------------------------------------------------------------
#  BANNIÈRE DE SÉCURITÉ
# -------------------------------------------------------------------
def print_security_banner(agent):
    """Affiche la banniere de securite si disponible."""
    if not agent or not hasattr(agent, "security"):
        return

    try:
        if agent.security.is_owner_mode:
            remaining = agent.security.get_remaining_time()
            console.print(
                f"[green][ PROPRIETAIRE | Auto-lock: {remaining // 60}m {remaining % 60}s ][/green]"
            )
        else:
            console.print("[yellow][ MODE INVITE - Acces limite ][/yellow]")
    except Exception:
        console.print("[yellow][ Statut securite indisponible ][/yellow]")

# -------------------------------------------------------------------
#  INITIALISATION DE L'AGENT
# -------------------------------------------------------------------
def init_agent(logger: logging.Logger):
    """Initialise MathAgent a partir de config.yaml."""
    try:
        from core.agent import MathAgent
        import yaml

        config_path = ROOT_DIR / "config.yaml"
        config = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}

        agent = MathAgent(config)
        console.print("[green]Agent initialise avec succes![/green]")
        console.print("[yellow]Mode securite: INVITE (acces limite)[/yellow]\n")
        return agent

    except Exception as e:
        console.print(f"[red]Erreur d'initialisation: {e}[/red]")
        console.print("[yellow]L'agent fonctionnera en mode limite.[/yellow]\n")
        logger.error(f"Erreur init: {e}", exc_info=True)
        return None

# -------------------------------------------------------------------
#  BOUCLE PRINCIPALE CLI
# -------------------------------------------------------------------
async def main():
    """Point d'entree principal CLI."""
    logger = setup_logging()
    logger.info("Demarrage du mode CLI")

    afficher_banniere()
    console.print(
        "\n[bold blue]Initialisation de l'Agent IA Mathematique...[/bold blue]\n"
    )

    check_env()
    agent = init_agent(logger)
    print_welcome()

    # Historique des commandes
    history_file = ROOT_DIR / "data" / ".cli_history"
    history_file.parent.mkdir(exist_ok=True)
    session = PromptSession(history=FileHistory(str(history_file)))

    loop = asyncio.get_event_loop()

    while True:
        try:
            # Statut securite
            if agent:
                print_security_banner(agent)

            # Prompt utilisateur
            user_input = await loop.run_in_executor(
                None, lambda: session.prompt("\n[Vous] > ")
            )
            user_input = user_input.strip()

            if not user_input:
                continue

            lower = user_input.lower()

            # ---------------------------------------------------------
            #  COMMANDES GLOBALES
            # ---------------------------------------------------------
            if lower in ("quit", "exit", "q"):
                console.print("\n[blue]Au revoir![/blue]")
                break

            if lower in ("aide", "help", "?"):
                print_welcome()
                continue

            if lower == "clear":
                console.clear()
                continue

            # ---------------------------------------------------------
            #  COMMANDES ISABELLE
            # ---------------------------------------------------------
            if lower.startswith("/isabelle_check"):
                if not ISABELLE_AVAILABLE:
                    console.print("[red]Module Isabelle non disponible.[/red]")
                    continue

                parts = user_input.split(maxsplit=1)
                if len(parts) != 2:
                    console.print("[red]Usage: /isabelle_check <chemin_fichier.thy>[/red]")
                    continue

                file_path = parts[1].strip()
                full_path = ROOT_DIR / file_path

                if not full_path.exists():
                    console.print(f"[red]Fichier introuvable: {full_path}[/red]")
                    continue

                console.print(f"[cyan]Vérification Isabelle de {file_path}...[/cyan]")
                success, output = IsabelleInterface.check_file(str(full_path))

                if success:
                    console.print("[green]✔ Isabelle compile sans erreur.[/green]")
                else:
                    console.print("[red]❌ Isabelle a détecté des erreurs :[/red]")

                console.print(Markdown(f"```\n{output}\n```"))
                continue

            if lower.startswith("/isabelle_safe_update"):
                if not ISABELLE_AVAILABLE:
                    console.print("[red]Module Isabelle non disponible.[/red]")
                    continue

                parts = user_input.split(maxsplit=3)
                if len(parts) < 4:
                    console.print("[red]Usage: /isabelle_safe_update <fichier.thy> <section> <nouveau_texte>[/red]")
                    continue

                _, file_path, section_name, new_text = parts
                full_path = ROOT_DIR / file_path

                if not full_path.exists():
                    console.print(f"[red]Fichier introuvable: {full_path}[/red]")
                    continue

                # Lire le fichier original
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if section_name not in content:
                    console.print(f"[red]Section '{section_name}' introuvable dans {file_path}[/red]")
                    continue

                updated = content.replace(section_name, new_text)

                console.print(f"[cyan]Test de mise à jour sécurisée avec Isabelle...[/cyan]")
                success, message = IsabelleInterface.safe_update(str(full_path), updated)

                if success:
                    console.print("[green]✔ Mise à jour réussie ![/green]")
                else:
                    console.print("[red]❌ Isabelle a détecté une erreur :[/red]")

                console.print(Markdown(f"```\n{message}\n```"))
                continue

# ---------------------------------------------------------
            #  COMMANDES ISABELLE AVANCÉES
            # ---------------------------------------------------------
            if lower.startswith("/isabelle_update_section_auto"):
                parts = user_input.split(maxsplit=3)
                if len(parts) < 4:
                    console.print("[red]Usage: /isabelle_update_section_auto <fichier.thy> <section> <texte_section>[/red]")
                    continue

                _, file_path, section_name, section_text = parts
                full_path = ROOT_DIR / file_path

                ok, msg = IsabelleAuto.auto_update_section(str(full_path), section_name, agent)
                console.print(Markdown(f"```\n{msg}\n```"))
                continue

            if lower.startswith("/isabelle_fix_errors"):
                parts = user_input.split(maxsplit=1)
                if len(parts) != 2:
                    console.print("[red]Usage: /isabelle_fix_errors <fichier.thy>[/red]")
                    continue

                file_path = parts[1]
                full_path = ROOT_DIR / file_path

                ok, msg = IsabelleAuto.auto_fix_errors(str(full_path), agent)
                console.print(Markdown(f"```\n{msg}\n```"))
                continue

            if lower.startswith("/isabelle_generate_proof"):
                parts = user_input.split(maxsplit=1)
                if len(parts) != 2:
                    console.print("[red]Usage: /isabelle_generate_proof <fichier.thy>[/red]")
                    continue

                file_path = parts[1]
                full_path = ROOT_DIR / file_path

                ok, msg = IsabelleAuto.auto_generate_proofs(str(full_path), agent)
                console.print(Markdown(f"```\n{msg}\n```"))
                continue

            if lower.startswith("/isabelle_explain_error"):
                parts = user_input.split(maxsplit=1)
                if len(parts) != 2:
                    console.print("[red]Usage: /isabelle_explain_error <message>[/red]")
                    continue

                explanation = IsabelleAuto.explain_error(parts[1], agent)
                console.print(Markdown(explanation))
                continue

            # ---------------------------------------------------------
            #  COMMANDE : /isabelle_auto_all
            # ---------------------------------------------------------
            if lower.startswith("/isabelle_auto_all"):
                parts = user_input.split(maxsplit=4)
                if len(parts) < 5:
                    console.print("[red]Usage: /isabelle_auto_all <fichier.thy> <section> <texte_section>[/red]")
                    continue

                _, file_path, section_name, section_text = parts[0:4]
                full_path = ROOT_DIR / file_path

                if not full_path.exists():
                    console.print(f"[red]Fichier introuvable: {full_path}[/red]")
                    continue

                console.print("[cyan]Exécution du pipeline complet Isabelle...[/cyan]")

                ok, msg = IsabelleAuto.auto_all(str(full_path), section_name, section_text, agent)

                if ok:
                    console.print("[green]✔ Pipeline complet réussi ![/green]")
                else:
                    console.print("[red]❌ Pipeline échoué[/red]")

                console.print(Markdown(f"```\n{msg}\n```"))
                continue


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[blue]Au revoir![/blue]")
