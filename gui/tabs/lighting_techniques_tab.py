"""
Lighting Techniques Tab - Interactive professional lighting setup controls
"""

from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget
from gui_examples.lighting_techniques import LightingTechniquesGenerator
from typing import Dict, Any
from loguru import logger


class LightingTechniquesTab(BaseTab):
    """Tab for experimenting with professional lighting techniques"""
    
    def __init__(self, parent=None):
        self.scene_gen = LightingTechniquesGenerator()
        super().__init__("Lighting Techniques", parent)
    
    def setup_ui(self):
        """Setup the tab UI with parameter controls"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Educational info
        info = QLabel(
            "<b>Professional Lighting Techniques</b><br><br>"
            "<b>Three-Point:</b> Classic studio setup (key + fill + rim)<br>"
            "<b>Dramatic:</b> Single strong light for high contrast<br>"
            "<b>Soft:</b> Large soft lights for even illumination<br>"
            "<b>Rim:</b> Strong backlight for silhouettes<br>"
            "<b>Top:</b> Overhead lighting (mysterious mood)<br><br>"
            "Experiment with different setups to see how lighting affects mood!"
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            "color: #4ec9b0; padding: 10px; "
            "background: #2d2d2d; border-radius: 5px; "
            "line-height: 1.4;"
        )
        scroll_layout.addWidget(info)
        
        # Lighting setup selection
        self.setup_params = ParameterWidget("Lighting Setup")
        self.setup_params.add_choice_parameter(
            'technique',
            'Lighting Technique:',
            choices=['three_point', 'dramatic', 'soft', 'rim', 'top'],
            default='three_point',
            tooltip=(
                "three_point: Balanced studio lighting\n"
                "dramatic: High contrast, single light\n"
                "soft: Even, flattering light\n"
                "rim: Backlit silhouette\n"
                "top: Overhead mystery lighting"
            )
        )
        
        # Light intensity controls
        self.intensity_params = ParameterWidget("Light Intensities")
        self.intensity_params.add_slider_parameter(
            'key', 'Key Light:', default=30, min_val=5, max_val=100,
            tooltip="Main light strength (brightest)"
        )
        self.intensity_params.add_slider_parameter(
            'fill', 'Fill Light:', default=10, min_val=0, max_val=50,
            tooltip="Fill light reduces harsh shadows"
        )
        self.intensity_params.add_slider_parameter(
            'rim', 'Rim/Back Light:', default=20, min_val=0, max_val=100,
            tooltip="Rim light separates subject from background"
        )
        
        # Light positioning
        self.position_params = ParameterWidget("Light Position")
        self.position_params.add_float_parameter(
            'height', 'Light Height:', default=4.0, min_val=1.0, max_val=10.0,
            step=0.5, tooltip="Height of key light above ground"
        )
        self.position_params.add_float_parameter(
            'distance', 'Light Distance:', default=5.0, min_val=2.0, max_val=15.0,
            step=0.5, tooltip="Distance from subject to light"
        )
        
        # Object settings
        self.object_params = ParameterWidget("Subject")
        self.object_params.add_choice_parameter(
            'type', 'Object Type:',
            choices=['sphere', 'cube', 'both'],
            default='sphere',
            tooltip="What to illuminate"
        )
        self.object_params.add_choice_parameter(
            'material', 'Material:',
            choices=['diffuse', 'plastic', 'metal'],
            default='plastic',
            tooltip=(
                "diffuse: Matte surface\n"
                "plastic: Glossy highlights\n"
                "metal: Reflective"
            )
        )
        
        # Scene settings
        self.scene_params = ParameterWidget("Scene Settings")
        self.scene_params.add_slider_parameter(
            'background', 'Background:', default=20, min_val=0, max_val=100,
            tooltip="Background brightness (0=black, 100=white)"
        )
        
        # Add to layout
        scroll_layout.addWidget(self.setup_params)
        scroll_layout.addWidget(self.intensity_params)
        scroll_layout.addWidget(self.position_params)
        scroll_layout.addWidget(self.object_params)
        scroll_layout.addWidget(self.scene_params)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        self.content_layout.addWidget(scroll)
    
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build the scene dictionary from current parameters"""
        setup_params = self.setup_params.get_parameters()
        intensity_params = self.intensity_params.get_parameters()
        position_params = self.position_params.get_parameters()
        object_params = self.object_params.get_parameters()
        scene_params = self.scene_params.get_parameters()
        
        scene_params_dict = {
            'width': params.get('width', 800),
            'height': params.get('height', 600),
            'lighting_type': setup_params['technique'],
            'key_intensity': float(intensity_params['key']),
            'fill_intensity': float(intensity_params['fill']),
            'rim_intensity': float(intensity_params['rim']),
            'key_height': position_params['height'],
            'key_distance': position_params['distance'],
            'object_type': object_params['type'],
            'object_material': object_params['material'],
            'background_brightness': scene_params['background'] / 100.0,
        }
        
        logger.debug(f"Lighting technique: {setup_params['technique']}")
        return self.scene_gen.generate(scene_params_dict)
    
    def get_default_params(self) -> Dict[str, Any]:
        """Return default rendering parameters"""
        return {
            'spp': 256,
            'integrator': 'path',
            'variant': 'scalar_rgb'
        }
    
    def get_output_filename(self) -> str:
        """Custom output filename"""
        technique = self.setup_params.get_parameters()['technique']
        return f"lighting_{technique}.png"
