import tkinter as tk
from tkinter import ttk
from datetime import datetime
import logging

class Statusbar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='Statusbar.TFrame')
        self.parent = parent
        self._setup_ui()
        self._last_update = None

    def _setup_ui(self):
        
        self.grid_propagate(False)
        self.config(height=24)
        
        # Configurar el sistema de paneles
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        
        # Panel izquierdo (mensajes)
        self.left_panel = ttk.Frame(self, style='Statusbar.TFrame')
        self.left_panel.grid(row=0, column=0, sticky='w')
        
        self.message_label = ttk.Label(
            self.left_panel,
            text="Listo",
            style='Statusbar.TLabel'
        )
        self.message_label.pack(side=tk.LEFT, padx=5)
        
        # Panel derecho (estado e información)
        self.right_panel = ttk.Frame(self, style='Statusbar.TFrame')
        self.right_panel.grid(row=0, column=1, sticky='e')
        
        # Contador de palabras
        self.word_count_label = ttk.Label(
            self.right_panel,
            text="Palabras: 0",
            style='Statusbar.TLabel'
        )
        self.word_count_label.pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(
            self.right_panel,
            orient=tk.VERTICAL
        ).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # Indicador de posición del cursor
        self.cursor_position_label = ttk.Label(
            self.right_panel,
            text="Ln 1, Col 1",
            style='Statusbar.TLabel'
        )
        self.cursor_position_label.pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(
            self.right_panel,
            orient=tk.VERTICAL
        ).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # Indicador de estado de guardado
        self.save_status_label = ttk.Label(
            self.right_panel,
            text="● Guardado",
            style='Statusbar.TLabel'
        )
        self.save_status_label.pack(side=tk.LEFT, padx=5)
        
        # Temporizador para actualizaciones
        self._update_clock()

    def set_message(self, message: str, timeout: int = 3000):
        
        self.message_label.config(text=message)
        self._last_update = datetime.now()
        
        if timeout > 0:
            self.after(timeout, self._check_message_expiry)

    def set_word_count(self, count: int):
        
        self.word_count_label.config(text=f"Palabras: {count}")

    def set_cursor_position(self, line: int, column: int):
        
        self.cursor_position_label.config(text=f"Ln {line}, Col {column}")

    def set_save_status(self, saved: bool):
        
        if saved:
            self.save_status_label.config(text="● Guardado", foreground='green')
        else:
            self.save_status_label.config(text="○ Sin guardar", foreground='orange')

    def _update_clock(self):
        
        current_time = datetime.now().strftime("%H:%M")
        if hasattr(self, 'time_label'):
            self.time_label.config(text=current_time)
        self.after(60000, self._update_clock)  # Actualizar cada minuto

    def _check_message_expiry(self):
        
        if self._last_update and (datetime.now() - self._last_update).seconds > 3:
            self.message_label.config(text="Listo")

    def bind_to_editor(self, editor):
        
        editor.text_area.bind('<KeyRelease>', lambda e: self._on_text_change(editor))
        editor.text_area.bind('<ButtonRelease>', lambda e: self._update_cursor_pos(editor))
        
    def _on_text_change(self, editor):
        
        content = editor.text_area.get("1.0", "end-1c")
        word_count = len(content.split())
        self.set_word_count(word_count)
        self.set_save_status(False)
        self._update_cursor_pos(editor)

    def _update_cursor_pos(self, editor):
        
        cursor_pos = editor.text_area.index(tk.INSERT)
        line, col = map(int, cursor_pos.split('.'))
        self.set_cursor_position(line, col)