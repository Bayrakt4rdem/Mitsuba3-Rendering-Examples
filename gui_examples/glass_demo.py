"""
Parametric Glass and Transparency Demo - Transparent materials, caustics, and refraction

This module demonstrates transparent materials like glass, water, and other dielectrics.
You'll learn how light bends (refraction), creates caustics (focused light patterns),
and how different materials have different refractive indices.

Learning Objectives:
- Understand Index of Refraction (IOR)
- Learn about caustics and light focusing
- Experiment with glass thickness
- Master transparent material rendering
- Understand total internal reflection
"""

from typing import Dict, Any
import math


class GlassDemoGenerator:
    """
    Generate scenes demonstrating glass and transparent materials
    
    Key Concepts:
    - IOR (Index of Refraction): How much light bends
      * Air: 1.0
      * Water: 1.33
      * Glass: 1.5 - 1.9
      * Diamond: 2.42
    
    - Dispersion: Different colors bend differently (rainbow effect)
    - Caustics: Focused light patterns from curved glass
    - Total Internal Reflection: Light trapped inside material
    """
    
    # Common IOR values for reference
    IOR_VALUES = {
        'air': 1.0,
        'water': 1.33,
        'acrylic': 1.49,
        'glass': 1.52,
        'sapphire': 1.77,
        'diamond': 2.42
    }
    
    @staticmethod
    def generate(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a glass demonstration scene
        
        Parameters:
            width: int - Image width (default: 800)
            height: int - Image height (default: 600)
            
            glass_type: str - Type of glass object:
                'sphere' - Glass sphere (creates caustics)
                'cube' - Glass cube
                'cylinder' - Glass cylinder
                'wine_glass' - Wine glass shape
            
            glass_ior: float - Index of refraction (1.0-2.5)
                Lower = less bending
                Higher = more bending, stronger caustics
            
            glass_tint: tuple - RGB tint color (0-1)
                (1,1,1) = clear glass
                (0.8,1.0,0.8) = slight green tint
            
            dispersion: bool - Enable rainbow effect (expensive!)
            
            light_intensity: float - Light strength (5-50)
            light_height: float - Height of light (2-8)
            
            background_type: str - Background setup:
                'white' - White background (shows caustics)
                'checker' - Checkered pattern
                'gradient' - Gradient background
            
            show_caustics: bool - Add caustic-receiving plane
            
            glass_thickness: float - For hollow objects (0.05-0.3)
        """
        
        width = params.get('width', 800)
        height = params.get('height', 600)
        
        glass_type = params.get('glass_type', 'sphere')
        glass_ior = params.get('glass_ior', 1.5)
        glass_tint = params.get('glass_tint', (1.0, 1.0, 1.0))
        dispersion = params.get('dispersion', False)
        
        light_intensity = params.get('light_intensity', 20.0)
        light_height = params.get('light_height', 5.0)
        
        background_type = params.get('background_type', 'white')
        show_caustics = params.get('show_caustics', True)
        glass_thickness = params.get('glass_thickness', 0.1)
        
        # Base scene setup
        scene_dict = {
            'type': 'scene',
            
            # Path tracer with high depth for glass
            # Glass needs multiple bounces to look correct
            'integrator': {
                'type': 'path',
                'max_depth': 12,  # Higher for glass/transparency
            },
            
            # Camera positioned to see glass and caustics
            'sensor': {
                'type': 'perspective',
                'fov': 45,
                'to_world': {
                    'type': 'look_at',
                    'origin': [4, -6, 3],
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
        }
        
        # Add background based on type
        GlassDemoGenerator._add_background(scene_dict, background_type)
        
        # Add caustic-receiving plane if enabled
        if show_caustics:
            # White plane below glass to catch caustics
            scene_dict['caustic_plane'] = {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, -0.01],  # Just below glass
                    'child': {
                        'type': 'scale',
                        'value': 5
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [0.95, 0.95, 0.95]  # Nearly white
                    }
                }
            }
        
        # Create glass BSDF
        # Dielectric = transparent material
        glass_bsdf = {
            'type': 'dielectric',
            'int_ior': glass_ior,  # Inside IOR
            'ext_ior': 1.0,         # Outside IOR (air)
        }
        
        # Add tint if not pure white
        if glass_tint != (1.0, 1.0, 1.0):
            # Tinted glass absorbs some wavelengths
            glass_bsdf = {
                'type': 'thindielectric',
                'int_ior': glass_ior,
                'ext_ior': 1.0,
                'specular_transmittance': {
                    'type': 'rgb',
                    'value': list(glass_tint)
                }
            }
        
        # Add glass object based on type
        if glass_type == 'sphere':
            # GLASS SPHERE
            # Creates beautiful caustics due to curved surface
            # Light focuses through sphere like a lens
            scene_dict['glass_sphere'] = {
                'type': 'sphere',
                'radius': 1.0,
                'center': [0, 0, 1.2],
                'bsdf': glass_bsdf
            }
        
        elif glass_type == 'cube':
            # GLASS CUBE
            # Flat surfaces create different refraction patterns
            # Good for understanding IOR effects
            scene_dict['glass_cube'] = {
                'type': 'cube',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, 1],
                    'child': {
                        'type': 'rotate',
                        'angle': 45,
                        'axis': [0, 0, 1],
                        'child': {
                            'type': 'rotate',
                            'angle': 20,
                            'axis': [1, 0, 0],
                            'child': {
                                'type': 'scale',
                                'value': 1.2
                            }
                        }
                    }
                },
                'bsdf': glass_bsdf
            }
        
        elif glass_type == 'cylinder':
            # GLASS CYLINDER
            # Creates line caustics
            # Demonstrates cylindrical lens effect
            scene_dict['glass_cylinder'] = {
                'type': 'cylinder',
                'radius': 0.6,
                'p0': [0, 0, 0.2],
                'p1': [0, 0, 2.5],
                'bsdf': glass_bsdf
            }
        
        elif glass_type == 'wine_glass':
            # WINE GLASS SHAPE
            # Complex geometry creates intricate caustics
            # Demonstrates hollow glass
            
            # Bowl (upper sphere)
            scene_dict['glass_bowl'] = {
                'type': 'sphere',
                'radius': 0.8,
                'center': [0, 0, 1.5],
                'bsdf': glass_bsdf
            }
            
            # Stem (cylinder)
            scene_dict['glass_stem'] = {
                'type': 'cylinder',
                'radius': 0.08,
                'p0': [0, 0, 0.2],
                'p1': [0, 0, 1.0],
                'bsdf': glass_bsdf
            }
            
            # Base (disk)
            scene_dict['glass_base'] = {
                'type': 'disk',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, 0.2],
                    'child': {
                        'type': 'scale',
                        'value': 0.5
                    }
                },
                'bsdf': glass_bsdf
            }
        
        # Add point light above glass
        # Point lights create sharp caustics
        scene_dict['key_light'] = {
            'type': 'point',
            'position': [0, -2, light_height],
            'intensity': {
                'type': 'rgb',
                'value': [light_intensity] * 3
            }
        }
        
        # Add fill light to see glass edges
        scene_dict['fill_light'] = {
            'type': 'point',
            'position': [3, -3, 3],
            'intensity': {
                'type': 'rgb',
                'value': [light_intensity * 0.3] * 3
            }
        }
        
        # Optional: Add colored object behind glass to show refraction
        scene_dict['red_sphere'] = {
            'type': 'sphere',
            'radius': 0.5,
            'center': [-2, 1, 0.5],
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': [0.8, 0.1, 0.1]
                }
            }
        }
        
        scene_dict['blue_sphere'] = {
            'type': 'sphere',
            'radius': 0.5,
            'center': [2, 1, 0.5],
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': [0.1, 0.1, 0.8]
                }
            }
        }
        
        return scene_dict
    
    @staticmethod
    def _add_background(scene_dict: Dict[str, Any], bg_type: str):
        """Add background to scene based on type"""
        
        if bg_type == 'white':
            # Simple white background - best for seeing caustics
            scene_dict['back_wall'] = {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 3, 2],
                    'child': {
                        'type': 'rotate',
                        'angle': 90,
                        'axis': [1, 0, 0],
                        'child': {
                            'type': 'scale',
                            'value': 8
                        }
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [0.9, 0.9, 0.9]
                    }
                }
            }
        
        elif bg_type == 'checker':
            # Checkered pattern - shows refraction distortion
            scene_dict['back_wall'] = {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 3, 2],
                    'child': {
                        'type': 'rotate',
                        'angle': 90,
                        'axis': [1, 0, 0],
                        'child': {
                            'type': 'scale',
                            'value': 8
                        }
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'checkerboard',
                        'color0': {'type': 'rgb', 'value': [0.2, 0.2, 0.2]},
                        'color1': {'type': 'rgb', 'value': [0.8, 0.8, 0.8]},
                        'to_uv': {
                            'type': 'scale',
                            'value': 4
                        }
                    }
                }
            }
        
        elif bg_type == 'gradient':
            # Gradient background (simulated with large light)
            scene_dict['env_light'] = {
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
                            'value': 15
                        }
                    }
                },
                'emitter': {
                    'type': 'area',
                    'radiance': {
                        'type': 'rgb',
                        'value': [2, 2, 2]
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [0.5, 0.5, 0.5]
                    }
                }
            }
