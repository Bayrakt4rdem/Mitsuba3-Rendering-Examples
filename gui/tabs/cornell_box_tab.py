"""
Cornell Box Tab - Interactive controls for the classic Cornell Box scene
"""

from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget
from gui_examples.cornell_box import CornellBoxGenerator
from typing import Dict, Any
from loguru import logger


class CornellBoxTab(BaseTab):
    """Tab for rendering the Cornell Box scene"""
    
    def __init__(self, parent=None):
        self.scene_gen = CornellBoxGenerator()
        super().__init__("Cornell Box", parent)
    
    def setup_ui(self):
        """Setup the tab UI with parameter controls"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Box parameters
        self.box_params = ParameterWidget("Cornell Box Settings")
        self.box_params.add_float_parameter(
            'box_size', 'Box Size:', default=2.0, min_val=1.0, max_val=5.0,
            step=0.1, tooltip="Size of the Cornell Box"
        )
        
        # Light parameters
        self.light_params = ParameterWidget("Lighting")
        self.light_params.add_slider_parameter(
            'intensity', 'Light Intensity:', default=15, min_val=1, max_val=50,
            tooltip="Brightness of the area light"
        )
        self.light_params.add_float_parameter(
            'light_size', 'Light Size:', default=0.5, min_val=0.1, max_val=1.5,
            step=0.1, tooltip="Size of the area light"
        )
        
        # Wall colors
        self.wall_params = ParameterWidget("Wall Colors")
        
        # Left wall (red)
        self.wall_params.add_slider_parameter(
            'left_r', 'Left Red:', default=63, min_val=0, max_val=100,
            tooltip="Red wall - Red component"
        )
        self.wall_params.add_slider_parameter(
            'left_g', 'Left Green:', default=6, min_val=0, max_val=100,
            tooltip="Red wall - Green component"
        )
        self.wall_params.add_slider_parameter(
            'left_b', 'Left Blue:', default=5, min_val=0, max_val=100,
            tooltip="Red wall - Blue component"
        )
        
        # Right wall (green)
        self.wall_params.add_slider_parameter(
            'right_r', 'Right Red:', default=14, min_val=0, max_val=100,
            tooltip="Green wall - Red component"
        )
        self.wall_params.add_slider_parameter(
            'right_g', 'Right Green:', default=45, min_val=0, max_val=100,
            tooltip="Green wall - Green component"
        )
        self.wall_params.add_slider_parameter(
            'right_b', 'Right Blue:', default=9, min_val=0, max_val=100,
            tooltip="Green wall - Blue component"
        )
        
        # Objects
        self.object_params = ParameterWidget("Scene Objects")
        self.object_params.add_float_parameter(
            'sphere_size', 'Sphere Size:', default=0.4, min_val=0.1, max_val=0.8,
            step=0.05, tooltip="Size of the metallic sphere"
        )
        self.object_params.add_float_parameter(
            'box_size', 'Box Size:', default=0.5, min_val=0.1, max_val=1.0,
            step=0.05, tooltip="Size of the white box"
        )
        
        # Add to layout
        scroll_layout.addWidget(self.box_params)
        scroll_layout.addWidget(self.light_params)
        scroll_layout.addWidget(self.wall_params)
        scroll_layout.addWidget(self.object_params)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        self.content_layout.addWidget(scroll)
    
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build the scene dictionary from current parameters"""
        box_params = self.box_params.get_parameters()
        light_params = self.light_params.get_parameters()
        wall_params = self.wall_params.get_parameters()
        object_params = self.object_params.get_parameters()
        
        scene_params = {
            'width': params.get('width', 800),
            'height': params.get('height', 800),
            'box_size': box_params['box_size'],
            'left_wall_color': (
                wall_params['left_r'] / 100.0,
                wall_params['left_g'] / 100.0,
                wall_params['left_b'] / 100.0
            ),
            'right_wall_color': (
                wall_params['right_r'] / 100.0,
                wall_params['right_g'] / 100.0,
                wall_params['right_b'] / 100.0
            ),
            'back_wall_color': (0.725, 0.71, 0.68),
            'floor_color': (0.725, 0.71, 0.68),
            'ceiling_color': (0.725, 0.71, 0.68),
            'light_intensity': float(light_params['intensity']),
            'light_size': light_params['light_size'],
            'sphere_size': object_params['sphere_size'],
            'box_size_param': object_params['box_size'],
        }
        
        logger.debug(f"Cornell Box params: {scene_params}")
        return self.scene_gen.generate(scene_params)
    
    def get_default_params(self) -> Dict[str, Any]:
        """Return default rendering parameters"""
        return {
            'spp': 512,  # Higher for better global illumination
            'integrator': 'path',
            'variant': 'scalar_rgb'
        }
