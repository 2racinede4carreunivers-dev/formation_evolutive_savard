#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenetre Principale
==================
Interface graphique principale de l'agent IA.
"""

import sys
import os
import logging
import asyncio
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QSplitter, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QStatusBar, QToolBar,
    QDialog, QDialogButtonBox, QFormLayout,
    QComboBox, QCheckBox, QTabWidget, QFrame,
    QScrollArea, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon, QAction, QKeySequence, QTextCursor

# Charger la configuration
import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class AsyncWorker(QThread):
    """Thread pour executer des taches asynchrones."""
    
    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
    
    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.coro)
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            loop.close()


class ChatDisplay(QTextEdit):
    """Widget d'affichage de la conversation."""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Segoe UI", 11))
        
        # Style
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: none;
                padding: 15px;
                selection-background-color: #45475a;
            }
        """)
    
    def add_message(self, role: str, content: str):
        """Ajoute un message a l'affichage."""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        if role == "user":
            prefix = '<p style="color: #89b4fa; font-weight: bold;">Vous:</p>'
        else:
            prefix = '<p style="color: #a6e3a1; font-weight: bold;">Agent:</p>'
        
        # Convertir le markdown basique en HTML
        html_content = self._markdown_to_html(content)
        
        cursor.insertHtml(f'{prefix}<p style="color: #cdd6f4; margin-left: 10px;">{html_content}</p><br>')
        
        # Scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
    
    def _markdown_to_html(self, text: str) -> str:
        """Convertit le markdown basique en HTML."""
        import re
        
        # Code blocks
        text = re.sub(r'```(\w+)?\n([\s\S]*?)\n```', 
                      r'<pre style="background-color: #313244; padding: 10px; border-radius: 5px; overflow-x: auto;"><code>\2</code></pre>', 
                      text)
        
        # Inline code
        text = re.sub(r'`([^`]+)`', 
                      r'<code style="background-color: #313244; padding: 2px 5px; border-radius: 3px;">\1</code>', 
                      text)
        
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        
        # Headers
        text = re.sub(r'^### (.+)$', r'<h4 style="color: #f5c2e7;">\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h3 style="color: #f5c2e7;">\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<h2 style="color: #f5c2e7;">\1</h2>', text, flags=re.MULTILINE)
        
        # Lists
        text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        
        # Line breaks
        text = text.replace('\n', '<br>')
        
        return text
    
    def clear_chat(self):
        """Efface la conversation."""
        self.clear()


class MessageInput(QLineEdit):
    """Widget de saisie de message."""
    
    send_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Segoe UI", 11))
        self.setPlaceholderText("Tapez votre message ici... (Ctrl+Enter pour envoyer)")
        
        self.setStyleSheet("""
            QLineEdit {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 10px;
                padding: 12px 15px;
                selection-background-color: #89b4fa;
            }
            QLineEdit:focus {
                border-color: #89b4fa;
            }
        """)
    
    def keyPressEvent(self, event):
        """Gere les touches."""
        if event.key() == Qt.Key.Key_Return:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self.send_message.emit(self.text())
                self.clear()
            else:
                self.send_message.emit(self.text())
                self.clear()
        else:
            super().keyPressEvent(event)


class ConversationList(QListWidget):
    """Liste des conversations."""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QListWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: none;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #45475a;
            }
            QListWidget::item:hover {
                background-color: #313244;
            }
        """)


class MathAgentApp(QMainWindow):
    """Fenetre principale de l'application."""
    
    def __init__(self):
        super().__init__()
        
        # Charger la configuration
        self.config = self._load_config()
        
        # Initialiser l'agent
        self.agent = None
        self._init_agent()
        
        # Worker pour les taches async
        self.worker: Optional[AsyncWorker] = None
        
        # Configurer l'interface
        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_statusbar()
        self._apply_theme()
        
        # Message de bienvenue
        self._show_welcome()
        
        logger.info("Interface graphique initialisee")
    
    def _load_config(self) -> dict:
        """Charge la configuration."""
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        return {}
    
    def _init_agent(self):
        """Initialise l'agent IA."""
        try:
            from ..core.agent import MathAgent
            self.agent = MathAgent(self.config)
        except Exception as e:
            logger.error(f"Erreur initialisation agent: {e}")
            self.agent = None
    
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("Agent IA Mathematique")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter pour redimensionner
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # === Panneau lateral gauche ===
        side_panel = QFrame()
        side_panel.setStyleSheet("background-color: #181825;")
        side_panel.setMinimumWidth(250)
        side_panel.setMaximumWidth(350)
        
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(10, 10, 10, 10)
        
        # Bouton nouvelle conversation
        new_chat_btn = QPushButton("+ Nouvelle Conversation")
        new_chat_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
        """)
        new_chat_btn.clicked.connect(self._new_conversation)
        side_layout.addWidget(new_chat_btn)
        
        # Label historique
        history_label = QLabel("Historique")
        history_label.setStyleSheet("color: #a6adc8; padding: 10px 0 5px 0;")
        side_layout.addWidget(history_label)
        
        # Liste des conversations
        self.conversation_list = ConversationList()
        self.conversation_list.itemClicked.connect(self._load_conversation)
        side_layout.addWidget(self.conversation_list)
        
        splitter.addWidget(side_panel)
        
        # === Zone principale ===
        main_panel = QFrame()
        main_panel.setStyleSheet("background-color: #1e1e2e;")
        
        main_panel_layout = QVBoxLayout(main_panel)
        main_panel_layout.setContentsMargins(0, 0, 0, 0)
        main_panel_layout.setSpacing(0)
        
        # Zone de chat
        self.chat_display = ChatDisplay()
        main_panel_layout.addWidget(self.chat_display, stretch=1)
        
        # Zone de saisie
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #181825; padding: 15px;")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        
        # Bouton microphone
        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setFixedSize(45, 45)
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: 22px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #f38ba8;
            }
        """)
        self.mic_btn.clicked.connect(self._toggle_voice)
        input_layout.addWidget(self.mic_btn)
        
        # Champ de saisie
        self.message_input = MessageInput()
        self.message_input.send_message.connect(self._send_message)
        input_layout.addWidget(self.message_input, stretch=1)
        
        # Bouton envoyer
        send_btn = QPushButton("Envoyer")
        send_btn.setFixedHeight(45)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 10px;
                padding: 0 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
        """)
        send_btn.clicked.connect(lambda: self._send_message(self.message_input.text()))
        input_layout.addWidget(send_btn)
        
        main_panel_layout.addWidget(input_frame)
        
        splitter.addWidget(main_panel)
        
        # Proportions du splitter
        splitter.setSizes([280, 920])
        
        # Rafraichir la liste des conversations
        self._refresh_conversation_list()
    
    def _setup_menu(self):
        """Configure la barre de menu."""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #181825;
                color: #cdd6f4;
                padding: 5px;
            }
            QMenuBar::item:selected {
                background-color: #313244;
            }
            QMenu {
                background-color: #1e1e2e;
                color: #cdd6f4;
                border: 1px solid #45475a;
            }
            QMenu::item:selected {
                background-color: #45475a;
            }
        """)
        
        # Menu Fichier
        file_menu = menubar.addMenu("&Fichier")
        
        new_action = QAction("Nouvelle conversation", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self._new_conversation)
        file_menu.addAction(new_action)
        
        save_action = QAction("Sauvegarder", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._save_conversation)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Exporter les donnees...", self)
        export_action.triggered.connect(self._export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quitter", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Edition
        edit_menu = menubar.addMenu("&Edition")
        
        clear_action = QAction("Effacer la conversation", self)
        clear_action.triggered.connect(self._clear_chat)
        edit_menu.addAction(clear_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("&Outils")
        
        calc_action = QAction("Calculatrice", self)
        calc_action.triggered.connect(lambda: self._send_message("Ouvre une calculatrice"))
        tools_menu.addAction(calc_action)
        
        isabelle_action = QAction("Editeur Isabelle", self)
        isabelle_action.triggered.connect(self._open_isabelle_editor)
        tools_menu.addAction(isabelle_action)
        
        # Menu Parametres
        settings_menu = menubar.addMenu("&Parametres")
        
        model_action = QAction("Modele LLM...", self)
        model_action.triggered.connect(self._show_model_settings)
        settings_menu.addAction(model_action)
        
        api_action = QAction("Cles API...", self)
        api_action.triggered.connect(self._show_api_settings)
        settings_menu.addAction(api_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("&Aide")
        
        about_action = QAction("A propos", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_toolbar(self):
        """Configure la barre d'outils."""
        toolbar = QToolBar("Outils")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #181825;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: transparent;
                color: #cdd6f4;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QToolButton:hover {
                background-color: #313244;
            }
        """)
        self.addToolBar(toolbar)
        
        # Ajouter des actions rapides
        toolbar.addAction("📁 Fichiers")
        toolbar.addAction("📧 Email")
        toolbar.addAction("📅 Calendrier")
        toolbar.addAction("🔬 Mathematiques")
        toolbar.addAction("🌐 Recherche")
    
    def _setup_statusbar(self):
        """Configure la barre de statut."""
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: #181825;
                color: #a6adc8;
                padding: 5px;
            }
        """)
        self.setStatusBar(self.statusbar)
        
        # Labels de statut
        self.status_llm = QLabel("LLM: Pret")
        self.status_llm.setStyleSheet("color: #a6e3a1;")
        self.statusbar.addPermanentWidget(self.status_llm)
    
    def _apply_theme(self):
        """Applique le theme sombre."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QSplitter::handle {
                background-color: #313244;
                width: 2px;
            }
        """)
    
    def _show_welcome(self):
        """Affiche le message de bienvenue."""
        welcome = """Bienvenue dans l'Agent IA Mathematique!

Je suis votre assistant specialise en mathematiques. Je peux vous aider avec:

• **Calculs et equations** - Resolution, derivees, integrales
• **Preuves formelles** - Avec Isabelle/HOL
• **Graphiques** - Visualisation de fonctions
• **Gestion de fichiers** - Acces a votre systeme de fichiers
• **Emails et calendrier** - Organisation de votre temps
• **GitHub** - Gestion de vos depots
• **Recherche web** - Trouver de l'information

Tapez votre question ou commande ci-dessous. Vous pouvez aussi utiliser le microphone pour parler."""
        
        self.chat_display.add_message("assistant", welcome)
    
    def _send_message(self, message: str):
        """Envoie un message a l'agent."""
        if not message.strip():
            return
        
        self.message_input.clear()
        
        # Afficher le message utilisateur
        self.chat_display.add_message("user", message)
        
        # Mettre a jour le statut
        self.status_llm.setText("LLM: Traitement...")
        self.status_llm.setStyleSheet("color: #f9e2af;")
        
        # Desactiver l'input
        self.message_input.setEnabled(False)
        
        if self.agent:
            # Lancer le traitement dans un thread
            self.worker = AsyncWorker(self.agent.process_message(message))
            self.worker.result_ready.connect(self._on_response_received)
            self.worker.error_occurred.connect(self._on_error)
            self.worker.start()
        else:
            self._on_error("Agent non initialise. Verifiez la configuration.")
    
    def _on_response_received(self, response: str):
        """Callback quand une reponse est recue."""
        self.chat_display.add_message("assistant", response)
        
        self.status_llm.setText("LLM: Pret")
        self.status_llm.setStyleSheet("color: #a6e3a1;")
        
        self.message_input.setEnabled(True)
        self.message_input.setFocus()
    
    def _on_error(self, error: str):
        """Callback en cas d'erreur."""
        self.chat_display.add_message("assistant", f"**Erreur:** {error}")
        
        self.status_llm.setText("LLM: Erreur")
        self.status_llm.setStyleSheet("color: #f38ba8;")
        
        self.message_input.setEnabled(True)
        self.message_input.setFocus()
    
    def _new_conversation(self):
        """Demarre une nouvelle conversation."""
        if self.agent:
            self.agent.new_conversation()
        
        self.chat_display.clear_chat()
        self._show_welcome()
        self._refresh_conversation_list()
    
    def _save_conversation(self):
        """Sauvegarde la conversation actuelle."""
        if self.agent:
            conv_id = self.agent.memory.save_conversation(
                self.agent.conversation_history
            )
            self.statusbar.showMessage(f"Conversation sauvegardee: {conv_id}", 3000)
            self._refresh_conversation_list()
    
    def _load_conversation(self, item: QListWidgetItem):
        """Charge une conversation depuis l'historique."""
        conv_id = item.data(Qt.ItemDataRole.UserRole)
        
        if self.agent and conv_id:
            if self.agent.load_conversation(conv_id):
                self.chat_display.clear_chat()
                
                for msg in self.agent.conversation_history:
                    self.chat_display.add_message(msg["role"], msg["content"])
    
    def _refresh_conversation_list(self):
        """Rafraichit la liste des conversations."""
        self.conversation_list.clear()
        
        if self.agent:
            conversations = self.agent.memory.list_conversations(limit=20)
            
            for conv in conversations:
                item = QListWidgetItem(conv["title"][:40] + "..." if len(conv.get("title", "")) > 40 else conv.get("title", "Sans titre"))
                item.setData(Qt.ItemDataRole.UserRole, conv["id"])
                self.conversation_list.addItem(item)
    
    def _clear_chat(self):
        """Efface la conversation actuelle."""
        self.chat_display.clear_chat()
        if self.agent:
            self.agent.new_conversation()
    
    def _toggle_voice(self):
        """Active/desactive la reconnaissance vocale."""
        if self.agent and hasattr(self.agent, 'voice'):
            self.statusbar.showMessage("Ecoute en cours... Parlez maintenant.", 5000)
            # TODO: Implementer l'ecoute vocale
    
    def _open_isabelle_editor(self):
        """Ouvre l'editeur Isabelle."""
        self.statusbar.showMessage("Ouverture de l'editeur Isabelle...", 3000)
        # TODO: Implementer l'editeur Isabelle integre
    
    def _show_model_settings(self):
        """Affiche les parametres du modele."""
        # TODO: Implementer le dialogue de parametres
        self.statusbar.showMessage("Parametres du modele (a venir)", 3000)
    
    def _show_api_settings(self):
        """Affiche les parametres API."""
        # TODO: Implementer le dialogue de parametres
        self.statusbar.showMessage("Parametres API (a venir)", 3000)
    
    def _export_data(self):
        """Exporte les donnees."""
        if self.agent:
            export_path = Path.home() / "Documents" / "agent_export.json"
            if self.agent.memory.export_data(export_path):
                self.statusbar.showMessage(f"Donnees exportees: {export_path}", 5000)
            else:
                self.statusbar.showMessage("Erreur lors de l'export", 3000)
    
    def _show_about(self):
        """Affiche la boite A propos."""
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.about(
            self,
            "A propos de l'Agent IA Mathematique",
            """<h2>Agent IA Mathematique</h2>
            <p>Version 1.0.0</p>
            <p>Un assistant IA specialise en mathematiques avec:</p>
            <ul>
                <li>Integration Ollama + OpenAI</li>
                <li>Support Isabelle/HOL</li>
                <li>WolframAlpha pour les calculs</li>
                <li>Gestion de fichiers, emails, calendrier</li>
                <li>Integration GitHub</li>
                <li>Reconnaissance vocale</li>
            </ul>
            <p>Cree avec PyQt6 et Python</p>
            """
        )
    
    def closeEvent(self, event):
        """Gere la fermeture de l'application."""
        # Sauvegarder la conversation en cours
        if self.agent and self.agent.conversation_history:
            self.agent.memory.save_conversation(self.agent.conversation_history)
        
        event.accept()
