
import json
from pathlib import Path
from typing import Union, Optional, Dict, Any
import logging
from dataclasses import dataclass, asdict
from datetime import datetime

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SheetMetadata:
    
    created_at: str
    modified_at: str
    version: str = "1.0"

class SheetUpdater:
    def __init__(self, workspace: Union[str, Path] = "sheets"):
        
        self.workspace = Path(workspace)
        self._current_sheet: Optional[Path] = None
        self._ensure_workspace_exists()
        
    def _ensure_workspace_exists(self) -> None:
        
        try:
            self.workspace.mkdir(exist_ok=True, parents=True)
        except PermissionError as e:
            logger.error(f"Error de permisos al crear workspace: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al crear workspace: {e}")
            raise

    def create_new_sheet(self, filename: str, content: str = "") -> bool:
       
        sheet_path = self.workspace / f"{filename}.sheet"
        
        if sheet_path.exists():
            logger.warning(f"El archivo {sheet_path} ya existe")
            return False
            
        metadata = SheetMetadata(
            created_at=str(datetime.now()),
            modified_at=str(datetime.now())
        )
        
        return self._save_sheet(sheet_path, content, metadata)

    def update_current_sheet(self, content: str) -> bool:
      
        if not self._current_sheet:
            logger.error("No hay hoja seleccionada para actualizar")
            return False
            
        try:
            with open(self._current_sheet, 'r') as f:
                existing_data = json.load(f)
            metadata = SheetMetadata(**existing_data['metadata'])
            metadata.modified_at = str(datetime.now())
        except Exception as e:
            logger.error(f"Error al leer hoja existente: {e}")
            metadata = SheetMetadata(
                created_at=str(datetime.now()),
                modified_at=str(datetime.now())
            )

        return self._save_sheet(self._current_sheet, content, metadata)

    def _save_sheet(self, 
                  path: Path, 
                  content: str, 
                  metadata: SheetMetadata) -> bool:
       
        try:
            data = {
                "metadata": asdict(metadata),
                "content": content
            }
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Hoja guardada en {path}")
            return True
            
        except IOError as e:
            logger.error(f"Error de E/S al guardar: {e}")
        except Exception as e:
            logger.error(f"Error inesperado al guardar: {e}")
            
        return False

    def load_sheet(self, filename: str) -> Optional[Dict[str, Any]]:
        
        sheet_path = self.workspace / filename
        try:
            with open(sheet_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self._current_sheet = sheet_path
            return data
            
        except FileNotFoundError:
            logger.error(f"Archivo {filename} no encontrado")
        except json.JSONDecodeError:
            logger.error(f"Error decodificando {filename}")
        except Exception as e:
            logger.error(f"Error al cargar {filename}: {e}")
            
        return None

    def list_available_sheets(self) -> list[str]:
        """Lista todas las hojas disponibles en el workspace"""
        return [f.name for f in self.workspace.glob("*.sheet") if f.is_file()]