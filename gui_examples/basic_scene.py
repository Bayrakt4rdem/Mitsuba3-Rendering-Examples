"""
Parametric Basic Scene - A simple sphere scene with adjustable parameters
"""

from typing import Dict, Any


class BasicSceneGenerator:
    """Generate a basic scene with a sphere and customizable parameters"""
    
    @staticmethod
    def generate(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Mitsuba scene dictionary
        
        Parameters:
            width: int - Image width
            height: int - Image height
            sphere_radius: float - Radius of the sphere
            sphere_x: float - X position
            sphere_y: float - Y position
            sphere_z: float - Z position
            camera_distance: float - Distance from origin
            material_type: str - Material type (diffuse, conductor, dielectric)
            material_color: tuple - RGB color (0-1)
            roughness: float - Material roughness
        """
        
        width = params.get('width', 800)
        height = params.get('height', 600)
        sphere_radius = params.get('sphere_radius', 1.0)
        sphere_x = params.get('sphere_x', 0.0)
        sphere_y = params.get('sphere_y', 0.0)
        sphere_z = params.get('sphere_z', 0.0)
        camera_distance = params.get('camera_distance', 5.0)
        material_type = params.get('material_type', 'diffuse')
        material_color = params.get('material_color', (0.8, 0.2, 0.2))
        roughness = params.get('roughness', 0.1)
        
        # Build BSDF based on material type
        if material_type == 'diffuse':
            bsdf = {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': material_color
                }
            }
        elif material_type == 'conductor':
            bsdf = {
                'type': 'roughconductor',
                'material': 'Cu',  # Copper
                'alpha': roughness
            }
        elif material_type == 'dielectric':
            bsdf = {
                'type': 'dielectric',
                'int_ior': 1.5,  # Glass
                'ext_ior': 1.0,  # Air
            }
        else:  # plastic
            bsdf = {
                'type': 'plastic',
                'diffuse_reflectance': {
                    'type': 'rgb',
                    'value': material_color
                },
                'nonlinear': True
            }
        
        # Scene dictionary
        scene_dict = {
            'type': 'scene',
            
            # Integrator
            'integrator': {
                'type': 'path',
            },
            
            # Camera - positioned at 45° angle looking at sphere
            'sensor': {
                'type': 'perspective',
                'fov': 39,
                'to_world': {
                    'type': 'look_at',
                    'origin': [camera_distance * 0.707, camera_distance * 0.707, camera_distance * 0.5],
                    'target': [0, 0, 0.5],
                    'up': [0, 0, 1]
                },
                'film': {
                    'type': 'hdrfilm',
                    'width': width,
                    'height': height,
                    'pixel_format': 'rgb',
                }
            },
            
            # Sphere
            'sphere': {
                'type': 'sphere',
                'radius': sphere_radius,
                'center': [sphere_x, sphere_y, sphere_z],
                'bsdf': bsdf
            },
            
            # Ground plane - positioned below sphere
            'ground': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, -1],
                    'child': {
                        'type': 'scale',
                        'value': 20
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [0.8, 0.8, 0.8]
                    }
                }
            },
            
            # Light - point light for reliable illumination
            'light': {
                'type': 'point',
                'intensity': {
                    'type': 'spectrum',
                    'value': 100.0
                },
                'position': [3, 3, 4]
            },
        }
        
        return scene_dict
