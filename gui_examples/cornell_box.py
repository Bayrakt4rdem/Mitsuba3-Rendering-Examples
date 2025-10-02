"""
Parametric Cornell Box Scene - Classic cornell box wi            # Camera
            'sensor': {
                'type': 'perspective',
                'fov': 39.3077,
                'to_world': {
                    'type': 'look_at',
                    'origin': [0, -10, 1],
                    'target': [0, 0, 1],
                    'up': [0, 0, 1]
                },
                'film': {le parameters
"""

from typing import Dict, Any


class CornellBoxGenerator:
    """Generate Cornell Box scene with customizable parameters"""
    
    @staticmethod
    def generate(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Mitsuba Cornell Box scene dictionary
        
        Parameters:
            width: int - Image width
            height: int - Image height
            box_size: float - Size of the cornell box
            left_wall_color: tuple - RGB color for left wall
            right_wall_color: tuple - RGB color for right wall
            back_wall_color: tuple - RGB color for back wall
            floor_color: tuple - RGB color for floor
            ceiling_color: tuple - RGB color for ceiling
            light_intensity: float - Light intensity multiplier
            light_size: float - Size of area light
            sphere_size: float - Size of sphere
            box_size_param: float - Size of box object
        """
        
        width = params.get('width', 800)
        height = params.get('height', 800)
        box_size = params.get('box_size', 2.0)
        
        # Wall colors
        left_color = params.get('left_wall_color', (0.63, 0.065, 0.05))  # Red
        right_color = params.get('right_wall_color', (0.14, 0.45, 0.091))  # Green
        back_color = params.get('back_wall_color', (0.725, 0.71, 0.68))  # White
        floor_color = params.get('floor_color', (0.725, 0.71, 0.68))  # White
        ceiling_color = params.get('ceiling_color', (0.725, 0.71, 0.68))  # White
        
        # Light
        light_intensity = params.get('light_intensity', 15.0)
        light_size = params.get('light_size', 0.5)
        
        # Objects
        sphere_size = params.get('sphere_size', 0.4)
        box_obj_size = params.get('box_size_param', 0.5)
        
        scene_dict = {
            'type': 'scene',
            
            # Integrator for global illumination
            'integrator': {
                'type': 'path',
                'max_depth': 8,
            },
            
            # Camera
            'sensor': {
                'type': 'perspective',
                'fov': 40,
                'to_world': {
                    'type': 'look_at',
                    'origin': [0, -3.5, 1],
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
            
            # Floor
            'floor': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'scale',
                    'value': [box_size, box_size, 1]
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': floor_color
                    }
                }
            },
            
            # Ceiling
            'ceiling': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, box_size],
                    'child': {
                        'type': 'scale',
                        'value': [box_size, box_size, 1]
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': ceiling_color
                    }
                }
            },
            
            # Back wall
            'back_wall': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, box_size, box_size / 2],
                    'child': {
                        'type': 'rotate',
                        'angle': 90,
                        'axis': [1, 0, 0],
                        'child': {
                            'type': 'scale',
                            'value': [box_size, box_size, 1]
                        }
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': back_color
                    }
                }
            },
            
            # Right wall (green)
            'right_wall': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [box_size, 0, box_size / 2],
                    'child': {
                        'type': 'rotate',
                        'angle': 90,
                        'axis': [0, 1, 0],
                        'child': {
                            'type': 'rotate',
                            'angle': 90,
                            'axis': [1, 0, 0],
                            'child': {
                                'type': 'scale',
                                'value': [box_size, box_size, 1]
                            }
                        }
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': right_color
                    }
                }
            },
            
            # Left wall (red)
            'left_wall': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [-box_size, 0, box_size / 2],
                    'child': {
                        'type': 'rotate',
                        'angle': -90,
                        'axis': [0, 1, 0],
                        'child': {
                            'type': 'rotate',
                            'angle': 90,
                            'axis': [1, 0, 0],
                            'child': {
                                'type': 'scale',
                                'value': [box_size, box_size, 1]
                            }
                        }
                    }
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': left_color
                    }
                }
            },
            
            # Area light on ceiling (facing downward)
            'light': {
                'type': 'rectangle',
                'to_world': {
                    'type': 'translate',
                    'value': [0, 0, box_size - 0.01],
                    'child': {
                        'type': 'scale',
                        'value': light_size,
                        'child': {
                            'type': 'rotate',
                            'axis': [1, 0, 0],
                            'angle': 180  # Flip to face downward
                        }
                    }
                },
                'emitter': {
                    'type': 'area',
                    'radiance': {
                        'type': 'rgb',
                        'value': [light_intensity, light_intensity, light_intensity]
                    }
                }
            },
            
            # Sphere (reflective)
            'sphere': {
                'type': 'sphere',
                'radius': sphere_size,
                'center': [-0.5, 0.3, sphere_size],
                'bsdf': {
                    'type': 'conductor',
                    'material': 'Al',  # Aluminum
                }
            },
            
            # Box object (diffuse)
            'box': {
                'type': 'cube',
                'to_world': {
                    'type': 'translate',
                    'value': [0.5, -0.3, box_obj_size / 2],
                    'child': {
                        'type': 'rotate',
                        'angle': 20,
                        'axis': [0, 0, 1],
                        'child': {
                            'type': 'scale',
                            'value': box_obj_size
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
            },
        }
        
        return scene_dict
