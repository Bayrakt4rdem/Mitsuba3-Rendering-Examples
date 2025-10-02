"""
Home/Welcome tab with app information and global settings
"""

from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QGroupBox, QFormLayout,
    QSpinBox, QComboBox, QCheckBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from gui.tabs.base_tab import BaseTab
from gui.core.config import AppConfig
from typing import Dict, Any
from loguru import logger


class HomeTab(BaseTab):
    """Home tab with welcome message and global settings"""
    
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, config: AppConfig, parent=None):
        self.config = config
        super().__init__("Home", parent)
    
    def setup_ui(self):
        """Setup the home tab UI"""
        # Hide render controls for home tab
        self.render_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress_bar.setVisible(False)
        
        # Welcome section
        welcome_group = QGroupBox("Welcome to Mitsuba 3 Render Studio")
        welcome_layout = QVBoxLayout()
        
        title = QLabel("🎨 Mitsuba 3 Render Studio")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4ec9b0; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel(
            "A professional interface for learning and experimenting with Mitsuba 3 rendering.\n\n"
            "Features:\n"
            "• Interactive parameter controls for all scenes\n"
            "• Real-time rendering with progress tracking\n"
            "• Multiple demo scenes (Basic, Materials, Lighting, Cornell Box)\n"
            "• Built-in image viewer and log console\n"
            "• Dark Fusion theme for comfortable viewing\n\n"
            "Select a scene tab to get started!"
        )
        description.setStyleSheet("color: #d4d4d4; padding: 10px; line-height: 1.6;")
        description.setWordWrap(True)
        
        welcome_layout.addWidget(title)
        welcome_layout.addWidget(description)
        welcome_group.setLayout(welcome_layout)
        
        # Global settings section
        settings_group = QGroupBox("Global Rendering Settings")
        settings_layout = QFormLayout()
        
        # Resolution
        resolution_layout = QHBoxLayout()
        self.width_spin = QSpinBox()
        self.width_spin.setRange(100, 4096)
        self.width_spin.setValue(self.config.default_resolution[0])
        self.width_spin.setSuffix(" px")
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(100, 4096)
        self.height_spin.setValue(self.config.default_resolution[1])
        self.height_spin.setSuffix(" px")
        
        resolution_layout.addWidget(QLabel("Width:"))
        resolution_layout.addWidget(self.width_spin)
        resolution_layout.addWidget(QLabel("Height:"))
        resolution_layout.addWidget(self.height_spin)
        resolution_layout.addStretch()
        
        settings_layout.addRow("Default Resolution:", resolution_layout)
        
        # Samples per pixel
        self.spp_spin = QSpinBox()
        self.spp_spin.setRange(1, 10000)
        self.spp_spin.setValue(self.config.default_spp)
        self.spp_spin.setSuffix(" samples")
        self.spp_spin.setToolTip("Higher values = better quality but slower rendering")
        settings_layout.addRow("Samples per Pixel:", self.spp_spin)
        
        # Variant
        self.variant_combo = QComboBox()
        self.variant_combo.addItems([
            "scalar_rgb", "scalar_spectral", 
            "llvm_rgb", "llvm_spectral",
            "cuda_rgb", "cuda_spectral"
        ])
        self.variant_combo.setCurrentText(self.config.default_variant)
        self.variant_combo.setToolTip("Rendering backend variant")
        settings_layout.addRow("Rendering Variant:", self.variant_combo)
        
        # Auto-scroll logs
        self.auto_scroll_check = QCheckBox()
        self.auto_scroll_check.setChecked(self.config.enable_auto_scroll)
        settings_layout.addRow("Auto-scroll Logs:", self.auto_scroll_check)
        
        # Apply button
        apply_btn = QPushButton("Apply Settings")
        apply_btn.clicked.connect(self._apply_settings)
        apply_btn.setMinimumHeight(30)
        settings_layout.addRow("", apply_btn)
        
        settings_group.setLayout(settings_layout)
        
        # Add to content layout
        self.content_layout.addWidget(welcome_group)
        self.content_layout.addWidget(settings_group)
        self.content_layout.addStretch()
    
    def _apply_settings(self):
        """Apply and save global settings"""
        settings = {
            'resolution': (self.width_spin.value(), self.height_spin.value()),
            'spp': self.spp_spin.value(),
            'variant': self.variant_combo.currentText(),
            'auto_scroll': self.auto_scroll_check.isChecked()
        }
        
        # Update config
        self.config.default_resolution = settings['resolution']
        self.config.default_spp = settings['spp']
        self.config.default_variant = settings['variant']
        self.config.enable_auto_scroll = settings['auto_scroll']
        
        logger.info(f"Settings applied: {settings}")
        self.settings_changed.emit(settings)
        self.log_message.emit("✅ Settings applied successfully")
    
    def get_current_settings(self) -> Dict[str, Any]:
        """Get current settings values"""
        return {
            'resolution': (self.width_spin.value(), self.height_spin.value()),
            'spp': self.spp_spin.value(),
            'variant': self.variant_combo.currentText(),
            'auto_scroll': self.auto_scroll_check.isChecked()
        }
    
    # Required by BaseTab (not used for Home tab)
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {}
    
    def get_default_params(self) -> Dict[str, Any]:
        return {}
