from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QFileDialog, QProgressBar, QComboBox, QLabel,
                           QTextEdit, QMessageBox, QHBoxLayout, QStyle,
                           QStackedWidget, QToolBar, QDialog, QSpinBox, QCheckBox,
                           QApplication, QGroupBox, QGridLayout, QLineEdit,
                           QTabWidget, QDialogButtonBox, QFormLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from presentation.styles import LIGHT_STYLE, DARK_STYLE
from presentation.animations import WidgetAnimations
from presentation.batch_processor import BatchProcessingWidget
from infrastructure.preferences import JsonUserPreferences
from application.subtitle_service import SubtitleService
from domain.interfaces import ProcessingStatus
import asyncio
import pathlib
import os
import logging
import traceback
import sys
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main_window_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ErrorHandler:
    @staticmethod
    def show_error_message(parent, title, message, details=None):
        """Display a comprehensive error message dialog"""
        error_dialog = QMessageBox(parent)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)

        if details:
            error_dialog.setDetailedText(details)

        error_dialog.exec()

class VideoProcessingThread(QThread):
    """Dedicated thread for video processing with signal-based error handling"""
    processing_complete = pyqtSignal(object)
    processing_error = pyqtSignal(str, str)

    def __init__(
        self, 
        subtitle_service, 
        file_path, 
        target_language, 
        translation_method='GoogleTrans'
    ):
        super().__init__()
        self.subtitle_service = subtitle_service
        self.file_path = file_path
        self.target_language = target_language
        self.translation_method = translation_method

    def run(self):
        try:
            # Simulate processing with progress updates
            result = asyncio.run(
                self.subtitle_service.process_video(
                    pathlib.Path(self.file_path), 
                    self.target_language,
                    self.translation_method
                )
            )
            self.processing_complete.emit(result)
        except Exception as e:
            # Capture full traceback for detailed error logging
            error_traceback = traceback.format_exc()
            logger.error(f"Video processing error: {e}")
            logger.error(error_traceback)
            self.processing_error.emit(str(e), error_traceback)

class PreferencesDialog(QDialog):
    """Modern, responsive preferences dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Dialog configuration
        self.setWindowTitle("Application Preferences")
        self.setMinimumSize(600, 500)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Preferences Tabs
        self.tab_widget = QTabWidget()
        
        # General Preferences Tab
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(10)
        
        # Theme Selection
        theme_label = QLabel("Application Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System Default"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        general_layout.addRow(theme_label, self.theme_combo)
        
        # Language Preferences
        language_label = QLabel("Default Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English", "Spanish", "French", 
            "German", "Italian", "Portuguese", "Arabic"
        ])
        general_layout.addRow(language_label, self.language_combo)
        
        # Translation Preferences Tab
        translation_tab = QWidget()
        translation_layout = QFormLayout(translation_tab)
        translation_layout.setContentsMargins(20, 20, 20, 20)
        translation_layout.setSpacing(10)
        
        # Translation Method
        method_label = QLabel("Default Translation Method:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GoogleTrans", "Argos Translate"])
        translation_layout.addRow(method_label, self.method_combo)
        
        # Max Chunk Size
        chunk_label = QLabel("Translation Chunk Size:")
        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(100, 1000)
        self.chunk_spin.setValue(500)
        self.chunk_spin.setSuffix(" characters")
        translation_layout.addRow(chunk_label, self.chunk_spin)
        
        # About Tab
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        about_layout.setContentsMargins(20, 20, 20, 20)
        about_layout.setSpacing(15)
        
        # App Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join('assets', 'logo.jpg'))
        logo_label.setPixmap(logo_pixmap.scaled(
            200, 200, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(logo_label)
        
        # App Description
        app_name = QLabel("<h2>AI Video Captions</h2>")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(app_name)
        
        description = QLabel(
            "Automated video captioning and translation tool\n"
            "Powered by <a href='https://www.linkedin.com/in/mohamed-thesnak/'>Mohamed Mahmoud</a> \n"
            "Version: 1.0.0\n\n"
            " 2025 AI Video Captions Team"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(description)
        
        # Hyperlinks
        github_link = QLabel(
            '<a href="https://github.com/Thesnak/AI-Video-Captions">GitHub Repository</a>'
        )
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(github_link)
        
        # Add tabs
        self.tab_widget.addTab(general_tab, "General")
        self.tab_widget.addTab(translation_tab, "Translation")
        self.tab_widget.addTab(about_tab, "About")
        
        main_layout.addWidget(self.tab_widget)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_preferences)
        button_box.rejected.connect(self.reject)
        
        main_layout.addWidget(button_box)
        
        # Load current preferences
        self.load_preferences()
    
    def load_preferences(self):
        """Load current application preferences"""
        try:
            # Load theme with fallback
            current_theme = getattr(self.parent(), 'current_theme', 'Dark')
            self.theme_combo.setCurrentText(current_theme)
            
            # Load other preferences from config
            config = self.parent().load_config()
            
            # Set language
            default_language = config.get('default_language', 'English')
            self.language_combo.setCurrentText(default_language)
            
            # Set translation method
            default_method = config.get('translation_method', 'GoogleTrans')
            self.method_combo.setCurrentText(default_method)
            
            # Set chunk size
            default_chunk_size = config.get('translation_chunk_size', 500)
            self.chunk_spin.setValue(default_chunk_size)
        
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
            # Set default values if loading fails
            self.theme_combo.setCurrentText('Light')
            self.language_combo.setCurrentText('English')
            self.method_combo.setCurrentText('GoogleTrans')
            self.chunk_spin.setValue(500)

    def on_theme_changed(self, theme):
        """Handle theme change preview"""
        try:
            if theme == "Light":
                self.parent().setStyleSheet(LIGHT_STYLE)
            elif theme == "Dark":
                self.parent().setStyleSheet(DARK_STYLE)
            else:
                # System default
                self.parent().setStyleSheet("")
        except Exception as e:
            logger.error(f"Theme change error: {e}")
    
    def save_preferences(self):
        """Save selected preferences"""
        try:
            # Prepare config dictionary
            config = {
                'theme': self.theme_combo.currentText(),
                'default_language': self.language_combo.currentText(),
                'translation_method': self.method_combo.currentText(),
                'translation_chunk_size': self.chunk_spin.value()
            }
            
            # Save configuration
            self.parent().save_config(config)
            
            # Apply theme
            theme = config['theme']
            if theme == "Light":
                self.parent().setStyleSheet(LIGHT_STYLE)
            elif theme == "Dark":
                self.parent().setStyleSheet(DARK_STYLE)
            else:
                self.parent().setStyleSheet("")
            
            # Close dialog
            self.accept()
        
        except Exception as e:
            logger.error(f"Preferences save error: {e}")
            QMessageBox.warning(
                self, 
                "Save Error", 
                f"Could not save preferences: {e}"
            )

class MainWindow(QMainWindow):
    def __init__(self, subtitle_service: SubtitleService, preferences: JsonUserPreferences):
        super().__init__(None, Qt.WindowType.Window)
        
        # Extensive logging
        logger.debug("MainWindow initialization STARTED")
        
        # Store services
        self.subtitle_service = subtitle_service
        self.preferences = preferences
        self.animations = WidgetAnimations()
        
        # Set window icon
        icon_path = os.path.join('assets', 'logo.jpg')
        self.setWindowIcon(QIcon(icon_path))
        
        # Initialize current theme
        self.current_theme = 'Dark'
        
        # Set window properties
        self.setWindowTitle("AI Video Captions")
        
        # Get screen dimensions
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        # Set window size and position
        window_width = int(screen_geometry.width() * 0.8)
        window_height = int(screen_geometry.height() * 0.7)
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        
        self.setGeometry(x, y, window_width, window_height)
        
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # Create central widget
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Create toolbar with preferences action
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        preferences_action = toolbar.addAction("Preferences")
        preferences_action.triggered.connect(self.show_preferences)
        
        # Main processing UI
        self.create_main_processing_ui(central_layout)
        
        # Initialize progress timer
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        
        logger.debug("MainWindow initialization COMPLETED")

    def show_preferences(self):
        """Show preferences dialog in a non-blocking manner"""
        try:
            # Create preferences dialog
            preferences_dialog = PreferencesDialog(self)
            
            # Use QDialog.open() for non-blocking dialog
            preferences_dialog.open()
        
        except Exception as e:
            logger.error(f"Preferences dialog error: {e}")
            QMessageBox.warning(
                self, 
                "Preferences Error", 
                f"Could not open preferences: {e}"
            )

    def create_main_processing_ui(self, central_layout):
        """Create a modern, responsive UI for video processing"""
        # Main container for processing elements
        processing_container = QWidget()
        processing_layout = QVBoxLayout(processing_container)
        processing_layout.setContentsMargins(20, 20, 20, 20)
        processing_layout.setSpacing(15)

        # Top section: Video selection and processing options
        top_section = QHBoxLayout()
        
        # Video selection area
        video_selection_group = QGroupBox("Video Selection")
        video_selection_layout = QVBoxLayout()
        
        # File path input
        file_input_layout = QHBoxLayout()
        self.video_path_input = QLineEdit()
        self.video_path_input.setPlaceholderText("Select video file...")
        self.video_path_input.setReadOnly(True)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_video)
        self.browse_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogStart))
        
        file_input_layout.addWidget(self.video_path_input)
        file_input_layout.addWidget(self.browse_button)
        
        video_selection_layout.addLayout(file_input_layout)
        video_selection_group.setLayout(video_selection_layout)
        
        # Processing options area
        processing_options_group = QGroupBox("Processing Options")
        processing_options_layout = QGridLayout()
        
        # Language selection
        language_label = QLabel("Target Language:")
        self.target_language_combo = QComboBox()
        self.target_language_combo.addItems([
            "en English", "es Spanish", "fr French", 
            "de German", "it Italian", "pt Portuguese", "ar Arabic"
        ])
        
        # Translation method selection
        method_label = QLabel("Translation Method:")
        self.translation_method_combo = QComboBox()
        self.translation_method_combo.addItems([
            "GoogleTrans", "Argos Translate"
        ])
        
        processing_options_layout.addWidget(language_label, 0, 0)
        processing_options_layout.addWidget(self.target_language_combo, 0, 1)
        processing_options_layout.addWidget(method_label, 1, 0)
        processing_options_layout.addWidget(self.translation_method_combo, 1, 1)
        
        processing_options_group.setLayout(processing_options_layout)
        
        # Combine top section
        top_section.addWidget(video_selection_group)
        top_section.addWidget(processing_options_group)
        
        # Progress and results section
        progress_results_layout = QVBoxLayout()
        
        # Progress bar with status
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% - Processing")
        
        progress_layout.addWidget(self.progress_bar)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Subtitle and processing results will appear here...")
        
        # Process button
        self.process_button = QPushButton("Process Video")
        self.process_button.clicked.connect(self.process_video)
        self.process_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        
        # Export SRT button
        self.export_srt_button = QPushButton("Export SRT")
        self.export_srt_button.clicked.connect(self.export_subtitles_to_srt)
        self.export_srt_button.setEnabled(False)  # Disable until subtitles are generated
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.process_button)
        buttons_layout.addWidget(self.export_srt_button)
        
        # Add to progress and results layout
        progress_results_layout.addLayout(progress_layout)
        progress_results_layout.addWidget(self.results_text)
        progress_results_layout.addLayout(buttons_layout)
        
        # Combine all sections
        processing_layout.addLayout(top_section)
        processing_layout.addLayout(progress_results_layout)
        
        # Add to central layout
        central_layout.addWidget(processing_container)

    def select_video(self):
        """Select video file"""
        try:
            # Open file dialog to select video
            file_dialog = QFileDialog()
            video_path, _ = file_dialog.getOpenFileName(
                self, 
                "Select Video File", 
                "", 
                "Video Files (*.mp4 *.avi *.mov *.mkv)"
            )
            
            if not video_path:
                return  # User cancelled
            
            # Update video path input
            self.video_path_input.setText(video_path)
            
            # Reset UI elements
            self.results_text.clear()
            self.progress_bar.setValue(0)
            
            # Disable export SRT button
            self.export_srt_button.setEnabled(False)
        
        except Exception as e:
            ErrorHandler.show_error_message(
                self, 
                "Video Selection Error", 
                "Failed to select video file",
                str(traceback.format_exc())
            )

    def process_video(self):
        """Start video processing"""
        try:
            # Get video path from input
            video_path = self.video_path_input.text()
            
            if not video_path or not os.path.exists(video_path):
                QMessageBox.warning(
                    self, 
                    "Processing Error", 
                    "Please select a valid video file first."
                )
                return
            
            # Extract language code from selection
            selected_lang = self.target_language_combo.currentText().split()[0]
            selected_method = self.translation_method_combo.currentText()
            
            # Reset UI
            self.results_text.clear()
            self.progress_bar.setValue(0)
            
            # Start video processing in a separate thread
            self.processing_thread = VideoProcessingThread(
                self.subtitle_service, 
                video_path, 
                selected_lang,
                selected_method
            )
            
            # Connect thread signals
            self.processing_thread.processing_complete.connect(self.on_processing_complete)
            self.processing_thread.processing_error.connect(self.on_processing_error)
            
            # Start processing
            self.processing_thread.start()
        
        except Exception as e:
            ErrorHandler.show_error_message(
                self, 
                "Video Processing Error", 
                "Failed to process selected video",
                str(traceback.format_exc())
            )

    def update_progress(self):
        """Update progress bar dynamically"""
        current_value = self.progress_bar.value()
        if current_value < 100:
            # Increment progress
            new_value = min(current_value + 5, 100)
            self.progress_bar.setValue(new_value)
            
            # Update status text
            status_text = {
                0: "Initializing...",
                20: "Extracting audio...",
                40: "Transcribing audio...",
                60: "Translating subtitles...",
                80: "Finalizing...",
                100: "Processing complete!"
            }.get(new_value, "Processing...")
            
            self.progress_bar.setFormat(f"%p% - {status_text}")
        else:
            # Stop timer when progress is complete
            if hasattr(self, 'progress_timer'):
                self.progress_timer.stop()

    def on_processing_complete(self, result):
        """Handle successful video processing"""
        try:
            # Stop progress timer if it exists
            if hasattr(self, 'progress_timer'):
                self.progress_timer.stop()
            
            # Update progress bar
            self.progress_bar.setValue(100)
            
            # Log processing result details
            logger.debug(f"Processing Result Status: {result.status}")
            logger.debug(f"Processing Result Message: {result.message}")
            
            if result.status == ProcessingStatus.COMPLETED and result.subtitles:
                # Store subtitles for potential export
                self.last_processed_subtitles = result.subtitles
                
                # Enable SRT export button
                self.export_srt_button.setEnabled(True)
                
                # Display subtitles in results text
                subtitle_text = "\n".join([
                    f"{subtitle.start_time} --> {subtitle.end_time}: {subtitle.text}" 
                    for subtitle in result.subtitles
                ])
                self.results_text.setText(f"Processing completed successfully!\n\nSubtitles:\n{subtitle_text}")
                
                # Show success notification
                QMessageBox.information(
                    self, 
                    "Processing Complete", 
                    f"Video processing finished successfully!\nGenerated {len(result.subtitles)} subtitles."
                )
            else:
                # Disable SRT export button
                self.export_srt_button.setEnabled(False)
                
                # Handle cases where no subtitles were generated
                self.results_text.setText(f"Processing result: {result.message}")
                QMessageBox.warning(
                    self, 
                    "Processing Incomplete", 
                    f"No subtitles were generated. Reason: {result.message}"
                )
        
        except Exception as e:
            ErrorHandler.show_error_message(
                self, 
                "Result Handling Error", 
                "Failed to process video result",
                str(traceback.format_exc())
            )

    def on_processing_error(self, error_message, error_traceback):
        """Handle processing errors"""
        try:
            self.progress_timer.stop()
            self.progress_bar.setValue(0)
            
            # Log the full error
            logger.error(f"Video processing error: {error_message}")
            logger.error(error_traceback)
            
            # Show detailed error message
            ErrorHandler.show_error_message(
                self, 
                "Video Processing Error", 
                f"Failed to process video: {error_message}",
                error_traceback
            )
            
            self.results_text.setText(f"Error occurred: {error_message}")
        
        except Exception as e:
            # Fallback error handling
            QMessageBox.critical(
                self, 
                "Critical Error", 
                f"Failed to handle processing error: {e}"
            )

    def load_preferences(self):
        """Load and apply user preferences"""
        try:
            # Load preferences
            current_prefs = self.preferences.load_preferences()
            
            # Language mapping
            lang_map = {
                "en": 0, "es": 1, "fr": 2, 
                "de": 3, "it": 4, "pt": 5, "ar": 6
            }
            
            # Get default language
            default_lang = current_prefs.get("default_language", "en")
            
            # Apply theme
            theme = current_prefs.get("theme", "light")
            self.apply_theme(theme)
            
            # Update language selection if combos exist
            if hasattr(self, 'target_language_combo'):
                self.target_language_combo.setCurrentIndex(
                    lang_map.get(default_lang, 0)
                )
        
        except Exception as e:
            ErrorHandler.show_error_message(
                self, 
                "Preferences Load Error", 
                "Failed to load preferences",
                str(traceback.format_exc())
            )

    def apply_theme(self, theme):
        """Apply theme to the application"""
        if theme == "dark":
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet(LIGHT_STYLE)

    def load_config(self):
        """Load application configuration"""
        try:
            # Default configuration
            default_config = {
                'theme': 'Light',
                'default_language': 'English',
                'translation_method': 'GoogleTrans',
                'translation_chunk_size': 500
            }
            
            # Check if config file exists
            config_path = os.path.join(
                os.path.expanduser('~'), 
                '.video_captions_config.json'
            )
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    saved_config = json.load(f)
                    # Merge saved config with defaults
                    default_config.update(saved_config)
            
            return default_config
        
        except Exception as e:
            logger.error(f"Config load error: {e}")
            return {
                'theme': 'Light',
                'default_language': 'English',
                'translation_method': 'GoogleTrans',
                'translation_chunk_size': 500
            }

    def save_config(self, config):
        """Save application configuration"""
        try:
            # Determine config file path
            config_path = os.path.join(
                os.path.expanduser('~'), 
                '.video_captions_config.json'
            )
            
            # Save configuration
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            logger.info("Configuration saved successfully")
        
        except Exception as e:
            logger.error(f"Config save error: {e}")
            QMessageBox.warning(
                self, 
                "Save Error", 
                f"Could not save configuration: {e}"
            )

    def apply_preferences(self):
        """Apply saved preferences"""
        try:
            config = self.load_config()
            
            # Apply theme
            theme = config.get('theme', 'Light')
            if theme == "Light":
                self.setStyleSheet(LIGHT_STYLE)
            elif theme == "Dark":
                self.setStyleSheet(DARK_STYLE)
            else:
                self.setStyleSheet("")
            
            # Store current theme for reference
            self.current_theme = theme
        
        except Exception as e:
            logger.error(f"Preferences application error: {e}")

    def export_subtitles_to_srt(self):
        """Export generated subtitles to SRT file"""
        try:
            # Check if subtitles exist
            if not hasattr(self, 'last_processed_subtitles') or not self.last_processed_subtitles:
                QMessageBox.warning(self, "Export Error", "No subtitles to export.")
                return
            
            # Open file dialog to choose save location
            srt_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Export Subtitles", 
                "", 
                "SRT Files (*.srt)"
            )
            
            if not srt_path:
                return  # User cancelled
            
            # Use terminal debugger to export SRT
            from infrastructure.terminal_debugger import TerminalDebugger
            
            success = TerminalDebugger.export_subtitles_to_srt(
                self.last_processed_subtitles, 
                srt_path
            )
            
            if success:
                QMessageBox.information(
                    self, 
                    "Export Successful", 
                    f"Subtitles exported to {srt_path}"
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Export Failed", 
                    "Could not export subtitles"
                )
        
        except Exception as e:
            ErrorHandler.show_error_message(
                self, 
                "Export Error", 
                "Failed to export subtitles",
                str(traceback.format_exc())
            )

def run_diagnostic():
    logger.debug("Starting diagnostic application")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show window
    window = MainWindow(SubtitleService(), JsonUserPreferences())
    
    logger.debug("Calling window.show()")
    window.show()
    
    logger.debug("Calling window.raise_()")
    window.raise_()
    
    logger.debug("Calling window.activateWindow()")
    window.activateWindow()
    
    logger.debug("Starting app.exec()")
    exit_code = app.exec()
    
    logger.debug(f"Application exited with code: {exit_code}")
    return exit_code

if __name__ == "__main__":
    run_diagnostic()
