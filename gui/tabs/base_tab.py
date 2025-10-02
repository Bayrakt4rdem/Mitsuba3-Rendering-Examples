"""
Base tab interface for all scene tabs
"""

from abc import ABCMeta, abstractmethod
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QProgressBar
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any
from loguru import logger


# Create a metaclass that combines QWidget's metaclass and ABCMeta
class QABCMeta(type(QWidget), ABCMeta):
    """Metaclass that combines Qt and ABC metaclasses"""
    pass


class BaseTab(QWidget, metaclass=QABCMeta):
    """
    Abstract base class for all scene tabs
    Provides common functionality and interface
    """
    
    render_requested = pyqtSignal(dict, dict, str)  # scene_dict, params, output_name
    log_message = pyqtSignal(str)
    
    def __init__(self, tab_name: str, parent=None):
        super().__init__(parent)
        self.tab_name = tab_name
        self._is_rendering = False
        self._setup_base_ui()
    
    def _setup_base_ui(self):
        """Setup base UI components common to all tabs"""
        self.main_layout = QVBoxLayout(self)
        
        # Subclass will add content here via setup_ui()
        self.content_layout = QVBoxLayout()
        self.main_layout.addLayout(self.content_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.main_layout.addWidget(self.progress_bar)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.render_btn = QPushButton("🎨 Render Scene")
        self.render_btn.clicked.connect(self._on_render_clicked)
        self.render_btn.setMinimumHeight(35)
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel_clicked)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setMaximumWidth(100)
        
        button_layout.addWidget(self.render_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        
        self.main_layout.addLayout(button_layout)
        
        # Call subclass setup
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """Subclass must implement this to setup custom UI"""
        pass
    
    @abstractmethod
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Subclass must implement this to return Mitsuba scene dictionary
        
        Args:
            params: Parameter values from UI
            
        Returns:
            Mitsuba scene dictionary
        """
        pass
    
    @abstractmethod
    def get_default_params(self) -> Dict[str, Any]:
        """
        Subclass must implement this to return default rendering parameters
        
        Returns:
            Dictionary with default parameters (spp, variant, etc.)
        """
        pass
    
    def get_output_filename(self) -> str:
        """Get the output filename for this scene (can be overridden)"""
        return f"{self.tab_name.lower().replace(' ', '_')}.png"
    
    def _on_render_clicked(self):
        """Handle render button click"""
        try:
            # Get parameters
            params = self.get_default_params()
            
            # Get scene
            scene_dict = self.get_scene_dict(params)
            
            # Get output filename
            output_name = self.get_output_filename()
            
            # Emit render request
            self.render_requested.emit(scene_dict, params, output_name)
            
            # Update UI
            self.set_rendering_state(True)
            
            logger.info(f"Render requested: {self.tab_name}")
            self.log_message.emit(f"🎨 Starting render: {self.tab_name}")
            
        except Exception as e:
            error_msg = f"Failed to prepare scene: {str(e)}"
            logger.error(error_msg)
            self.log_message.emit(f"❌ Error: {error_msg}")
    
    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        logger.info(f"Cancel requested: {self.tab_name}")
        self.log_message.emit(f"⏹️  Cancelling render: {self.tab_name}")
        # Parent window will handle actual cancellation
    
    def set_rendering_state(self, is_rendering: bool):
        """Update UI for rendering state"""
        self._is_rendering = is_rendering
        self.render_btn.setEnabled(not is_rendering)
        self.cancel_btn.setEnabled(is_rendering)
        
        if is_rendering:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
        else:
            self.progress_bar.setVisible(False)
    
    def update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def on_render_complete(self):
        """Called when rendering completes"""
        self.set_rendering_state(False)
        logger.debug(f"Render complete: {self.tab_name}")
    
    def on_render_failed(self, error: str):
        """Called when rendering fails"""
        self.set_rendering_state(False)
        logger.error(f"Render failed: {self.tab_name} - {error}")
