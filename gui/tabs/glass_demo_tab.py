"""
Glass Demo Tab - Interactive transparent material and caustics controls
"""

from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget
from gui_examples.glass_demo import GlassDemoGenerator
from typing import Dict, Any
from loguru import logger


class GlassDemoTab(BaseTab):
    """Tab for experimenting with glass and transparent materials"""
    
    def __init__(self, parent=None):
        self.scene_gen = GlassDemoGenerator()
        super().__init__("Glass & Transparency", parent)
    
    def setup_ui(self):
        """Setup the tab UI with parameter controls"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Educational info
        info = QLabel(
            "<b>Glass and Transparent Materials</b><br><br>"
            "<b>Index of Refraction (IOR):</b> How much light bends<br>"
            "• Water: 1.33 | Glass: 1.5 | Diamond: 2.42<br><br>"
            "<b>Caustics:</b> Focused light patterns from curved glass<br>"
            "<b>Refraction:</b> Light bending through transparent materials<br><br>"
            "Higher IOR = more bending, stronger caustics!<br>"
            "Requires more samples for clean results (512+ SPP recommended)"
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            "color: #4ec9b0; padding: 10px; "
            "background: #2d2d2d; border-radius: 5px; "
            "line-height: 1.4;"
        )
        scroll_layout.addWidget(info)
        
        # Glass object selection
        self.object_params = ParameterWidget("Glass Object")
        self.object_params.add_choice_parameter(
            'type', 'Glass Shape:',
            choices=['sphere', 'cube', 'cylinder', 'wine_glass'],
            default='sphere',
            tooltip=(
                "sphere: Beautiful caustics (lens effect)\n"
                "cube: Flat refraction\n"
                "cylinder: Line caustics\n"
                "wine_glass: Complex caustics"
            )
        )
        
        # Glass properties
        self.glass_params = ParameterWidget("Glass Properties")
        self.glass_params.add_float_parameter(
            'ior', 'Index of Refraction:', default=1.5, min_val=1.0, max_val=2.5,
            decimals=2, step=0.05,
            tooltip=(
                "1.0 = Air (no bending)\n"
                "1.33 = Water\n"
                "1.5 = Standard glass\n"
                "1.9 = Dense glass\n"
                "2.42 = Diamond"
            )
        )
        
        # Glass tint (color)
        self.tint_params = ParameterWidget("Glass Tint")
        self.tint_params.add_slider_parameter(
            'tint_r', 'Red Tint:', default=100, min_val=50, max_val=100,
            tooltip="Red component (100=clear, <100=absorbs red)"
        )
        self.tint_params.add_slider_parameter(
            'tint_g', 'Green Tint:', default=100, min_val=50, max_val=100,
            tooltip="Green component (100=clear, <100=absorbs green)"
        )
        self.tint_params.add_slider_parameter(
            'tint_b', 'Blue Tint:', default=100, min_val=50, max_val=100,
            tooltip="Blue component (100=clear, <100=absorbs blue)"
        )
        
        # Lighting
        self.light_params = ParameterWidget("Lighting")
        self.light_params.add_slider_parameter(
            'intensity', 'Light Intensity:', default=20, min_val=5, max_val=50,
            tooltip="Brightness of main light"
        )
        self.light_params.add_float_parameter(
            'height', 'Light Height:', default=5.0, min_val=2.0, max_val=8.0,
            step=0.5, tooltip="Height of light (affects caustic pattern)"
        )
        
        # Background
        self.bg_params = ParameterWidget("Background")
        self.bg_params.add_choice_parameter(
            'type', 'Background Type:',
            choices=['white', 'checker', 'gradient'],
            default='white',
            tooltip=(
                "white: Best for caustics\n"
                "checker: Shows refraction distortion\n"
                "gradient: Atmospheric"
            )
        )
        self.bg_params.add_bool_parameter(
            'show_caustics', 'Show Caustic Plane:', default=True,
            tooltip="Add white plane to catch light caustics"
        )
        
        # Add to layout
        scroll_layout.addWidget(self.object_params)
        scroll_layout.addWidget(self.glass_params)
        scroll_layout.addWidget(self.tint_params)
        scroll_layout.addWidget(self.light_params)
        scroll_layout.addWidget(self.bg_params)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        self.content_layout.addWidget(scroll)
    
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build the scene dictionary from current parameters"""
        object_params = self.object_params.get_parameters()
        glass_params = self.glass_params.get_parameters()
        tint_params = self.tint_params.get_parameters()
        light_params = self.light_params.get_parameters()
        bg_params = self.bg_params.get_parameters()
        
        scene_params_dict = {
            'width': params.get('width', 800),
            'height': params.get('height', 600),
            'glass_type': object_params['type'],
            'glass_ior': glass_params['ior'],
            'glass_tint': (
                tint_params['tint_r'] / 100.0,
                tint_params['tint_g'] / 100.0,
                tint_params['tint_b'] / 100.0
            ),
            'light_intensity': float(light_params['intensity']),
            'light_height': light_params['height'],
            'background_type': bg_params['type'],
            'show_caustics': bg_params['show_caustics'],
        }
        
        logger.debug(f"Glass demo: type={object_params['type']}, IOR={glass_params['ior']}")
        return self.scene_gen.generate(scene_params_dict)
    
    def get_default_params(self) -> Dict[str, Any]:
        """Return default rendering parameters"""
        # Glass needs more samples for clean results
        return {
            'spp': 512,  # Higher for glass/caustics
            'integrator': 'path',
            'variant': 'scalar_rgb'
        }
    
    def get_output_filename(self) -> str:
        """Custom output filename"""
        glass_type = self.object_params.get_parameters()['type']
        ior = self.glass_params.get_parameters()['ior']
        return f"glass_{glass_type}_ior{ior:.2f}.png"
