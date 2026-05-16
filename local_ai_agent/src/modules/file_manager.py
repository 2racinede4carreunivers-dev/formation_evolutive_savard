#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Gestion de Fichiers
==========================
Gere l'acces au systeme de fichiers.
"""

import os
import logging
import subprocess
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path
import mimetypes

logger = logging.getLogger(__name__)


class FileModule:
    """Module de gestion des fichiers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le module fichiers.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        self.work_dir = Path(os.environ.get("WORK_DIRECTORY", Path.home() / "Documents"))
        
        # Extensions supportees
        self.text_extensions = {'.txt', '.md', '.py', '.js', '.json', '.xml', '.csv', '.thy', '.tex'}
        self.doc_extensions = {'.docx', '.pdf', '.xlsx', '.pptx'}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        self.archive_extensions = {'.zip', '.tar', '.gz', '.rar', '.7z'}
        
        logger.info(f"Module fichiers initialise - Repertoire: {self.work_dir}")
    
    async def open_path(self, query: str) -> str:
        """
        Ouvre un fichier ou dossier.
        
        Args:
            query: Requete contenant le chemin
            
        Returns:
            Resultat de l'operation
        """
        path = self._extract_path(query)
        
        if not path:
            return "Je n'ai pas pu identifier le chemin. Precisez le dossier ou fichier."
        
        path = Path(path)
        
        # Resoudre les chemins relatifs
        if not path.is_absolute():
            path = self.work_dir / path
        
        if not path.exists():
            return f"Le chemin n'existe pas: `{path}`"
        
        if path.is_dir():
            return await self._list_directory(path)
        else:
            return await self._read_file(path)
    
    def _extract_path(self, query: str) -> Optional[str]:
        """
        Extrait un chemin d'une requete.
        
        Args:
            query: Requete en langage naturel
            
        Returns:
            Chemin extrait ou None
        """
        import re
        
        # Patterns de chemins
        patterns = [
            r'"([^"]+)"',  # Entre guillemets
            r"'([^']+)'",  # Entre apostrophes
            r"`([^`]+)`",  # Entre backticks
            r"([A-Za-z]:\\[^\s]+)",  # Chemin Windows
            r"(~/[^\s]+)",  # Chemin Unix home
            r"(/[^\s]+)",  # Chemin Unix absolu
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1)
        
        # Chercher apres des mots cles
        keywords = ["dossier", "fichier", "ouvre", "lis", "folder", "file"]
        for kw in keywords:
            if kw in query.lower():
                idx = query.lower().index(kw) + len(kw)
                remaining = query[idx:].strip()
                # Prendre le premier mot/chemin
                words = remaining.split()
                if words:
                    return words[0]
        
        return None
    
    async def _list_directory(self, path: Path) -> str:
        """
        Liste le contenu d'un repertoire.
        
        Args:
            path: Chemin du repertoire
            
        Returns:
            Liste formatee
        """
        try:
            items = list(path.iterdir())
            
            # Trier: dossiers d'abord, puis fichiers
            dirs = sorted([i for i in items if i.is_dir()], key=lambda x: x.name.lower())
            files = sorted([i for i in items if i.is_file()], key=lambda x: x.name.lower())
            
            result = f"**Contenu de `{path}`:**\n\n"
            
            if dirs:
                result += "**Dossiers:**\n"
                for d in dirs[:20]:  # Limiter a 20
                    result += f"  - 📁 {d.name}/\n"
                if len(dirs) > 20:
                    result += f"  ... et {len(dirs) - 20} autres dossiers\n"
                result += "\n"
            
            if files:
                result += "**Fichiers:**\n"
                for f in files[:30]:  # Limiter a 30
                    size = f.stat().st_size
                    size_str = self._format_size(size)
                    ext = f.suffix.lower()
                    icon = self._get_file_icon(ext)
                    result += f"  - {icon} {f.name} ({size_str})\n"
                if len(files) > 30:
                    result += f"  ... et {len(files) - 30} autres fichiers\n"
            
            if not dirs and not files:
                result += "*Dossier vide*\n"
            
            return result
            
        except PermissionError:
            return f"Permission refusee pour acceder a `{path}`"
        except Exception as e:
            logger.error(f"Erreur lecture dossier: {e}")
            return f"Erreur: {str(e)}"
    
    async def _read_file(self, path: Path) -> str:
        """
        Lit le contenu d'un fichier.
        
        Args:
            path: Chemin du fichier
            
        Returns:
            Contenu du fichier
        """
        ext = path.suffix.lower()
        
        try:
            if ext in self.text_extensions:
                return await self._read_text_file(path)
            elif ext == '.pdf':
                return await self._read_pdf(path)
            elif ext == '.docx':
                return await self._read_docx(path)
            elif ext in self.image_extensions:
                return f"**Image:** `{path.name}`\n\nTaille: {self._format_size(path.stat().st_size)}\n\n*Pour afficher l'image, ouvrez-la avec votre visionneuse.*"
            else:
                return f"Format de fichier non supporte: `{ext}`"
                
        except Exception as e:
            logger.error(f"Erreur lecture fichier: {e}")
            return f"Erreur lors de la lecture: {str(e)}"
    
    async def _read_text_file(self, path: Path) -> str:
        """
        Lit un fichier texte.
        
        Args:
            path: Chemin du fichier
            
        Returns:
            Contenu du fichier
        """
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                content = path.read_text(encoding=encoding)
                
                # Limiter la taille affichee
                if len(content) > 10000:
                    content = content[:10000] + "\n\n... [contenu tronque]"
                
                ext = path.suffix.lower()
                lang = {
                    '.py': 'python',
                    '.js': 'javascript',
                    '.json': 'json',
                    '.thy': 'isabelle',
                    '.tex': 'latex',
                    '.md': 'markdown'
                }.get(ext, '')
                
                return f"**Fichier:** `{path.name}`\n\n```{lang}\n{content}\n```"
                
            except UnicodeDecodeError:
                continue
        
        return "Impossible de decoder le fichier avec les encodages disponibles."
    
    async def _read_pdf(self, path: Path) -> str:
        """
        Lit un fichier PDF.
        
        Args:
            path: Chemin du fichier
            
        Returns:
            Texte extrait
        """
        try:
            import PyPDF2
            
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                
                text = ""
                for i, page in enumerate(reader.pages[:10]):  # Limiter a 10 pages
                    text += f"\n--- Page {i+1} ---\n"
                    text += page.extract_text() or "[Pas de texte extractible]"
                
                if num_pages > 10:
                    text += f"\n\n... [{num_pages - 10} pages supplementaires]"
                
                return f"**PDF:** `{path.name}` ({num_pages} pages)\n\n{text}"
                
        except Exception as e:
            return f"Erreur lecture PDF: {str(e)}"
    
    async def _read_docx(self, path: Path) -> str:
        """
        Lit un fichier Word.
        
        Args:
            path: Chemin du fichier
            
        Returns:
            Texte extrait
        """
        try:
            from docx import Document
            
            doc = Document(path)
            text = "\n".join([p.text for p in doc.paragraphs])
            
            if len(text) > 10000:
                text = text[:10000] + "\n\n... [contenu tronque]"
            
            return f"**Document Word:** `{path.name}`\n\n{text}"
            
        except Exception as e:
            return f"Erreur lecture Word: {str(e)}"
    
    async def create_file(self, query: str) -> str:
        """
        Cree ou modifie un fichier.
        
        Args:
            query: Requete avec le contenu
            
        Returns:
            Resultat de l'operation
        """
        # Cette methode necessite une confirmation
        return "Creation de fichier - fonctionnalite a implementer avec confirmation utilisateur."
    
    async def search_files(self, query: str, directory: Optional[Path] = None) -> str:
        """
        Recherche des fichiers.
        
        Args:
            query: Terme de recherche
            directory: Repertoire de recherche
            
        Returns:
            Resultats de la recherche
        """
        search_dir = directory or self.work_dir
        
        try:
            results = []
            for item in search_dir.rglob(f"*{query}*"):
                if len(results) >= 50:
                    break
                results.append(item)
            
            if not results:
                return f"Aucun fichier trouve correspondant a '{query}'"
            
            output = f"**Resultats de recherche pour '{query}':**\n\n"
            for r in results:
                rel_path = r.relative_to(search_dir) if r.is_relative_to(search_dir) else r
                icon = "📁" if r.is_dir() else self._get_file_icon(r.suffix)
                output += f"  - {icon} `{rel_path}`\n"
            
            return output
            
        except Exception as e:
            return f"Erreur de recherche: {str(e)}"
    
    def _format_size(self, size: int) -> str:
        """Formate une taille en bytes."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def _get_file_icon(self, ext: str) -> str:
        """Retourne une icone pour l'extension."""
        ext = ext.lower()
        icons = {
            '.py': '🐍',
            '.js': '📜',
            '.json': '📋',
            '.txt': '📝',
            '.md': '📖',
            '.pdf': '📕',
            '.docx': '📘',
            '.xlsx': '📊',
            '.pptx': '📽️',
            '.thy': '🔬',
            '.tex': '📐',
            '.jpg': '🖼️',
            '.png': '🖼️',
            '.zip': '📦',
        }
        return icons.get(ext, '📄')
