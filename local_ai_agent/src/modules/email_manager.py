#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Email
============
Gere l'envoi et la lecture d'emails.
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Email:
    """Represente un email."""
    to: List[str]
    subject: str
    body: str
    cc: Optional[List[str]] = None
    attachments: Optional[List[Path]] = None


class EmailModule:
    """Module de gestion des emails."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le module email.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        
        # Configuration email
        self.email_address = os.environ.get("EMAIL_ADDRESS", "")
        self.email_password = os.environ.get("EMAIL_APP_PASSWORD", "")
        self.smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        
        # Templates
        self.templates_dir = Path(__file__).parent.parent.parent / "templates" / "email"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        self._configured = bool(self.email_address and self.email_password)
        
        logger.info(f"Module email initialise - Configure: {self._configured}")
    
    async def compose(self, query: str) -> str:
        """
        Compose un email a partir d'une requete.
        
        Args:
            query: Description de l'email a envoyer
            
        Returns:
            Brouillon ou confirmation
        """
        if not self._configured:
            return self._get_setup_instructions()
        
        # Parser la requete pour extraire les informations
        email_info = self._parse_email_request(query)
        
        if not email_info:
            return "Je n'ai pas pu comprendre votre demande. Precisez le destinataire et le contenu de l'email."
        
        # Generer le brouillon
        draft = self._generate_draft(email_info)
        
        return f"""**Brouillon d'email:**

**A:** {', '.join(email_info.get('to', ['?']))}
**Sujet:** {email_info.get('subject', '?')}

---

{draft}

---

*Voulez-vous que j'envoie cet email? Repondez "oui" pour confirmer ou modifiez le contenu.*
"""
    
    def _get_setup_instructions(self) -> str:
        """Retourne les instructions de configuration."""
        return """**Configuration email requise**

Pour utiliser la fonctionnalite email, configurez votre fichier `.env`:

```
EMAIL_ADDRESS=votre.email@gmail.com
EMAIL_APP_PASSWORD=votre-mot-de-passe-application
```

**Pour Gmail:**
1. Activez la verification en 2 etapes sur votre compte Google
2. Allez sur: https://myaccount.google.com/apppasswords
3. Generez un mot de passe d'application
4. Utilisez ce mot de passe dans EMAIL_APP_PASSWORD
"""
    
    def _parse_email_request(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Parse une requete d'email.
        
        Args:
            query: Requete en langage naturel
            
        Returns:
            Dictionnaire avec les informations de l'email
        """
        import re
        
        info = {}
        
        # Extraire le destinataire
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, query)
        if emails:
            info['to'] = emails
        
        # Extraire le sujet (entre guillemets ou apres "sujet:")
        subject_match = re.search(r'sujet[:\s]+["\']?([^"\']+)["\']?', query, re.IGNORECASE)
        if subject_match:
            info['subject'] = subject_match.group(1).strip()
        
        # Le reste est le contenu
        info['content_hint'] = query
        
        return info if info else None
    
    def _generate_draft(self, email_info: Dict[str, Any]) -> str:
        """
        Genere un brouillon d'email.
        
        Args:
            email_info: Informations de l'email
            
        Returns:
            Contenu du brouillon
        """
        # Generer un brouillon basique
        # Dans la version complete, utiliser le LLM pour generer le contenu
        
        content_hint = email_info.get('content_hint', '')
        
        draft = f"""Bonjour,

[Contenu genere base sur: {content_hint}]

Cordialement,
[Votre nom]
"""
        return draft
    
    async def send(self, email: Email) -> str:
        """
        Envoie un email.
        
        Args:
            email: Email a envoyer
            
        Returns:
            Resultat de l'envoi
        """
        if not self._configured:
            return "Email non configure."
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = ', '.join(email.to)
            msg['Subject'] = email.subject
            
            if email.cc:
                msg['Cc'] = ', '.join(email.cc)
            
            msg.attach(MIMEText(email.body, 'plain'))
            
            # Pieces jointes
            if email.attachments:
                for attachment_path in email.attachments:
                    if attachment_path.exists():
                        with open(attachment_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="{attachment_path.name}"'
                        )
                        msg.attach(part)
            
            # Envoyer
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email envoye a: {email.to}")
            return f"**Email envoye avec succes!**\n\nDestinataire(s): {', '.join(email.to)}\nSujet: {email.subject}"
            
        except smtplib.SMTPAuthenticationError:
            return "Erreur d'authentification. Verifiez votre mot de passe d'application."
        except Exception as e:
            logger.error(f"Erreur envoi email: {e}")
            return f"Erreur lors de l'envoi: {str(e)}"
    
    async def list_templates(self) -> str:
        """Liste les templates disponibles."""
        templates = list(self.templates_dir.glob("*.txt"))
        
        if not templates:
            return "Aucun template d'email disponible."
        
        result = "**Templates d'email disponibles:**\n\n"
        for t in templates:
            result += f"  - {t.stem}\n"
        
        return result
