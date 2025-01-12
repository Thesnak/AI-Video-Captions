LIGHT_STYLE = """
QMainWindow {
    background-color: #f0f0f0;
}

QPushButton {
    background-color: #0078D4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106EBE;
}

QPushButton:disabled {
    background-color: #CCE4F7;
}

QProgressBar {
    border: 2px solid #0078D4;
    border-radius: 4px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #0078D4;
}

QComboBox {
    padding: 6px;
    border: 1px solid #999;
    border-radius: 4px;
}

QTextEdit {
    border: 1px solid #999;
    border-radius: 4px;
    padding: 4px;
    background-color: white;
}

QLabel {
    color: #333;
}
"""

DARK_STYLE = """
QMainWindow {
    background-color: #1E1E1E;
}

QPushButton {
    background-color: #0078D4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106EBE;
}

QPushButton:disabled {
    background-color: #333;
    color: #666;
}

QProgressBar {
    border: 2px solid #0078D4;
    border-radius: 4px;
    text-align: center;
    color: white;
}

QProgressBar::chunk {
    background-color: #0078D4;
}

QComboBox {
    padding: 6px;
    border: 1px solid #666;
    border-radius: 4px;
    background-color: #333;
    color: white;
}

QTextEdit {
    border: 1px solid #666;
    border-radius: 4px;
    padding: 4px;
    background-color: #252525;
    color: white;
}

QLabel {
    color: white;
}
"""
