"""
Custom Mesh Loader - Load and render OBJ, PLY, STL files
"""

from typing import Dict, Any
from pathlib import Path


class CustomMeshGenerator:
    """Generate scene with custom 3D mesh file"""
    
    @staticmethod
    def generate(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Mitsuba scene with custom mesh
        
        Parameters:
            width: int - Image width
            height: int - Image height
            mesh_file: str - Path to mesh file (.obj, .ply, .stl, .serialized)
            mesh_scale: float - Scale factor for mesh
            mesh_rotation_x: float - Rotation around X axis (degrees)
            mesh_rotation_y: float - Rotation around Y axis (degrees)
            mesh_rotation_z: float - Rotation around Z axis (degrees)
            mesh_position: tuple - (x, y, z) position
            camera_distance: float - Distance from origin
            camera_height: float - Camera height
            material_type: str - Material type (diffuse, conductor, dielectric, plastic)
            material_color: tuple - RGB color (0-1) for diffuse/plastic
            roughness: float - Material roughness (0-1)
            use_ground: bool - Add ground plane
            light_type: str - 'point' or 'hdri'
            hdri_path: str - Path to HDRI environment map (if light_type='hdri')
        """
        
        width = params.get('width', 800)
        height = params.get('height', 600)
        
        # Mesh parameters
        mesh_file = params.get('mesh_file', None)
        if not mesh_file:
            raise ValueError("mesh_file parameter is required!")
        
        mesh_scale = params.get('mesh_scale', 1.0)
        mesh_rot_x = params.get('mesh_rotation_x', 0.0)
        mesh_rot_y = params.get('mesh_rotation_y', 0.0)
        mesh_rot_z = params.get('mesh_rotation_z', 0.0)
        mesh_pos = params.get('mesh_position', (0, 0, 0))
        
        # Camera
        camera_distance = params.get('camera_distance', 5.0)
        camera_height = params.get('camera_height', 2.0)
        
        # Material
        material_type = params.get('material_type', 'diffuse')
        material_color = params.get('material_color', (0.8, 0.8, 0.8))
        roughness = params.get('roughness', 0.1)
        
        # Scene options
        use_ground = params.get('use_ground', True)
        light_type = params.get('light_type', 'point')
        hdri_path = params.get('hdri_path', None)
        
        # Build BSDF
        bsdf = CustomMeshGenerator._create_material(material_type, material_color, roughness)
        
        # Build mesh transform
        mesh_transform = {
            'type': 'translate',
            'value': list(mesh_pos),
            'child': {
                'type': 'rotate',
                'axis': [1, 0, 0],
                'angle': mesh_rot_x,
                'child': {
                    'type': 'rotate',
                    'axis': [0, 1, 0],
                    'angle': mesh_rot_y,
                    'child': {
                        'type': 'rotate',
                        'axis': [0, 0, 1],
                        'angle': mesh_rot_z,
                        'child': {
                            'type': 'scale',
                            'value': mesh_scale
                        }
                    }
                }
            }
        }
        
        # Scene dictionary
        scene_dict = {
            'type': 'scene',
            
            # Integrator
            'integrator': {
                'type': 'path',
                'max_depth': 8,
            },
            
            # Camera
            'sensor': {
                'type': 'perspective',
                'fov': 45,
                'to_world': {
                    'type': 'look_at',
                    'origin': [camera_distance * 0.707, -camera_distance * 0.707, camera_height],
                    'target': [0, 0, mesh_pos[2]],
                    'up': [0, 0, 1]
                },
                'film': {
                    'type': 'hdrfilm',
                    'width': width,
                    'height': height,
                    'pixel_format': 'rgb',
                }
            },
            
            # Custom mesh - detect file type
            'custom_mesh': CustomMeshGenerator._create_mesh_shape(mesh_file, mesh_transform, bsdf),
        }
        
        # Add ground plane if requested
        if use_ground:
            scene_dict['ground'] = {
                'type': 'rectangle',
                'to_world': {
                    'type': 'scale',
                    'value': 20
                },
                'bsdf': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [0.5, 0.5, 0.5]
                    }
                }
            }
        
        # Add lighting
        if light_type == 'hdri' and hdri_path:
            # Environment map lighting
            scene_dict['emitter'] = {
                'type': 'envmap',
                'filename': str(hdri_path),
            }
        else:
            # Default point lights
            scene_dict['light_key'] = {
                'type': 'point',
                'position': [5, -5, 5],
                'intensity': {
                    'type': 'spectrum',
                    'value': 100.0
                }
            }
            scene_dict['light_fill'] = {
                'type': 'point',
                'position': [-3, -3, 3],
                'intensity': {
                    'type': 'spectrum',
                    'value': 30.0
                }
            }
        
        return scene_dict
    
    @staticmethod
    def _create_mesh_shape(mesh_file: str, transform: Dict[str, Any], bsdf: Dict[str, Any]) -> Dict[str, Any]:
        """Create mesh shape with correct plugin type based on file extension"""
        mesh_path = Path(mesh_file)
        extension = mesh_path.suffix.lower()
        
        # Mitsuba plugin type mapping
        # Note: STL files are loaded via 'obj' plugin in Mitsuba 3
        if extension == '.obj':
            plugin_type = 'obj'
        elif extension == '.ply':
            plugin_type = 'ply'
        elif extension == '.stl':
            plugin_type = 'obj'  # Mitsuba's OBJ plugin supports STL
        elif extension == '.serialized':
            plugin_type = 'serialized'
        else:
            # Default to obj plugin (most versatile)
            plugin_type = 'obj'
        
        mesh_dict = {
            'type': plugin_type,
            'filename': str(mesh_file),
            'to_world': transform,
            'bsdf': bsdf
        }
        
        # STL files often don't have normals - enable face normals computation
        if extension == '.stl':
            mesh_dict['face_normals'] = True
        
        return mesh_dict
    
    @staticmethod
    def _create_material(material_type: str, color: tuple, roughness: float) -> Dict[str, Any]:
        """Create material BSDF"""
        if material_type == 'diffuse':
            return {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': color
                }
            }
        elif material_type == 'conductor':
            return {
                'type': 'roughconductor',
                'material': 'Al',  # Aluminum
                'alpha': roughness
            }
        elif material_type == 'dielectric':
            return {
                'type': 'dielectric',
                'int_ior': 1.5,
                'ext_ior': 1.0,
            }
        elif material_type == 'plastic':
            return {
                'type': 'plastic',
                'diffuse_reflectance': {
                    'type': 'rgb',
                    'value': color
                },
                'nonlinear': True
            }
        else:
            # Default to diffuse
            return {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': color
                }
            }
