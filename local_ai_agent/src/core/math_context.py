#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Contexte Mathematique
=====================================
Retient les theoremes, definitions et concepts mathematiques favoris
pour les reutiliser dans les conversations et preuves Isabelle.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import sqlite3
import re

logger = logging.getLogger(__name__)


class MathContext:
    """Gestionnaire de contexte mathematique persistant."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le gestionnaire de contexte.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        
        # Base de donnees
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "math_context.db"
        
        self._init_database()
        
        # Cache en memoire pour acces rapide
        self._theorems_cache: Dict[str, Dict] = {}
        self._definitions_cache: Dict[str, Dict] = {}
        self._load_cache()
        
        logger.info("Gestionnaire de contexte mathematique initialise")
    
    def _init_database(self):
        """Initialise la base de donnees."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des theoremes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS theorems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    statement TEXT NOT NULL,
                    proof TEXT,
                    isabelle_code TEXT,
                    domain TEXT,
                    tags TEXT,
                    notes TEXT,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des definitions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS definitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT UNIQUE NOT NULL,
                    definition TEXT NOT NULL,
                    formal_definition TEXT,
                    isabelle_code TEXT,
                    domain TEXT,
                    related_terms TEXT,
                    examples TEXT,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des concepts et relations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS concepts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    domain TEXT,
                    parent_concepts TEXT,
                    child_concepts TEXT,
                    related_theorems TEXT,
                    related_definitions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des preuves favorites
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proof_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    pattern_type TEXT,
                    description TEXT,
                    isabelle_template TEXT,
                    applicable_to TEXT,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des sessions de travail
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS work_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT,
                    active_theorems TEXT,
                    active_definitions TEXT,
                    current_goal TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def _load_cache(self):
        """Charge les donnees frequemment utilisees en cache."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Charger les theoremes les plus utilises
            cursor.execute("""
                SELECT name, statement, proof, isabelle_code, domain, tags
                FROM theorems
                ORDER BY usage_count DESC
                LIMIT 50
            """)
            
            for row in cursor.fetchall():
                self._theorems_cache[row[0]] = {
                    "name": row[0],
                    "statement": row[1],
                    "proof": row[2],
                    "isabelle_code": row[3],
                    "domain": row[4],
                    "tags": json.loads(row[5]) if row[5] else []
                }
            
            # Charger les definitions les plus utilisees
            cursor.execute("""
                SELECT term, definition, formal_definition, isabelle_code, domain
                FROM definitions
                ORDER BY usage_count DESC
                LIMIT 50
            """)
            
            for row in cursor.fetchall():
                self._definitions_cache[row[0]] = {
                    "term": row[0],
                    "definition": row[1],
                    "formal_definition": row[2],
                    "isabelle_code": row[3],
                    "domain": row[4]
                }
    
    # ==================== THEOREMES ====================
    
    def add_theorem(
        self,
        name: str,
        statement: str,
        proof: Optional[str] = None,
        isabelle_code: Optional[str] = None,
        domain: Optional[str] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Ajoute ou met a jour un theoreme.
        
        Args:
            name: Nom du theoreme
            statement: Enonce du theoreme
            proof: Preuve (optionnel)
            isabelle_code: Code Isabelle (optionnel)
            domain: Domaine mathematique
            tags: Tags pour la recherche
            notes: Notes personnelles
            
        Returns:
            True si ajoute avec succes
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO theorems 
                    (name, statement, proof, isabelle_code, domain, tags, notes, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    name, statement, proof, isabelle_code, domain,
                    json.dumps(tags or []), notes
                ))
                conn.commit()
            
            # Mettre a jour le cache
            self._theorems_cache[name] = {
                "name": name,
                "statement": statement,
                "proof": proof,
                "isabelle_code": isabelle_code,
                "domain": domain,
                "tags": tags or []
            }
            
            logger.info(f"Theoreme ajoute: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur ajout theoreme: {e}")
            return False
    
    def get_theorem(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Recupere un theoreme par son nom.
        
        Args:
            name: Nom du theoreme
            
        Returns:
            Dictionnaire du theoreme ou None
        """
        # Verifier le cache d'abord
        if name in self._theorems_cache:
            self._increment_usage("theorems", name)
            return self._theorems_cache[name]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, statement, proof, isabelle_code, domain, tags, notes
                FROM theorems WHERE name = ?
            """, (name,))
            
            row = cursor.fetchone()
            if row:
                self._increment_usage("theorems", name)
                return {
                    "name": row[0],
                    "statement": row[1],
                    "proof": row[2],
                    "isabelle_code": row[3],
                    "domain": row[4],
                    "tags": json.loads(row[5]) if row[5] else [],
                    "notes": row[6]
                }
        
        return None
    
    def search_theorems(
        self,
        query: str,
        domain: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recherche des theoremes.
        
        Args:
            query: Terme de recherche
            domain: Filtrer par domaine
            limit: Nombre max de resultats
            
        Returns:
            Liste des theoremes correspondants
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if domain:
                cursor.execute("""
                    SELECT name, statement, domain, tags
                    FROM theorems
                    WHERE (name LIKE ? OR statement LIKE ? OR tags LIKE ?)
                    AND domain = ?
                    ORDER BY usage_count DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", f"%{query}%", domain, limit))
            else:
                cursor.execute("""
                    SELECT name, statement, domain, tags
                    FROM theorems
                    WHERE name LIKE ? OR statement LIKE ? OR tags LIKE ?
                    ORDER BY usage_count DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", f"%{query}%", limit))
            
            return [
                {
                    "name": row[0],
                    "statement": row[1],
                    "domain": row[2],
                    "tags": json.loads(row[3]) if row[3] else []
                }
                for row in cursor.fetchall()
            ]
    
    def list_theorems_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Liste tous les theoremes d'un domaine."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, statement FROM theorems
                WHERE domain = ?
                ORDER BY name
            """, (domain,))
            
            return [{"name": row[0], "statement": row[1]} for row in cursor.fetchall()]
    
    # ==================== DEFINITIONS ====================
    
    def add_definition(
        self,
        term: str,
        definition: str,
        formal_definition: Optional[str] = None,
        isabelle_code: Optional[str] = None,
        domain: Optional[str] = None,
        related_terms: Optional[List[str]] = None,
        examples: Optional[List[str]] = None
    ) -> bool:
        """
        Ajoute ou met a jour une definition.
        
        Args:
            term: Terme a definir
            definition: Definition en langage naturel
            formal_definition: Definition formelle
            isabelle_code: Code Isabelle
            domain: Domaine mathematique
            related_terms: Termes lies
            examples: Exemples
            
        Returns:
            True si ajoute avec succes
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO definitions
                    (term, definition, formal_definition, isabelle_code, domain, 
                     related_terms, examples, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    term, definition, formal_definition, isabelle_code, domain,
                    json.dumps(related_terms or []),
                    json.dumps(examples or [])
                ))
                conn.commit()
            
            # Mettre a jour le cache
            self._definitions_cache[term] = {
                "term": term,
                "definition": definition,
                "formal_definition": formal_definition,
                "isabelle_code": isabelle_code,
                "domain": domain
            }
            
            logger.info(f"Definition ajoutee: {term}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur ajout definition: {e}")
            return False
    
    def get_definition(self, term: str) -> Optional[Dict[str, Any]]:
        """Recupere une definition par son terme."""
        if term in self._definitions_cache:
            self._increment_usage("definitions", term, "term")
            return self._definitions_cache[term]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT term, definition, formal_definition, isabelle_code, 
                       domain, related_terms, examples
                FROM definitions WHERE term = ?
            """, (term,))
            
            row = cursor.fetchone()
            if row:
                self._increment_usage("definitions", term, "term")
                return {
                    "term": row[0],
                    "definition": row[1],
                    "formal_definition": row[2],
                    "isabelle_code": row[3],
                    "domain": row[4],
                    "related_terms": json.loads(row[5]) if row[5] else [],
                    "examples": json.loads(row[6]) if row[6] else []
                }
        
        return None
    
    def search_definitions(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recherche des definitions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT term, definition, domain
                FROM definitions
                WHERE term LIKE ? OR definition LIKE ?
                ORDER BY usage_count DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            return [
                {"term": row[0], "definition": row[1], "domain": row[2]}
                for row in cursor.fetchall()
            ]
    
    # ==================== PATTERNS DE PREUVES ====================
    
    def add_proof_pattern(
        self,
        name: str,
        pattern_type: str,
        description: str,
        isabelle_template: str,
        applicable_to: Optional[List[str]] = None
    ) -> bool:
        """
        Ajoute un pattern de preuve reutilisable.
        
        Args:
            name: Nom du pattern
            pattern_type: Type (induction, contradiction, direct, etc.)
            description: Description du pattern
            isabelle_template: Template Isabelle avec placeholders
            applicable_to: Types de theoremes ou ca s'applique
            
        Returns:
            True si ajoute avec succes
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO proof_patterns
                    (name, pattern_type, description, isabelle_template, applicable_to)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    name, pattern_type, description, isabelle_template,
                    json.dumps(applicable_to or [])
                ))
                conn.commit()
            
            logger.info(f"Pattern de preuve ajoute: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur ajout pattern: {e}")
            return False
    
    def get_proof_patterns(self, pattern_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Recupere les patterns de preuves."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if pattern_type:
                cursor.execute("""
                    SELECT name, pattern_type, description, isabelle_template
                    FROM proof_patterns
                    WHERE pattern_type = ?
                    ORDER BY usage_count DESC
                """, (pattern_type,))
            else:
                cursor.execute("""
                    SELECT name, pattern_type, description, isabelle_template
                    FROM proof_patterns
                    ORDER BY usage_count DESC
                """)
            
            return [
                {
                    "name": row[0],
                    "type": row[1],
                    "description": row[2],
                    "template": row[3]
                }
                for row in cursor.fetchall()
            ]
    
    # ==================== CONTEXTE DE CONVERSATION ====================
    
    def get_relevant_context(self, message: str) -> Dict[str, Any]:
        """
        Extrait le contexte mathematique pertinent pour un message.
        
        Args:
            message: Message de l'utilisateur
            
        Returns:
            Contexte pertinent (theoremes, definitions, patterns)
        """
        context = {
            "theorems": [],
            "definitions": [],
            "patterns": [],
            "suggestions": []
        }
        
        # Detecter les termes mathematiques dans le message
        math_terms = self._extract_math_terms(message)
        
        for term in math_terms:
            # Chercher dans les theoremes
            theorems = self.search_theorems(term, limit=3)
            context["theorems"].extend(theorems)
            
            # Chercher dans les definitions
            definitions = self.search_definitions(term, limit=3)
            context["definitions"].extend(definitions)
        
        # Detecter le type de preuve necessaire
        if any(kw in message.lower() for kw in ["prouve", "demontre", "montrer"]):
            if "induction" in message.lower():
                context["patterns"] = self.get_proof_patterns("induction")
            elif "contradiction" in message.lower():
                context["patterns"] = self.get_proof_patterns("contradiction")
            else:
                context["patterns"] = self.get_proof_patterns()[:3]
        
        # Dedupliquer
        context["theorems"] = self._deduplicate(context["theorems"], "name")
        context["definitions"] = self._deduplicate(context["definitions"], "term")
        
        return context
    
    def _extract_math_terms(self, text: str) -> List[str]:
        """Extrait les termes mathematiques d'un texte."""
        # Termes connus
        known_terms = list(self._theorems_cache.keys()) + list(self._definitions_cache.keys())
        
        found = []
        text_lower = text.lower()
        
        for term in known_terms:
            if term.lower() in text_lower:
                found.append(term)
        
        # Detecter des patterns mathematiques communs
        math_patterns = [
            r'\b(theoreme|lemme|corollaire|proposition)\s+(?:de\s+)?(\w+)',
            r'\b(groupe|anneau|corps|espace|ensemble)\s+(\w+)',
            r'\b(fonction|application|morphisme|isomorphisme)\b',
            r'\b(nombre|entier|reel|complexe|premier)\b',
        ]
        
        for pattern in math_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    found.extend(match)
                else:
                    found.append(match)
        
        return list(set(found))
    
    def _deduplicate(self, items: List[Dict], key: str) -> List[Dict]:
        """Deduplique une liste de dictionnaires."""
        seen = set()
        result = []
        for item in items:
            if item.get(key) not in seen:
                seen.add(item.get(key))
                result.append(item)
        return result
    
    def _increment_usage(self, table: str, name: str, column: str = "name"):
        """Incremente le compteur d'usage."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE {table}
                    SET usage_count = usage_count + 1
                    WHERE {column} = ?
                """, (name,))
                conn.commit()
        except:
            pass
    
    # ==================== SESSIONS DE TRAVAIL ====================
    
    def create_session(self, name: str, goal: Optional[str] = None) -> int:
        """Cree une nouvelle session de travail."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO work_sessions (session_name, current_goal)
                VALUES (?, ?)
            """, (name, goal))
            conn.commit()
            return cursor.lastrowid
    
    def get_active_session(self) -> Optional[Dict[str, Any]]:
        """Recupere la session de travail la plus recente."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, session_name, active_theorems, active_definitions, 
                       current_goal, notes
                FROM work_sessions
                ORDER BY updated_at DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "theorems": json.loads(row[2]) if row[2] else [],
                    "definitions": json.loads(row[3]) if row[3] else [],
                    "goal": row[4],
                    "notes": row[5]
                }
        
        return None
    
    def update_session(
        self,
        session_id: int,
        theorems: Optional[List[str]] = None,
        definitions: Optional[List[str]] = None,
        goal: Optional[str] = None,
        notes: Optional[str] = None
    ):
        """Met a jour une session de travail."""
        updates = []
        values = []
        
        if theorems is not None:
            updates.append("active_theorems = ?")
            values.append(json.dumps(theorems))
        if definitions is not None:
            updates.append("active_definitions = ?")
            values.append(json.dumps(definitions))
        if goal is not None:
            updates.append("current_goal = ?")
            values.append(goal)
        if notes is not None:
            updates.append("notes = ?")
            values.append(notes)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(session_id)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    UPDATE work_sessions
                    SET {', '.join(updates)}
                    WHERE id = ?
                """, values)
                conn.commit()
    
    # ==================== EXPORT/IMPORT ====================
    
    def export_all(self, filepath: Path) -> bool:
        """Exporte tout le contexte mathematique."""
        try:
            data = {
                "theorems": [],
                "definitions": [],
                "proof_patterns": [],
                "exported_at": datetime.now().isoformat()
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM theorems")
                columns = [d[0] for d in cursor.description]
                data["theorems"] = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                cursor.execute("SELECT * FROM definitions")
                columns = [d[0] for d in cursor.description]
                data["definitions"] = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                cursor.execute("SELECT * FROM proof_patterns")
                columns = [d[0] for d in cursor.description]
                data["proof_patterns"] = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur export contexte: {e}")
            return False
    
    def import_data(self, filepath: Path) -> bool:
        """Importe des donnees de contexte."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for thm in data.get("theorems", []):
                self.add_theorem(
                    name=thm["name"],
                    statement=thm["statement"],
                    proof=thm.get("proof"),
                    isabelle_code=thm.get("isabelle_code"),
                    domain=thm.get("domain"),
                    tags=json.loads(thm["tags"]) if thm.get("tags") else None
                )
            
            for defn in data.get("definitions", []):
                self.add_definition(
                    term=defn["term"],
                    definition=defn["definition"],
                    formal_definition=defn.get("formal_definition"),
                    isabelle_code=defn.get("isabelle_code"),
                    domain=defn.get("domain")
                )
            
            self._load_cache()
            return True
            
        except Exception as e:
            logger.error(f"Erreur import contexte: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne des statistiques sur le contexte."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM theorems")
            num_theorems = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM definitions")
            num_definitions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM proof_patterns")
            num_patterns = cursor.fetchone()[0]
            
            cursor.execute("SELECT DISTINCT domain FROM theorems WHERE domain IS NOT NULL")
            domains = [row[0] for row in cursor.fetchall()]
        
        return {
            "theorems": num_theorems,
            "definitions": num_definitions,
            "proof_patterns": num_patterns,
            "domains": domains,
            "cached_theorems": len(self._theorems_cache),
            "cached_definitions": len(self._definitions_cache)
        }
