"""
Log viewer widget with terminal-like appearance
"""

from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QTextCursor, QFont, QColor
from loguru import logger


class LogViewer(QWidget):
    """Terminal-style log viewer with color support"""
    
    def __init__(self, max_lines: int = 1000, parent=None):
        super().__init__(parent)
        self.max_lines = max_lines
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Log text area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        # Terminal-style font
        font = QFont("Consolas", 9)
        if not font.exactMatch():
            font = QFont("Courier New", 9)
        self.text_edit.setFont(font)
        
        # Dark background for terminal feel
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                padding: 5px;
            }
        """)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Clear Logs")
        self.clear_btn.clicked.connect(self.clear)
        self.clear_btn.setMaximumWidth(100)
        
        self.auto_scroll_btn = QPushButton("Auto-scroll: ON")
        self.auto_scroll_btn.setCheckable(True)
        self.auto_scroll_btn.setChecked(True)
        self.auto_scroll_btn.clicked.connect(self._toggle_auto_scroll)
        self.auto_scroll_btn.setMaximumWidth(120)
        
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.auto_scroll_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addWidget(self.text_edit)
        
        self.auto_scroll = True
    
    def _toggle_auto_scroll(self):
        """Toggle auto-scroll feature"""
        self.auto_scroll = self.auto_scroll_btn.isChecked()
        self.auto_scroll_btn.setText(f"Auto-scroll: {'ON' if self.auto_scroll else 'OFF'}")
    
    @pyqtSlot(str)
    def append_log(self, message: str):
        """
        Append a log message with HTML formatting support
        
        Args:
            message: Log message (can contain HTML color tags)
        """
        # Move cursor to end
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.text_edit.setTextCursor(cursor)
        
        # Append message
        self.text_edit.insertHtml(message + "<br>")
        
        # Limit lines
        self._limit_lines()
        
        # Auto-scroll to bottom
        if self.auto_scroll:
            self.text_edit.verticalScrollBar().setValue(
                self.text_edit.verticalScrollBar().maximum()
            )
    
    def _limit_lines(self):
        """Keep only the last max_lines"""
        doc = self.text_edit.document()
        while doc.blockCount() > self.max_lines:
            cursor = QTextCursor(doc.firstBlock())
            cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()  # Remove the newline
    
    @pyqtSlot()
    def clear(self):
        """Clear all log messages"""
        self.text_edit.clear()
        logger.debug("Log viewer cleared")
    
    def log_info(self, message: str):
        """Log an info message"""
        html = f'<span style="color: #4ec9b0;">[INFO]</span> {message}'
        self.append_log(html)
    
    def log_warning(self, message: str):
        """Log a warning message"""
        html = f'<span style="color: #dcdcaa;">[WARN]</span> {message}'
        self.append_log(html)
    
    def log_error(self, message: str):
        """Log an error message"""
        html = f'<span style="color: #f48771;">[ERROR]</span> {message}'
        self.append_log(html)
    
    def log_success(self, message: str):
        """Log a success message"""
        html = f'<span style="color: #6a9955;">[SUCCESS]</span> {message}'
        self.append_log(html)
