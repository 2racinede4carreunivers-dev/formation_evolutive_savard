#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Reconnaissance Vocale
============================
Gere la reconnaissance et la synthese vocale.
"""

import os
import logging
from typing import Dict, Any, Optional, Callable
import threading
import queue

logger = logging.getLogger(__name__)


class VoiceModule:
    """Module de gestion vocale."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le module vocal.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        self.enabled = os.environ.get("ENABLE_VOICE", "true").lower() == "true"
        self.language = os.environ.get("DEFAULT_LANGUAGE", "fr")
        
        # Reconnaissance vocale
        self._recognizer = None
        self._microphone = None
        
        # Synthese vocale
        self._tts_engine = None
        
        # Queue pour les resultats
        self._result_queue = queue.Queue()
        
        # Callback pour les resultats
        self._callback: Optional[Callable[[str], None]] = None
        
        # Thread d'ecoute
        self._listening = False
        self._listen_thread: Optional[threading.Thread] = None
        
        if self.enabled:
            self._initialize()
        
        logger.info(f"Module vocal initialise - Active: {self.enabled}")
    
    def _initialize(self):
        """Initialise les composants vocaux."""
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone()
            
            # Ajuster pour le bruit ambiant
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logger.info("Reconnaissance vocale initialisee")
        except Exception as e:
            logger.error(f"Erreur initialisation reconnaissance vocale: {e}")
            self._recognizer = None
        
        try:
            import pyttsx3
            self._tts_engine = pyttsx3.init()
            
            # Configuration de la voix
            voices = self._tts_engine.getProperty('voices')
            
            # Chercher une voix francaise
            for voice in voices:
                if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                    self._tts_engine.setProperty('voice', voice.id)
                    break
            
            self._tts_engine.setProperty('rate', 150)
            
            logger.info("Synthese vocale initialisee")
        except Exception as e:
            logger.error(f"Erreur initialisation synthese vocale: {e}")
            self._tts_engine = None
    
    def start_listening(self, callback: Callable[[str], None]):
        """
        Demarre l'ecoute continue.
        
        Args:
            callback: Fonction appelee avec le texte reconnu
        """
        if not self._recognizer or not self._microphone:
            logger.warning("Reconnaissance vocale non disponible")
            return
        
        self._callback = callback
        self._listening = True
        
        self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listen_thread.start()
        
        logger.info("Ecoute vocale demarree")
    
    def stop_listening(self):
        """Arrete l'ecoute."""
        self._listening = False
        if self._listen_thread:
            self._listen_thread.join(timeout=2)
        logger.info("Ecoute vocale arretee")
    
    def _listen_loop(self):
        """Boucle d'ecoute en arriere-plan."""
        import speech_recognition as sr
        
        while self._listening:
            try:
                with self._microphone as source:
                    # Ecouter avec timeout
                    audio = self._recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=15
                    )
                
                # Reconnaitre
                text = self._recognize_audio(audio)
                
                if text and self._callback:
                    self._callback(text)
                    
            except sr.WaitTimeoutError:
                # Pas de parole detectee, continuer
                continue
            except Exception as e:
                logger.error(f"Erreur ecoute: {e}")
    
    def _recognize_audio(self, audio) -> Optional[str]:
        """
        Reconnait l'audio.
        
        Args:
            audio: Audio capture
            
        Returns:
            Texte reconnu ou None
        """
        import speech_recognition as sr
        
        # Langues a essayer
        languages = []
        if self.language == "fr":
            languages = ["fr-FR", "en-US"]
        else:
            languages = ["en-US", "fr-FR"]
        
        for lang in languages:
            try:
                text = self._recognizer.recognize_google(audio, language=lang)
                logger.debug(f"Reconnu ({lang}): {text}")
                return text
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                logger.error(f"Erreur API reconnaissance: {e}")
                return None
        
        return None
    
    async def listen_once(self) -> Optional[str]:
        """
        Ecoute une seule phrase.
        
        Returns:
            Texte reconnu ou None
        """
        if not self._recognizer or not self._microphone:
            return None
        
        import speech_recognition as sr
        
        try:
            with self._microphone as source:
                logger.info("Ecoute en cours...")
                audio = self._recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            return self._recognize_audio(audio)
            
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            logger.error(f"Erreur ecoute: {e}")
            return None
    
    def speak(self, text: str):
        """
        Synthetise et joue le texte.
        
        Args:
            text: Texte a prononcer
        """
        if not self._tts_engine:
            logger.warning("Synthese vocale non disponible")
            return
        
        try:
            # Nettoyer le texte (retirer markdown, etc.)
            clean_text = self._clean_text_for_speech(text)
            
            self._tts_engine.say(clean_text)
            self._tts_engine.runAndWait()
            
        except Exception as e:
            logger.error(f"Erreur synthese vocale: {e}")
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Nettoie le texte pour la synthese vocale.
        
        Args:
            text: Texte brut
            
        Returns:
            Texte nettoye
        """
        import re
        
        # Retirer le markdown
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
        text = re.sub(r'`[^`]+`', '', text)              # Code inline
        text = re.sub(r'```[\s\S]*?```', '', text)       # Code blocks
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
        text = re.sub(r'#{1,6}\s*', '', text)            # Headers
        text = re.sub(r'[-*]\s+', '', text)              # List items
        
        # Retirer les formules LaTeX
        text = re.sub(r'\$[^$]+\$', 'formule mathematique', text)
        
        # Limiter la longueur
        if len(text) > 500:
            text = text[:500] + "... suite tronquee pour la lecture."
        
        return text.strip()
    
    def is_available(self) -> bool:
        """Verifie si le module vocal est disponible."""
        return self._recognizer is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du module vocal."""
        return {
            "enabled": self.enabled,
            "recognition_available": self._recognizer is not None,
            "synthesis_available": self._tts_engine is not None,
            "listening": self._listening,
            "language": self.language
        }
