#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module GitHub
=============
Gere les interactions avec GitHub.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)


class GitHubModule:
    """Module de gestion GitHub."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le module GitHub.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        
        self.token = os.environ.get("GITHUB_TOKEN", "")
        self.username = os.environ.get("GITHUB_USERNAME", "")
        
        self._configured = bool(self.token and self.username)
        
        # Client GitHub (charge a la demande)
        self._github = None
        
        logger.info(f"Module GitHub initialise - Configure: {self._configured}")
    
    @property
    def github(self):
        """Client GitHub (lazy loading)."""
        if self._github is None and self._configured:
            try:
                from github import Github
                self._github = Github(self.token)
            except Exception as e:
                logger.error(f"Erreur initialisation GitHub: {e}")
        return self._github
    
    async def execute(self, query: str) -> str:
        """
        Execute une action GitHub.
        
        Args:
            query: Commande ou action
            
        Returns:
            Resultat de l'action
        """
        query_lower = query.lower()
        
        if "clone" in query_lower:
            return await self._clone_repo(query)
        elif "push" in query_lower:
            return await self._push(query)
        elif "pull" in query_lower:
            return await self._pull(query)
        elif "commit" in query_lower:
            return await self._commit(query)
        elif "status" in query_lower:
            return await self._status(query)
        elif "liste" in query_lower or "repos" in query_lower:
            return await self._list_repos()
        else:
            return "Action GitHub non reconnue. Commandes disponibles: clone, push, pull, commit, status, liste repos"
    
    async def _clone_repo(self, query: str) -> str:
        """
        Clone un repository.
        
        Args:
            query: Requete contenant l'URL ou le nom du repo
            
        Returns:
            Resultat du clone
        """
        import re
        
        # Extraire l'URL ou le nom du repo
        url_match = re.search(r'(https://github\.com/[\w\-]+/[\w\-]+)', query)
        repo_match = re.search(r'([\w\-]+/[\w\-]+)', query)
        
        if url_match:
            repo_url = url_match.group(1)
        elif repo_match:
            repo_url = f"https://github.com/{repo_match.group(1)}"
        else:
            return "Je n'ai pas pu identifier le repository. Donnez l'URL ou le nom (user/repo)."
        
        # Determiner le dossier de destination
        repo_name = repo_url.split('/')[-1]
        dest_dir = Path(os.environ.get("WORK_DIRECTORY", Path.home() / "Documents")) / "GitHub" / repo_name
        
        if dest_dir.exists():
            return f"Le dossier `{dest_dir}` existe deja."
        
        try:
            dest_dir.parent.mkdir(parents=True, exist_ok=True)
            
            result = subprocess.run(
                ["git", "clone", repo_url, str(dest_dir)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return f"**Repository clone avec succes!**\n\nEmplacement: `{dest_dir}`"
            else:
                return f"Erreur lors du clone:\n```\n{result.stderr}\n```"
                
        except subprocess.TimeoutExpired:
            return "Timeout: Le clone a pris trop de temps."
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    async def _push(self, query: str) -> str:
        """
        Push les changements.
        
        Args:
            query: Requete avec le chemin du repo
            
        Returns:
            Resultat du push
        """
        repo_path = self._find_repo_path(query)
        
        if not repo_path:
            return "Je n'ai pas trouve de repository Git. Precisez le chemin."
        
        try:
            # D'abord commit si necessaire
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if status.stdout.strip():
                return "Il y a des changements non commites. Faites d'abord un commit."
            
            # Push
            result = subprocess.run(
                ["git", "push"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return f"**Push reussi!**\n\n```\n{result.stdout or 'Everything up-to-date'}\n```"
            else:
                return f"Erreur lors du push:\n```\n{result.stderr}\n```"
                
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    async def _pull(self, query: str) -> str:
        """
        Pull les changements.
        
        Args:
            query: Requete avec le chemin du repo
            
        Returns:
            Resultat du pull
        """
        repo_path = self._find_repo_path(query)
        
        if not repo_path:
            return "Je n'ai pas trouve de repository Git. Precisez le chemin."
        
        try:
            result = subprocess.run(
                ["git", "pull"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return f"**Pull reussi!**\n\n```\n{result.stdout or 'Already up to date'}\n```"
            else:
                return f"Erreur lors du pull:\n```\n{result.stderr}\n```"
                
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    async def _commit(self, query: str) -> str:
        """
        Commit les changements.
        
        Args:
            query: Requete avec le message de commit
            
        Returns:
            Resultat du commit
        """
        repo_path = self._find_repo_path(query)
        
        if not repo_path:
            return "Je n'ai pas trouve de repository Git. Precisez le chemin."
        
        # Extraire le message de commit
        import re
        msg_match = re.search(r'["\']([^"\']+)["\']', query)
        commit_msg = msg_match.group(1) if msg_match else "Update via Agent IA"
        
        try:
            # Add all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=repo_path,
                capture_output=True
            )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return f"**Commit reussi!**\n\nMessage: {commit_msg}\n\n```\n{result.stdout}\n```"
            elif "nothing to commit" in result.stdout.lower():
                return "Rien a commiter. Le repertoire de travail est propre."
            else:
                return f"Erreur lors du commit:\n```\n{result.stderr}\n```"
                
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    async def _status(self, query: str) -> str:
        """
        Affiche le statut du repo.
        
        Args:
            query: Requete avec le chemin du repo
            
        Returns:
            Statut du repo
        """
        repo_path = self._find_repo_path(query)
        
        if not repo_path:
            return "Je n'ai pas trouve de repository Git. Precisez le chemin."
        
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            return f"**Statut de `{repo_path.name}`:**\n\n```\n{result.stdout}\n```"
            
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    async def _list_repos(self) -> str:
        """Liste les repositories de l'utilisateur."""
        if not self._configured or not self.github:
            return "GitHub non configure. Ajoutez GITHUB_TOKEN et GITHUB_USERNAME dans .env"
        
        try:
            user = self.github.get_user()
            repos = list(user.get_repos())[:20]  # Limiter a 20
            
            result = f"**Vos repositories ({len(repos)} affiches):**\n\n"
            
            for repo in repos:
                visibility = "🔒" if repo.private else "🌐"
                result += f"  - {visibility} **{repo.name}**"
                if repo.description:
                    result += f" - {repo.description[:50]}"
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Erreur lors de la recuperation des repos: {str(e)}"
    
    def _find_repo_path(self, query: str) -> Optional[Path]:
        """
        Trouve le chemin d'un repository Git.
        
        Args:
            query: Requete contenant potentiellement le chemin
            
        Returns:
            Chemin du repo ou None
        """
        import re
        
        # Extraire un chemin de la requete
        path_patterns = [
            r'"([^"]+)"',
            r"'([^']+)'",
            r"([A-Za-z]:\\[^\s]+)",
            r"(~/[^\s]+)",
        ]
        
        for pattern in path_patterns:
            match = re.search(pattern, query)
            if match:
                path = Path(match.group(1)).expanduser()
                if (path / ".git").exists():
                    return path
        
        # Chercher dans le dossier de travail
        work_dir = Path(os.environ.get("WORK_DIRECTORY", Path.home() / "Documents"))
        github_dir = work_dir / "GitHub"
        
        if github_dir.exists():
            # Prendre le premier repo trouve
            for item in github_dir.iterdir():
                if item.is_dir() and (item / ".git").exists():
                    return item
        
        return None
