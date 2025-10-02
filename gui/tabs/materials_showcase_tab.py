"""
Materials Showcase Tab - Compare different material types side by side
"""

from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget
from typing import Dict, Any
from loguru import logger


class MaterialsShowcaseTab(BaseTab):
    """Tab for showcasing different material types"""
    
    def __init__(self, parent=None):
        super().__init__("Materials", parent)
    
    def setup_ui(self):
        """Setup the tab UI"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Info label
        info = QLabel(
            "This scene showcases 5 different material types:\n"
            "• Diffuse (matte)\n"
            "• Plastic (glossy)\n"
            "• Conductor (metal)\n"
            "• Dielectric (glass)\n"
            "• Rough Conductor (brushed metal)\n\n"
            "Adjust parameters to see how materials respond to light!"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #4ec9b0; padding: 10px; background: #2d2d2d; border-radius: 5px;")
        scroll_layout.addWidget(info)
        
        # Lighting parameters
        self.light_params = ParameterWidget("Lighting")
        self.light_params.add_slider_parameter(
            'intensity', 'Light Intensity:', default=20, min_val=5, max_val=100,
            tooltip="Overall scene brightness"
        )
        self.light_params.add_float_parameter(
            'light_height', 'Light Height:', default=4.0, min_val=2.0, max_val=8.0,
            step=0.5, tooltip="Height of the area light"
        )
        
        # Material parameters
        self.material_params = ParameterWidget("Material Adjustments")
        self.material_params.add_slider_parameter(
            'roughness', 'Conductor Roughness:', default=5, min_val=0, max_val=50,
            tooltip="Roughness of metallic materials"
        )
        self.material_params.add_slider_parameter(
            'plastic_roughness', 'Plastic Roughness:', default=10, min_val=0, max_val=50,
            tooltip="Roughness of plastic coating"
        )
        self.material_params.add_float_parameter(
            'glass_ior', 'Glass IOR:', default=1.5, min_val=1.0, max_val=2.5,
            decimals=2, step=0.1, tooltip="Index of refraction for glass (1.5=standard)"
        )
        
        # Scene parameters
        self.scene_params = ParameterWidget("Scene Settings")
        self.scene_params.add_float_parameter(
            'sphere_spacing', 'Sphere Spacing:', default=2.5, min_val=1.5, max_val=4.0,
            step=0.1, tooltip="Distance between spheres"
        )
        self.scene_params.add_float_parameter(
            'sphere_radius', 'Sphere Radius:', default=0.8, min_val=0.3, max_val=1.2,
            step=0.1, tooltip="Size of each sphere"
        )
        
        scroll_layout.addWidget(self.light_params)
        scroll_layout.addWidget(self.material_params)
        scroll_layout.addWidget(self.scene_params)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        self.content_layout.addWidget(scroll)
    
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build the materials showcase scene"""
        light_params = self.light_params.get_parameters()
        material_params = self.material_params.get_parameters()
        scene_params = self.scene_params.get_parameters()
        
        width = params.get('width', 1200)
        height = params.get('height', 400)
        
        spacing = scene_params['sphere_spacing']
        radius = scene_params['sphere_radius']
        roughness = material_params['roughness'] / 100.0
        plastic_rough = material_params['plastic_roughness'] / 100.0
        glass_ior = material_params['glass_ior']
        light_intensity = float(light_params['intensity'])
        light_height = light_params['light_height']
        
        scene_dict = {
            'type': 'scene',
            
            'integrator': {'type': 'path'},
            
            # Camera
            'sensor': {
                'type': 'perspective',
                'fov': 50,
                'to_world': {
                    'type': 'look_at',
                    'origin': [0, -8, 3],
                    'target': [0, 0, 1],
                    'up': [0, 0, 1]
                },
                'film': {
                    'type': 'hdrfilm',
                    'width': width,
                    'height': height,
                    'pixel_format': 'rgb',
                }
            },
            
            # Ground
            'ground': {
                'type': 'rectangle',
                'to_world': {'type': 'scale', 'value': 20},
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.8, 0.8, 0.8]}
                }
            },
            
            # Area light (above spheres, facing downward)
            'light': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, light_height],
                    'child': {
                        'type': 'scale',
                        'value': 3,
                        'child': {
                            'type': 'rotate',
                            'axis': [1, 0, 0],
                            'angle': 180  # Flip to face downward
                        }
                    }
                },
                'emitter': {
                    'type': 'area',
                    'radiance': {'type': 'rgb', 'value': [light_intensity] * 3}
                }
            },
            
            # Sphere 1: Diffuse (Red)
            'sphere_diffuse': {
                'type': 'sphere',
                'radius': radius,
                'center': [-spacing * 2, 0, radius],
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {'type': 'rgb', 'value': [0.8, 0.2, 0.2]}
                }
            },
            
            # Sphere 2: Plastic (Blue)
            'sphere_plastic': {
                'type': 'sphere',
                'radius': radius,
                'center': [-spacing, 0, radius],
                'bsdf': {
                    'type': 'plastic',
                    'diffuse_reflectance': {'type': 'rgb', 'value': [0.2, 0.2, 0.8]},
                    'nonlinear': True
                }
            },
            
            # Sphere 3: Conductor (Gold)
            'sphere_conductor': {
                'type': 'sphere',
                'radius': radius,
                'center': [0, 0, radius],
                'bsdf': {
                    'type': 'roughconductor',
                    'material': 'Au',  # Gold
                    'alpha': roughness
                }
            },
            
            # Sphere 4: Dielectric (Glass)
            'sphere_dielectric': {
                'type': 'sphere',
                'radius': radius,
                'center': [spacing, 0, radius],
                'bsdf': {
                    'type': 'dielectric',
                    'int_ior': glass_ior,
                    'ext_ior': 1.0,
                }
            },
            
            # Sphere 5: Rough Conductor (Aluminum)
            'sphere_rough_conductor': {
                'type': 'sphere',
                'radius': radius,
                'center': [spacing * 2, 0, radius],
                'bsdf': {
                    'type': 'roughconductor',
                    'material': 'Al',  # Aluminum
                    'alpha': 0.3  # Fixed rough for comparison
                }
            },
        }
        
        logger.debug(f"Materials showcase params: spacing={spacing}, radius={radius}")
        return scene_dict
    
    def get_default_params(self) -> Dict[str, Any]:
        """Return default rendering parameters"""
        return {
            'spp': 256,
            'integrator': 'path',
            'variant': 'scalar_rgb'
        }
    
    def get_output_filename(self) -> str:
        """Custom output filename"""
        return "materials_showcase.png"
