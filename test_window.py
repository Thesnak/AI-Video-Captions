import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_window_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DiagnosticWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Extensive logging
        logger.debug("DiagnosticWindow initialization STARTED")
        
        # Set window properties
        self.setWindowTitle("Diagnostic Window")
        
        # Get screen dimensions
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        logger.debug(f"Primary screen geometry: {screen_geometry}")
        
        # Set window size and position
        window_width = int(screen_geometry.width() * 0.5)
        window_height = int(screen_geometry.height() * 0.5)
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        
        self.setGeometry(x, y, window_width, window_height)
        
        # Create central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add label
        label = QLabel("If you can read this, the window is working!")
        layout.addWidget(label)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        logger.debug("DiagnosticWindow initialization COMPLETED")

def run_diagnostic():
    logger.debug("Starting diagnostic application")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show window
    window = DiagnosticWindow()
    
    # Multiple show methods
    window.show()
    window.raise_()
    window.activateWindow()
    
    logger.debug("Starting app.exec()")
    exit_code = app.exec()
    
    logger.debug(f"Application exited with code: {exit_code}")
    return exit_code

if __name__ == "__main__":
    run_diagnostic()