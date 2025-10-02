"""
Parametric Lighting Techniques Demo - Professional lighting setups for 3D rendering

This module demonstrates various professional lighting techniques used in photography,
film, and 3D rendering. Each technique creates different moods and emphasizes
different aspects of your subject.

Learning Objectives:
- Understand 3-point lighting (key, fill, rim)
- Learn how light position affects mood
- Experiment with light intensity ratios
- Master dramatic lighting techniques
"""

from typing import Dict, Any


class LightingTechniquesGenerator:
    """
    Generate scenes demonstrating professional lighting techniques
    
    Lighting Techniques Available:
    1. THREE_POINT - Classic studio setup (key + fill + rim)
    2. DRAMATIC - Single hard light for high contrast
    3. SOFT - Large soft lights for even illumination
    4. RIM - Backlight emphasis for silhouettes
    5. TOP - Overhead lighting (horror/mystery)
    """
    
    @staticmethod
    def generate(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a scene with professional lighting setup
        
        Parameters:
            width: int - Image width (default: 800)
            height: int - Image height (default: 600)
            
            lighting_type: str - Lighting setup type:
                'three_point' - Classic 3-point lighting
                'dramatic' - Single strong side light
                'soft' - Large soft lights
                'rim' - Strong backlight
                'top' - Overhead dramatic
            
            key_intensity: float - Main light strength (1-100)
            fill_intensity: float - Fill light strength (1-50)
            rim_intensity: float - Rim/back light strength (1-100)
            
            key_height: float - Height of key light (1-10)
            key_distance: float - Distance of key light (2-15)
            
            object_type: str - Subject type:
                'sphere' - Simple sphere
                'cube' - Cube object
                'both' - Sphere and cube
            
            object_material: str - Material type:
                'diffuse' - Matte surface
                'plastic' - Glossy surface
                'metal' - Reflective surface
            
            background_brightness: float - Background color (0-1)
        """
        
        # Extract parameters with defaults
        width = params.get('width', 800)
        height = params.get('height', 600)
        
        lighting_type = params.get('lighting_type', 'three_point')
        key_intensity = params.get('key_intensity', 30.0)
        fill_intensity = params.get('fill_intensity', 10.0)
        rim_intensity = params.get('rim_intensity', 20.0)
        key_height = params.get('key_height', 4.0)
        key_distance = params.get('key_distance', 5.0)
        
        object_type = params.get('object_type', 'sphere')
        object_material = params.get('object_material', 'plastic')
        background_brightness = params.get('background_brightness', 0.2)
        
        # Build base scene
        scene_dict = {
            'type': 'scene',
            
            # Path tracer for realistic lighting
            'integrator': {
                'type': 'path',
                'max_depth': 8,
            },
            
            # Camera setup - positioned to view subject
            'sensor': {
                'type': 'perspective',
                'fov': 45,
                'to_world': {
                    'type': 'look_at',
                    'origin': [0, -6, 2],
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
            
            # Ground plane - provides surface for shadows
            'ground': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'scale',
                    'value': 20
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [background_brightness] * 3
                    }
                }
            },
            
            # Background wall - helps visualize lighting
            'back_wall': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 5, 5],
                    'child': {
                        'type': 'rotate',
                        'angle': 90,
                        'axis': [1, 0, 0],
                        'child': {
                            'type': 'scale',
                            'value': 10
                        }
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [background_brightness * 0.8] * 3
                    }
                }
            },
        }
        
        # Add objects based on type
        obj_bsdf = LightingTechniquesGenerator._create_material(object_material)
        
        if object_type == 'sphere' or object_type == 'both':
            scene_dict['sphere'] = {
                'type': 'sphere',
                'radius': 1.0,
                'center': [-1.2 if object_type == 'both' else 0, 0, 1],
                'bsdf': obj_bsdf
            }
        
        if object_type == 'cube' or object_type == 'both':
            scene_dict['cube'] = {
                'type': 'cube',
                'to_world': {
                    'type': 'translate',
                    'value': [1.2 if object_type == 'both' else 0, 0, 1],
                    'child': {
                        'type': 'rotate',
                        'angle': 30,
                        'axis': [0, 0, 1],
                        'child': {
                            'type': 'scale',
                            'value': 1.5
                        }
                    }
                },
                'bsdf': obj_bsdf
            }
        
        # Add lights based on lighting type
        if lighting_type == 'three_point':
            # THREE-POINT LIGHTING
            # This is the foundation of studio lighting
            
            # KEY LIGHT: Main light source (brightest, creates primary shadows)
            # Positioned 45° to side and above subject
            scene_dict['key_light'] = {
                'type': 'point',
                'position': [key_distance * 0.7, -key_distance * 0.7, key_height],
                'intensity': {
                    'type': 'rgb',
                    'value': [key_intensity] * 3
                }
            }
            
            # FILL LIGHT: Softens shadows created by key light
            # Positioned opposite to key, lower intensity
            scene_dict['fill_light'] = {
                'type': 'point',
                'position': [-key_distance * 0.5, -key_distance * 0.8, key_height * 0.6],
                'intensity': {
                    'type': 'rgb',
                    'value': [fill_intensity] * 3
                }
            }
            
            # RIM/BACK LIGHT: Separates subject from background
            # Positioned behind and above subject
            scene_dict['rim_light'] = {
                'type': 'point',
                'position': [0, key_distance * 0.5, key_height * 1.2],
                'intensity': {
                    'type': 'rgb',
                    'value': [rim_intensity] * 3
                }
            }
        
        elif lighting_type == 'dramatic':
            # DRAMATIC LIGHTING
            # Single strong light creates high contrast and deep shadows
            # Common in film noir, horror, dramatic portraits
            
            scene_dict['key_light'] = {
                'type': 'point',
                'position': [key_distance, -key_distance * 0.5, key_height],
                'intensity': {
                    'type': 'rgb',
                    'value': [key_intensity * 1.5] * 3
                }
            }
            
            # Optional weak fill to prevent pure black shadows
            scene_dict['weak_fill'] = {
                'type': 'point',
                'position': [-key_distance * 0.8, -key_distance, key_height * 0.3],
                'intensity': {
                    'type': 'rgb',
                    'value': [fill_intensity * 0.3] * 3
                }
            }
        
        elif lighting_type == 'soft':
            # SOFT LIGHTING
            # Multiple soft lights create even, flattering illumination
            # Used in beauty photography, product shots
            
            # Large area light above
            scene_dict['top_light'] = {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, key_height + 2],
                    'child': {
                        'type': 'scale',
                        'value': 3
                    }
                },
                'emitter': {
                    'type': 'area',
                    'radiance': {
                        'type': 'rgb',
                        'value': [key_intensity * 0.8] * 3
                    }
                }
            }
            
            # Side fill lights
            for i, x_pos in enumerate([-key_distance, key_distance]):
                scene_dict[f'side_light_{i}'] = {
                    'type': 'rectangle',
                    'to_world': {
                        'type': 'translate',
                        'value': [x_pos, -key_distance * 0.5, key_height * 0.7],
                        'child': {
                            'type': 'scale',
                            'value': 2
                        }
                    },
                    'emitter': {
                        'type': 'area',
                        'radiance': {
                            'type': 'rgb',
                            'value': [fill_intensity * 1.2] * 3
                        }
                    }
                }
        
        elif lighting_type == 'rim':
            # RIM LIGHTING
            # Strong backlight creates glowing edge, dramatic silhouette
            # Used for product reveals, dramatic effect
            
            # Strong rim light from behind
            scene_dict['rim_light'] = {
                'type': 'point',
                'position': [0, key_distance * 0.8, key_height * 1.5],
                'intensity': {
                    'type': 'rgb',
                    'value': [rim_intensity * 2] * 3
                }
            }
            
            # Weak front fill to show some detail
            scene_dict['front_fill'] = {
                'type': 'point',
                'position': [0, -key_distance * 1.2, key_height * 0.5],
                'intensity': {
                    'type': 'rgb',
                    'value': [fill_intensity * 0.5] * 3
                }
            }
        
        elif lighting_type == 'top':
            # TOP LIGHTING
            # Overhead light creates mysterious, dramatic mood
            # Used in horror, mystery, noir
            
            scene_dict['top_light'] = {
                'type': 'point',
                'position': [0, -1, key_height * 2],
                'intensity': {
                    'type': 'rgb',
                    'value': [key_intensity * 1.2] * 3
                }
            }
            
            # Very weak bounce light from below
            scene_dict['bounce'] = {
                'type': 'point',
                'position': [0, -2, 0.5],
                'intensity': {
                    'type': 'rgb',
                    'value': [fill_intensity * 0.2] * 3
                }
            }
        
        return scene_dict
    
    @staticmethod
    def _create_material(material_type: str) -> Dict[str, Any]:
        """
        Create material BSDF based on type
        
        Material types affect how light interacts:
        - Diffuse: Scatters light evenly (matte)
        - Plastic: Glossy coat over diffuse (paint-like)
        - Metal: Reflects light (conductor)
        """
        if material_type == 'diffuse':
            return {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': [0.6, 0.6, 0.6]
                }
            }
        elif material_type == 'plastic':
            return {
                'type': 'plastic',
                'diffuse_reflectance': {
                    'type': 'rgb',
                    'value': [0.5, 0.5, 0.5]
                },
                'nonlinear': True
            }
        elif material_type == 'metal':
            return {
                'type': 'roughconductor',
                'material': 'Al',  # Aluminum
                'alpha': 0.1
            }
        else:
            return {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': [0.6, 0.6, 0.6]
                }
            }
