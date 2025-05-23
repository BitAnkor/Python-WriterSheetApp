import logging
from pathlib import Path
from gui.app import WriterApp
from core.updatesheets import SheetUpdater

def configure_logging():
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def get_default_workspace():
    
    return Path.home() / "WriterSheetApp" / "workspace"


def main():
    try:
        # Configuración inicial
        configure_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting application initialization")
        
        
        workspace_path = Path.home() / "WriterSheetApp" / "workspace"
        workspace_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Workspace initialized at: {workspace_path}")
        
        sheet_updater = SheetUpdater(workspace=workspace_path)
        
        
        app = WriterApp(sheet_updater)
    
        logger.info("Application initialized successfully")
        app.mainloop()
        
    except Exception as e:
        logger.critical(f"Fatal error during initialization: {e}")
        raise

if __name__ == "__main__":
    main()