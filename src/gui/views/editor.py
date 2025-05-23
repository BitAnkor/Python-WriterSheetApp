import tkinter as tk
from tkinter import ttk, scrolledtext


class EditorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self._setup_editor()
        
    def _setup_editor(self):
        bg = self.app.style.lookup('TFrame', 'background')
        fg = self.app.style.lookup('TLabel', 'foreground')
        
        self.text_area = tk.Text(
            self,
            wrap=tk.WORD,
            font=('Segoe UI', 12),
            padx=10,
            pady=10,
            bg=bg,
            fg=fg,
            insertbackground=fg,  # Color del cursor
            selectbackground='#4a6ea9',
            selectforeground='white'
        )
        
        # Scrollbar con estilo
        scroll = ttk.Scrollbar(self, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scroll.set)
        
        # Layout
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
    def _setup_toolbar(self):
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(fill=tk.X)
        
        tools = [
            ("Bold", self._make_bold),
            ("Italic", self._make_italic),
            ("Save", self._save_content)
        ]
        
        for text, cmd in tools:
            btn = ttk.Button(
                self.toolbar,
                text=text,
                command=cmd
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _setup_editor(self):
        self.text_area = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=('Segoe UI', 12),
            padx=10,
            pady=10
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
        # Configuración de tags para formato
        self.text_area.tag_config('bold', font=('Segoe UI', 12, 'bold'))
        self.text_area.tag_config('italic', font=('Segoe UI', 12, 'italic'))
    
    def _make_bold(self):
        self._apply_format('bold')
        
    def _make_italic(self):
        self._apply_format('italic')
        
    def _apply_format(self, tag):
        try:
            current_tags = self.text_area.tag_names(tk.SEL_FIRST)
            if tag in current_tags:
                self.text_area.tag_remove(tag, tk.SEL_FIRST, tk.SEL_LAST)
            else:
                self.text_area.tag_add(tag, tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
    
    def _save_content(self):
        content = self.text_area.get("1.0", tk.END)
        self.master.sheet_updater.update_current_sheet(content)