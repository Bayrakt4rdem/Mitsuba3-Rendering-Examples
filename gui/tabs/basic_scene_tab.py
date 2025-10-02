"""
Basic Scene Tab - Interactive controls for the basic sphere scene
"""

from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget
from gui_examples.basic_scene import BasicSceneGenerator
from typing import Dict, Any
from loguru import logger


class BasicSceneTab(BaseTab):
    """Tab for rendering a basic scene with a sphere"""
    
    def __init__(self, parent=None):
        self.scene_gen = BasicSceneGenerator()
        super().__init__("Basic Scene", parent)
    
    def setup_ui(self):
        """Setup the tab UI with parameter controls"""
        # Create scroll area for parameters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Sphere parameters
        self.sphere_params = ParameterWidget("Sphere Properties")
        self.sphere_params.add_float_parameter(
            'radius', 'Radius:', default=1.0, min_val=0.1, max_val=5.0,
            step=0.1, tooltip="Size of the sphere"
        )
        self.sphere_params.add_float_parameter(
            'pos_x', 'Position X:', default=0.0, min_val=-5.0, max_val=5.0,
            step=0.1, tooltip="Horizontal position"
        )
        self.sphere_params.add_float_parameter(
            'pos_y', 'Position Y:', default=0.0, min_val=-5.0, max_val=5.0,
            step=0.1, tooltip="Depth position"
        )
        self.sphere_params.add_float_parameter(
            'pos_z', 'Position Z:', default=1.0, min_val=-2.0, max_val=5.0,
            step=0.1, tooltip="Height above ground (default: 1.0 = on ground)"
        )
        
        # Material parameters
        self.material_params = ParameterWidget("Material Properties")
        self.material_params.add_choice_parameter(
            'material', 'Material Type:', 
            choices=['diffuse', 'plastic', 'conductor', 'dielectric'],
            default='diffuse',
            tooltip="Type of material for the sphere"
        )
        self.material_params.add_slider_parameter(
            'roughness', 'Roughness:', default=10, min_val=0, max_val=100,
            tooltip="Surface roughness (0=smooth, 100=rough)"
        )
        self.material_params.add_slider_parameter(
            'color_r', 'Color Red:', default=80, min_val=0, max_val=100,
            tooltip="Red color component (0-100)"
        )
        self.material_params.add_slider_parameter(
            'color_g', 'Color Green:', default=20, min_val=0, max_val=100,
            tooltip="Green color component (0-100)"
        )
        self.material_params.add_slider_parameter(
            'color_b', 'Color Blue:', default=20, min_val=0, max_val=100,
            tooltip="Blue color component (0-100)"
        )
        
        # Camera parameters
        self.camera_params = ParameterWidget("Camera Settings")
        self.camera_params.add_float_parameter(
            'distance', 'Distance:', default=5.0, min_val=2.0, max_val=20.0,
            step=0.5, tooltip="Camera distance from origin"
        )
        
        # Add to scroll layout
        scroll_layout.addWidget(self.sphere_params)
        scroll_layout.addWidget(self.material_params)
        scroll_layout.addWidget(self.camera_params)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        self.content_layout.addWidget(scroll)
    
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build the scene dictionary from current parameters"""
        # Get UI parameters
        sphere_params = self.sphere_params.get_parameters()
        material_params = self.material_params.get_parameters()
        camera_params = self.camera_params.get_parameters()
        
        # Build scene parameters
        scene_params = {
            'width': params.get('width', 800),
            'height': params.get('height', 600),
            'sphere_radius': sphere_params['radius'],
            'sphere_x': sphere_params['pos_x'],
            'sphere_y': sphere_params['pos_y'],
            'sphere_z': sphere_params['pos_z'],
            'camera_distance': camera_params['distance'],
            'material_type': material_params['material'],
            'material_color': (
                material_params['color_r'] / 100.0,
                material_params['color_g'] / 100.0,
                material_params['color_b'] / 100.0
            ),
            'roughness': material_params['roughness'] / 100.0,
        }
        
        logger.debug(f"Scene params: {scene_params}")
        return self.scene_gen.generate(scene_params)
    
    def get_default_params(self) -> Dict[str, Any]:
        """Return default rendering parameters"""
        return {
            'spp': 256,
            'integrator': 'path',
            'variant': 'scalar_rgb'
        }
