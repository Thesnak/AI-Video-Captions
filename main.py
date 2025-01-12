import sys
import logging
import os
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QTimer
from infrastructure.video_processor import MoviePyVideoProcessor
from infrastructure.transcriber import WhisperTranscriber
from infrastructure.translator import GoogleTranslatorService
from infrastructure.terminal_debugger import TerminalDebugger
from application.subtitle_service import SubtitleService
from presentation.main_window import MainWindow
from infrastructure.preferences import JsonUserPreferences
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_splash_screen():
    """Create and display a splash screen"""
    # Ensure the path to the splash image is correct
    splash_image_path = os.path.join('assets', 'splash_screen.png')
    
    # Create splash screen
    splash_pixmap = QPixmap(splash_image_path)
    
    # Get screen dimensions
    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()
    
    # Define fixed splash screen size
    splash_width = 800
    splash_height = 400
    
    # Scale splash screen while maintaining aspect ratio
    scaled_pixmap = splash_pixmap.scaled(
        splash_width, 
        splash_height, 
        Qt.AspectRatioMode.KeepAspectRatio, 
        Qt.TransformationMode.SmoothTransformation
    )
    
    splash = QSplashScreen(scaled_pixmap)
    splash.setWindowFlags(
        Qt.WindowType.WindowStaysOnTopHint | 
        Qt.WindowType.FramelessWindowHint
    )
    
    # Center the splash screen
    splash.move(
        (screen_geometry.width() - splash_width) // 2,
        (screen_geometry.height() - splash_height) // 2
    )
    
    splash.setFixedSize(splash_width, splash_height)
    splash.show()
    
    return splash

def main():
    try:
        # Log system and dependency information
        system_info = TerminalDebugger.get_system_info()
        dependencies = TerminalDebugger.check_dependencies()
        
        logger.info("System Information:")
        logger.info(json.dumps(system_info, indent=2))
        
        logger.info("Dependency Versions:")
        logger.info(json.dumps(dependencies, indent=2))
        
        # Create application
        app = QApplication(sys.argv)
        
        # Set application icon
        app_icon_path = os.path.join('assets', 'logo.jpg')
        app_icon = QIcon(app_icon_path)
        app.setWindowIcon(app_icon)
        
        # Create and show splash screen
        splash = create_splash_screen()
        
        # Initialize services
        video_processor = MoviePyVideoProcessor()
        transcriber = WhisperTranscriber()
        translator = GoogleTranslatorService()
        preferences = JsonUserPreferences()
        
        # Create subtitle service with optional progress callback
        subtitle_service = SubtitleService(
            video_processor=video_processor,
            transcriber=transcriber,
            translator=translator,
            progress_callback=None
        )

        # Create main window
        window = MainWindow(subtitle_service, preferences)
        
        # Close splash screen after a delay and show main window
        QTimer.singleShot(2000, splash.close)  # 2-second splash screen
        QTimer.singleShot(2000, window.show)
        
        # Execute application
        exit_code = app.exec()
        
        # Log application exit
        logger.info(f"Application exited with code: {exit_code}")
        
        return exit_code
    
    except Exception as e:
        # Capture and log any unexpected errors
        error_info = TerminalDebugger.capture_exception(e)
        TerminalDebugger.log_error(error_info)
        
        # Log to console
        logger.error("Unhandled exception in main application")
        logger.error(json.dumps(error_info, indent=2))
        
        return 1

if __name__ == "__main__":
    sys.exit(main())