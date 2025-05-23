theme = {
    ".": {
        "configure": {
            "background": "#2d2d2d",
            "foreground": "#e6e6e6",
            "font": ("Segoe UI", 10)
        }
    },
    "TFrame": {
        "configure": {
            "background": "#2d2d2d"
        }
    },
    "Header.TFrame": {
        "configure": {
            "background": "#1a1a1a",
            "relief": "raised",
            "borderwidth": 1
        }
    },
    "Header.TLabel": {
        "configure": {
            "background": "#1a1a1a",
            "foreground": "#ffffff",
            "font": ("Segoe UI", 12, "bold")
        }
    },
    "Header.TButton": {
        "configure": {
            "background": "#3d3d3d",
            "foreground": "white",
            "padding": 5
        },
        "map": {
            "background": [("active", "#4a6ea9")]
        }
    },
    "Sidebar.TFrame": {
        "configure": {
            "background": "#333333",
            "borderwidth": 1,
            "relief": "sunken"
        }
    },
    "SidebarTitle.TLabel": {
        "configure": {
            "background": "#333333",
            "foreground": "#ffffff",
            "font": ("Segoe UI", 9, "bold"),
            "anchor": "center"
        }
    },
    "Sidebar.TButton": {
        "configure": {
            "background": "#3d3d3d",
            "padding": 3
        },
        "map": {
            "background": [("active", "#4d4d4d")]
        }
    },
    "Statusbar.TFrame": {
        "configure": {
            "background": "#333333",
            "borderwidth": 1,
            "relief": "sunken"
        }
    },
    "Statusbar.TLabel": {
        "configure": {
            "background": "#333333",
            "foreground": "#cccccc",
            "font": ("Segoe UI", 8),
            "padding": 2
        }
    },
    "TNotebook": {
        "configure": {
            "tabmargins": [2, 5, 2, 0],
            "background": "#2d2d2d"
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "padding": [10, 5],
            "background": "#3d3d3d"
        },
        "map": {
            "background": [("selected", "#2d2d2d")],
            "expand": [("selected", [1, 1, 1, 0])]
        }
    },
    "TScrollbar": {
        "configure": {
            "background": "#3d3d3d",
            "arrowcolor": "#ffffff"
        }
    }
}