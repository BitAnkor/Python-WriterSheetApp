import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import logging


class Sidebar(ttk.Frame):
    def __init__(self, parent, sheet_updater):
        super().__init__(parent, style='Sidebar.TFrame')
        self.parent = parent
        self.sheet_updater = sheet_updater
        
        # Colores por defecto seguros
        self.bg_color = "#e0e0e0"  # Gris claro
        self.fg_color = "#333333"  # Gris oscuro
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura los elementos de la interfaz"""
        self.grid_propagate(False)
        self.config(width=200)
        
        # Título
        self.title_label = ttk.Label(
            self, 
            text="ARCHIVOS",
            style='SidebarTitle.TLabel'
        )
        self.title_label.pack(pady=(10, 5), padx=5, fill=tk.X)

        # Lista de archivos con colores seguros
        self.sheets_list = tk.Listbox(
            self,
            bg=self.bg_color,
            fg=self.fg_color,
            selectbackground='#4a6ea9',  # Azul
            selectforeground='white',
            borderwidth=0,
            highlightthickness=0,
            font=('Segoe UI', 10)
        )
        self.sheets_list.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sheets_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sheets_list.yview)
        
        # Botones de acción
        self._setup_action_buttons()

    def _setup_action_buttons(self):

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(0, 10), padx=5, fill=tk.X)
        
        buttons = [
            ("Nuevo", self._new_sheet),
            ("Abrir", self._open_sheet),
            ("Eliminar", self._delete_sheet)
        ]
        
        for text, cmd in buttons:
            btn = ttk.Button(
                btn_frame,
                text=text,
                command=cmd,
                style='Sidebar.TButton'
            )
            btn.pack(side=tk.LEFT, expand=True, padx=2)

    def _load_sheets_list(self):
        
        self.sheets_list.delete(0, tk.END)
        try:
            for sheet in self.sheet_updater.list_available_sheets():
                self.sheets_list.insert(tk.END, sheet)
        except Exception as e:
            logging.error(f"Error loading sheets list: {e}")

    def _new_sheet(self):
    
        if self.sheet_updater is None:
            messagebox.showerror("Error", "Sheet updater no está inicializado")
            return
    
        def create():
            filename = entry.get().strip()
            if not filename:
                messagebox.showwarning("Advertencia", "El nombre no puede estar vacío")
                return
            
            if not filename.endswith('.sheet'):
                filename += '.sheet'
            
            try:
                if self.sheet_updater.create_new_sheet(filename):
                    self._load_sheets_list()
                    top.destroy()
                    messagebox.showinfo("Éxito", f"Archivo {filename} creado")
                else:
                    messagebox.showerror("Error", "El archivo ya existe")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear: {str(e)}")
        
        top = tk.Toplevel(self)
        top.title("Nuevo Archivo")
        top.resizable(False, False)
        
        ttk.Label(top, text="Nombre del archivo:").pack(pady=(10, 5))
        entry = ttk.Entry(top, width=25)
        entry.pack(pady=5, padx=10)
        entry.focus_set()
        
        btn_frame = ttk.Frame(top)
        btn_frame.pack(pady=(5, 10))
        
        ttk.Button(btn_frame, text="Crear", command=create).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=top.destroy).pack(side=tk.LEFT)

    def _open_sheet(self):
        
        selection = self.sheets_list.curselection()
        if selection:
            filename = self.sheets_list.get(selection[0])
            sheet_data = self.sheet_updater.load_sheet(filename)
            if sheet_data:
                self.parent.editor.load_content(sheet_data['content'])
                self.parent.statusbar.set_message(f"Abierto: {filename}")

    def _delete_sheet(self):
        
        selection = self.sheets_list.curselection()
        if selection:
            filename = self.sheets_list.get(selection[0])
            if messagebox.askyesno(
                "Confirmar",
                f"¿Eliminar permanentemente {filename}?"
            ):
                try:
                    (self.sheet_updater.workspace / filename).unlink()
                    self._load_sheets_list()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")