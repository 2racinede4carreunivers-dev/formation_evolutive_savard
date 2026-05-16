#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire LLM
================
Gere les interactions avec les modeles de langage (Ollama et OpenAI).
"""

import os
import logging
from typing import Dict, Any, List, Optional
import asyncio

logger = logging.getLogger(__name__)


class LLMManager:
    """Gestionnaire des modeles de langage."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le gestionnaire LLM.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        self.ollama_available = False
        self.openai_available = False
        
        # Configuration Ollama
        self.ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2")
        
        # Configuration OpenAI
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")
        self.openai_model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        
        # Verifier la disponibilite
        self._check_availability()
    
    def _check_availability(self):
        """Verifie la disponibilite des providers LLM."""
        # Verifier Ollama
        try:
            import ollama
            ollama.list()
            self.ollama_available = True
            logger.info(f"Ollama disponible avec le modele: {self.ollama_model}")
        except Exception as e:
            logger.warning(f"Ollama non disponible: {e}")
            self.ollama_available = False
        
        # Verifier OpenAI
        if self.openai_key and self.openai_key.startswith("sk-"):
            self.openai_available = True
            logger.info("OpenAI API disponible")
        else:
            logger.warning("Cle OpenAI non configuree ou invalide")
            self.openai_available = False
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        use_openai: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """
        Envoie une requete de chat au LLM.
        
        Args:
            messages: Liste de messages (role, content)
            use_openai: Forcer l'utilisation d'OpenAI
            temperature: Temperature de generation
            max_tokens: Nombre max de tokens
            
        Returns:
            Reponse du modele
        """
        # Determiner le provider a utiliser
        if use_openai and self.openai_available:
            return await self._chat_openai(messages, temperature, max_tokens)
        elif self.ollama_available:
            return await self._chat_ollama(messages, temperature)
        elif self.openai_available:
            return await self._chat_openai(messages, temperature, max_tokens)
        else:
            raise RuntimeError("Aucun provider LLM disponible!")
    
    async def _chat_ollama(
        self,
        messages: List[Dict[str, str]],
        temperature: float
    ) -> str:
        """
        Chat avec Ollama (local).
        
        Args:
            messages: Liste de messages
            temperature: Temperature de generation
            
        Returns:
            Reponse du modele
        """
        try:
            import ollama
            
            # Ollama est synchrone, donc on l'execute dans un thread
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: ollama.chat(
                    model=self.ollama_model,
                    messages=messages,
                    options={"temperature": temperature}
                )
            )
            
            return response["message"]["content"]
            
        except Exception as e:
            logger.error(f"Erreur Ollama: {e}")
            
            # Fallback vers OpenAI si disponible
            if self.openai_available:
                logger.info("Fallback vers OpenAI")
                return await self._chat_openai(messages, temperature, 4096)
            
            raise
    
    async def _chat_openai(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        Chat avec OpenAI.
        
        Args:
            messages: Liste de messages
            temperature: Temperature de generation
            max_tokens: Nombre max de tokens
            
        Returns:
            Reponse du modele
        """
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.openai_key)
            
            response = await client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erreur OpenAI: {e}")
            
            # Fallback vers Ollama si disponible
            if self.ollama_available:
                logger.info("Fallback OpenAI -> Ollama local")
                return await self._chat_ollama(messages, temperature)
            
            raise
    
    async def generate(
        self,
        prompt: str,
        use_openai: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """
        Generation de texte simple (sans historique).
        
        Args:
            prompt: Prompt de generation
            use_openai: Forcer l'utilisation d'OpenAI
            temperature: Temperature de generation
            max_tokens: Nombre max de tokens
            
        Returns:
            Texte genere
        """
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, use_openai, temperature, max_tokens)
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estime le nombre de tokens dans un texte.
        
        Args:
            text: Texte a analyser
            
        Returns:
            Estimation du nombre de tokens
        """
        # Estimation simple: ~4 caracteres par token en moyenne
        return len(text) // 4
    
    def should_use_openai(self, messages: List[Dict[str, str]]) -> bool:
        """
        Determine si OpenAI devrait etre utilise.
        
        Args:
            messages: Liste de messages
            
        Returns:
            True si OpenAI est recommande
        """
        if not self.openai_available:
            return False
        
        # Calculer la longueur totale
        total_chars = sum(len(m.get("content", "")) for m in messages)
        
        # Detecter les taches complexes
        last_message = messages[-1].get("content", "").lower() if messages else ""
        
        complex_keywords = [
            "prouve", "demontre", "theoreme", "isabelle",
            "code complexe", "algorithme", "optimise",
            "analyse detaillee", "explique en profondeur"
        ]
        
        is_complex = any(kw in last_message for kw in complex_keywords)
        is_long = total_chars > 8000
        
        return is_complex or is_long
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """
        Retourne les modeles disponibles.
        
        Returns:
            Dictionnaire des modeles par provider
        """
        models = {"ollama": [], "openai": []}
        
        if self.ollama_available:
            try:
                import ollama
                result = ollama.list()
                models["ollama"] = [m["name"] for m in result.get("models", [])]
            except:
                pass
        
        if self.openai_available:
            models["openai"] = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
        
        return models
    
    def set_model(self, provider: str, model: str):
        """
        Change le modele actif.
        
        Args:
            provider: "ollama" ou "openai"
            model: Nom du modele
        """
        if provider == "ollama":
            self.ollama_model = model
            logger.info(f"Modele Ollama change: {model}")
        elif provider == "openai":
            self.openai_model = model
            logger.info(f"Modele OpenAI change: {model}")
