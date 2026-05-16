#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Memoire
=======================
Gere la persistance des conversations et des preferences.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import sqlite3
import hashlib

logger = logging.getLogger(__name__)


class MemoryManager:
    """Gestionnaire de memoire persistante."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le gestionnaire de memoire.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        
        # Repertoire de donnees
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Base de donnees SQLite
        self.db_path = self.data_dir / "memory.db"
        self._init_database()
        
        # Cache des preferences
        self._preferences_cache: Dict[str, Any] = {}
        self._load_preferences()
        
        logger.info("Gestionnaire de memoire initialise")
    
    def _init_database(self):
        """Initialise la base de donnees SQLite."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des conversations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    messages TEXT
                )
            """)
            
            # Table des preferences
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des patterns appris
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT,
                    pattern_data TEXT,
                    frequency INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def save_conversation(
        self,
        messages: List[Dict[str, str]],
        conversation_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> str:
        """
        Sauvegarde une conversation.
        
        Args:
            messages: Liste des messages
            conversation_id: ID existant ou None pour nouveau
            title: Titre de la conversation
            
        Returns:
            ID de la conversation
        """
        if not conversation_id:
            # Generer un nouvel ID
            content = json.dumps(messages[:2]) if messages else ""
            conversation_id = hashlib.md5(
                f"{datetime.now().isoformat()}{content}".encode()
            ).hexdigest()[:16]
        
        if not title and messages:
            # Generer un titre depuis le premier message
            first_msg = messages[0].get("content", "")[:50]
            title = first_msg + "..." if len(first_msg) >= 50 else first_msg
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO conversations (id, title, updated_at, messages)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?)
            """, (conversation_id, title, json.dumps(messages)))
            conn.commit()
        
        logger.debug(f"Conversation sauvegardee: {conversation_id}")
        return conversation_id
    
    def load_conversation(self, conversation_id: str) -> Optional[List[Dict[str, str]]]:
        """
        Charge une conversation.
        
        Args:
            conversation_id: ID de la conversation
            
        Returns:
            Liste des messages ou None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT messages FROM conversations WHERE id = ?",
                (conversation_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return json.loads(row[0])
        
        return None
    
    def list_conversations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Liste les conversations recentes.
        
        Args:
            limit: Nombre max de conversations
            
        Returns:
            Liste des conversations (id, title, date)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, created_at, updated_at
                FROM conversations
                ORDER BY updated_at DESC
                LIMIT ?
            """, (limit,))
            
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3]
                }
                for row in cursor.fetchall()
            ]
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Supprime une conversation.
        
        Args:
            conversation_id: ID de la conversation
            
        Returns:
            True si supprimee
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM conversations WHERE id = ?",
                (conversation_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def _load_preferences(self):
        """Charge les preferences en cache."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM preferences")
            
            for row in cursor.fetchall():
                try:
                    self._preferences_cache[row[0]] = json.loads(row[1])
                except:
                    self._preferences_cache[row[0]] = row[1]
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Recupere une preference.
        
        Args:
            key: Cle de la preference
            default: Valeur par defaut
            
        Returns:
            Valeur de la preference
        """
        return self._preferences_cache.get(key, default)
    
    def set_preference(self, key: str, value: Any):
        """
        Definit une preference.
        
        Args:
            key: Cle de la preference
            value: Valeur a stocker
        """
        self._preferences_cache[key] = value
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO preferences (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, json.dumps(value)))
            conn.commit()
    
    def learn_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]):
        """
        Enregistre un pattern d'utilisation.
        
        Args:
            pattern_type: Type de pattern (commande, preference, etc.)
            pattern_data: Donnees du pattern
        """
        data_str = json.dumps(pattern_data, sort_keys=True)
        data_hash = hashlib.md5(f"{pattern_type}{data_str}".encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verifier si le pattern existe
            cursor.execute("""
                SELECT id, frequency FROM patterns
                WHERE pattern_type = ? AND pattern_data = ?
            """, (pattern_type, data_str))
            
            row = cursor.fetchone()
            
            if row:
                # Incrementer la frequence
                cursor.execute(
                    "UPDATE patterns SET frequency = ? WHERE id = ?",
                    (row[1] + 1, row[0])
                )
            else:
                # Creer nouveau pattern
                cursor.execute("""
                    INSERT INTO patterns (pattern_type, pattern_data)
                    VALUES (?, ?)
                """, (pattern_type, data_str))
            
            conn.commit()
    
    def get_frequent_patterns(
        self,
        pattern_type: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recupere les patterns frequents.
        
        Args:
            pattern_type: Type de pattern
            limit: Nombre max de patterns
            
        Returns:
            Liste des patterns
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pattern_data, frequency
                FROM patterns
                WHERE pattern_type = ?
                ORDER BY frequency DESC
                LIMIT ?
            """, (pattern_type, limit))
            
            return [
                {
                    "data": json.loads(row[0]),
                    "frequency": row[1]
                }
                for row in cursor.fetchall()
            ]
    
    def search_conversations(self, query: str) -> List[Dict[str, Any]]:
        """
        Recherche dans les conversations.
        
        Args:
            query: Terme de recherche
            
        Returns:
            Conversations correspondantes
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, created_at
                FROM conversations
                WHERE title LIKE ? OR messages LIKE ?
                ORDER BY updated_at DESC
                LIMIT 20
            """, (f"%{query}%", f"%{query}%"))
            
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2]
                }
                for row in cursor.fetchall()
            ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur la memoire.
        
        Returns:
            Dictionnaire de statistiques
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM conversations")
            num_conversations = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM patterns")
            num_patterns = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM preferences")
            num_preferences = cursor.fetchone()[0]
        
        return {
            "conversations": num_conversations,
            "patterns": num_patterns,
            "preferences": num_preferences,
            "database_size_mb": round(self.db_path.stat().st_size / 1024 / 1024, 2)
        }
    
    def export_data(self, export_path: Path) -> bool:
        """
        Exporte toutes les donnees.
        
        Args:
            export_path: Chemin du fichier d'export
            
        Returns:
            True si exporte avec succes
        """
        try:
            data = {
                "conversations": [],
                "preferences": self._preferences_cache,
                "patterns": [],
                "exported_at": datetime.now().isoformat()
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM conversations")
                for row in cursor.fetchall():
                    data["conversations"].append({
                        "id": row[0],
                        "title": row[1],
                        "created_at": row[2],
                        "updated_at": row[3],
                        "messages": json.loads(row[4])
                    })
                
                cursor.execute("SELECT * FROM patterns")
                for row in cursor.fetchall():
                    data["patterns"].append({
                        "id": row[0],
                        "type": row[1],
                        "data": json.loads(row[2]),
                        "frequency": row[3]
                    })
            
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur export: {e}")
            return False
