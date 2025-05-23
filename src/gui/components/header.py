import tkinter as tk
from tkinter import ttk

class AppHeader(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='Header.TFrame')
        self.parent = parent
        
        # Definir los íconos aquí como fallback
        self.theme_icons = {
            'light': '🌙',
            'dark': '☀️'
        }
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Logo
        self.logo = ttk.Label(
            self,
            text="WriterSheetApp",
            style='Header.TLabel'
        )
        self.logo.pack(side=tk.LEFT, padx=10)
        
        # Botón de tema con valor por defecto
        current_theme = getattr(self.parent, 'current_theme', 'light')
        self.theme_btn = ttk.Button(
            self,
            text=self.theme_icons.get(current_theme, '☀️'),
            command=self._toggle_theme,
            width=3
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
    
    def _toggle_theme(self):

        if hasattr(self.parent, 'toggle_theme'):
            new_icon = self.parent.toggle_theme()
            self.theme_btn.config(text=new_icon)