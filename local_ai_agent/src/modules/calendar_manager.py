#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Calendrier
=================
Gere les evenements et rendez-vous.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class CalendarEvent:
    """Represente un evenement de calendrier."""
    title: str
    start: datetime
    end: datetime
    description: Optional[str] = None
    location: Optional[str] = None
    reminder_minutes: int = 30


class CalendarModule:
    """Module de gestion du calendrier."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le module calendrier.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        self.provider = os.environ.get("CALENDAR_PROVIDER", "local")
        
        # Stockage local des evenements
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.calendar_file = self.data_dir / "calendar.json"
        
        self._events: List[Dict[str, Any]] = []
        self._load_events()
        
        logger.info(f"Module calendrier initialise - Provider: {self.provider}")
    
    def _load_events(self):
        """Charge les evenements depuis le stockage local."""
        if self.calendar_file.exists():
            try:
                with open(self.calendar_file, 'r', encoding='utf-8') as f:
                    self._events = json.load(f)
            except Exception as e:
                logger.error(f"Erreur chargement calendrier: {e}")
                self._events = []
    
    def _save_events(self):
        """Sauvegarde les evenements."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.calendar_file, 'w', encoding='utf-8') as f:
            json.dump(self._events, f, indent=2, default=str)
    
    async def add_event(self, query: str) -> str:
        """
        Ajoute un evenement au calendrier.
        
        Args:
            query: Description de l'evenement
            
        Returns:
            Confirmation ou demande de details
        """
        # Parser la requete
        event_info = self._parse_event_request(query)
        
        if not event_info.get('title'):
            return "Je n'ai pas compris l'evenement. Precisez le titre et la date."
        
        # Creer l'evenement
        event = {
            'id': len(self._events) + 1,
            'title': event_info['title'],
            'start': event_info.get('start', datetime.now() + timedelta(hours=1)).isoformat(),
            'end': event_info.get('end', datetime.now() + timedelta(hours=2)).isoformat(),
            'description': event_info.get('description', ''),
            'location': event_info.get('location', ''),
            'created_at': datetime.now().isoformat()
        }
        
        self._events.append(event)
        self._save_events()
        
        return f"""**Evenement cree:**

📅 **{event['title']}**
🕐 Debut: {event['start']}
🕐 Fin: {event['end']}
📍 Lieu: {event.get('location', 'Non specifie')}

*L'evenement a ete ajoute a votre calendrier local.*
"""
    
    def _parse_event_request(self, query: str) -> Dict[str, Any]:
        """
        Parse une requete d'evenement.
        
        Args:
            query: Requete en langage naturel
            
        Returns:
            Informations de l'evenement
        """
        import re
        
        info = {}
        
        # Extraire le titre (entre guillemets ou apres "rendez-vous")
        title_patterns = [
            r'["\']([^"\']+)["\']',
            r'rendez-vous\s+(?:pour\s+)?(.+?)(?:\s+(?:le|a|demain|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche))',
            r'evenement\s+(.+?)(?:\s+(?:le|a|demain))',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                info['title'] = match.group(1).strip()
                break
        
        if 'title' not in info:
            # Utiliser toute la requete comme titre par defaut
            info['title'] = query[:50]
        
        # Extraire la date/heure
        now = datetime.now()
        
        if 'demain' in query.lower():
            info['start'] = now + timedelta(days=1)
        elif 'apres-demain' in query.lower():
            info['start'] = now + timedelta(days=2)
        else:
            info['start'] = now + timedelta(hours=1)
        
        # Extraire l'heure
        time_match = re.search(r'(\d{1,2})[h:](\d{2})?', query)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            info['start'] = info['start'].replace(hour=hour, minute=minute)
        
        info['end'] = info['start'] + timedelta(hours=1)
        
        return info
    
    async def list_events(self, days: int = 7) -> str:
        """
        Liste les evenements a venir.
        
        Args:
            days: Nombre de jours a afficher
            
        Returns:
            Liste formatee des evenements
        """
        now = datetime.now()
        end_date = now + timedelta(days=days)
        
        upcoming = []
        for event in self._events:
            try:
                start = datetime.fromisoformat(event['start'])
                if now <= start <= end_date:
                    upcoming.append(event)
            except:
                continue
        
        if not upcoming:
            return f"Aucun evenement prevu dans les {days} prochains jours."
        
        # Trier par date
        upcoming.sort(key=lambda x: x['start'])
        
        result = f"**Evenements des {days} prochains jours:**\n\n"
        
        current_date = None
        for event in upcoming:
            start = datetime.fromisoformat(event['start'])
            date_str = start.strftime("%A %d %B")
            
            if date_str != current_date:
                current_date = date_str
                result += f"\n**{date_str}**\n"
            
            time_str = start.strftime("%H:%M")
            result += f"  - {time_str} - {event['title']}\n"
        
        return result
    
    async def delete_event(self, event_id: int) -> str:
        """
        Supprime un evenement.
        
        Args:
            event_id: ID de l'evenement
            
        Returns:
            Confirmation
        """
        for i, event in enumerate(self._events):
            if event.get('id') == event_id:
                deleted = self._events.pop(i)
                self._save_events()
                return f"Evenement '{deleted['title']}' supprime."
        
        return f"Evenement #{event_id} non trouve."
    
    async def get_today(self) -> str:
        """Retourne les evenements du jour."""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0)
        today_end = now.replace(hour=23, minute=59, second=59)
        
        today_events = []
        for event in self._events:
            try:
                start = datetime.fromisoformat(event['start'])
                if today_start <= start <= today_end:
                    today_events.append(event)
            except:
                continue
        
        if not today_events:
            return "Aucun evenement prevu aujourd'hui."
        
        result = "**Evenements d'aujourd'hui:**\n\n"
        for event in sorted(today_events, key=lambda x: x['start']):
            start = datetime.fromisoformat(event['start'])
            result += f"  - {start.strftime('%H:%M')} - {event['title']}\n"
        
        return result
