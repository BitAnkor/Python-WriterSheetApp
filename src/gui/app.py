import tkinter as tk
from tkinter import ttk
import sys
import os
from gui.components.header import AppHeader
from gui.components.sidebar import Sidebar
from gui.components.statusbar import Statusbar
from gui.views.editor import EditorView

#para asegurar los imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



class WriterApp(tk.Tk):
    def __init__(self, sheet_updater=None):
        super().__init__()
        self.title("WriterSheetApp")
        self.geometry("1200x700")
        self.minsize(800, 500)
        
        # Configuración de tema 
        self.current_theme = 'light'
        self.theme_icons = {
            'light': '🌙',
            'dark': '☀️'
        }
        self._load_theme(self.current_theme)
        
        # Inicializa componentes
        self.sheet_updater = sheet_updater
        self._setup_main_layout()
    
    def _load_theme(self, theme_name):
        
        try:
            theme_module = __import__(
                f'gui.themes.{theme_name}',
                fromlist=['theme']
            )
            self.style = ttk.Style(self)
            self.style.theme_use('default')
            self.style.theme_create('custom', settings=theme_module.theme)
            self.style.theme_use('custom')
        except Exception as e:
            print(f"Error loading theme: {e}")
            # Fallback básico
            self.style = ttk.Style(self)
            bg = '#f5f5f5' if theme_name == 'light' else '#2d2d2d'
            self.style.configure('.', background=bg)
    
    def toggle_theme(self):
        
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self._load_theme(new_theme)
        self.current_theme = new_theme
        return self.theme_icons[new_theme]
    
    def _setup_main_layout(self):
        
        # Grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Componentes 
        self.header = AppHeader(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        self.sidebar = Sidebar(self, self.sheet_updater)  
        self.sidebar.grid(row=1, column=0, sticky='ns')
        
        self.editor = EditorView(self)
        self.editor.grid(row=1, column=1, sticky='nsew')
        
        self.statusbar = Statusbar(self)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky='ew')