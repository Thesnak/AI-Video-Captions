from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QListWidget, QLabel, QSpinBox, QProgressBar)
from PyQt6.QtCore import pyqtSignal
import pathlib

class BatchProcessingWidget(QWidget):
    process_batch = pyqtSignal(list, str)  # files, target_language

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.files = []

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # File list
        self.file_list = QListWidget()
        layout.addWidget(QLabel("Selected Files:"))
        layout.addWidget(self.file_list)

        # Controls
        controls_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.add_files)
        
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_files)
        
        self.concurrent_label = QLabel("Concurrent Tasks:")
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 5)
        self.concurrent_spin.setValue(3)
        
        controls_layout.addWidget(self.add_files_btn)
        controls_layout.addWidget(self.clear_btn)
        controls_layout.addWidget(self.concurrent_label)
        controls_layout.addWidget(self.concurrent_spin)
        
        layout.addLayout(controls_layout)

        # Batch progress
        self.batch_progress = QProgressBar()
        layout.addWidget(self.batch_progress)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mkv)"
        )
        for file in files:
            if file not in self.files:
                self.files.append(file)
                self.file_list.addItem(pathlib.Path(file).name)
        
        self.update_progress()

    def clear_files(self):
        self.files.clear()
        self.file_list.clear()
        self.update_progress()

    def update_progress(self):
        self.batch_progress.setMaximum(len(self.files))
        self.batch_progress.setValue(0)
