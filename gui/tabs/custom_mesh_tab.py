"""
Custom Mesh Tab - Load and render custom 3D models

⚠️ TODO: This tab is partially functional but has known issues.
See TODO.md for details on:
- STL file loading problems (some files fail with normals error)
- Need automatic camera positioning based on mesh bounds
- Need better error handling and validation
- Need mesh statistics display

Current status: Works for some OBJ/PLY files, STL support experimental
"""

from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QFileDialog, QLineEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget
from typing import Dict, Any
from loguru import logger
from pathlib import Path


class CustomMeshTab(BaseTab):
    """Tab for loading and rendering custom 3D meshes"""
    
    def __init__(self, parent=None):
        super().__init__("Custom Mesh", parent)
        self.mesh_file_path = None
    
    def setup_ui(self):
        """Setup the tab UI"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Info label
        info = QLabel(
            "Load and render custom 3D models!\n\n"
            "Supported formats:\n"
            "• OBJ (.obj) - Wavefront OBJ files\n"
            "• PLY (.ply) - Stanford PLY format\n"
            "• STL (.stl) - Stereolithography\n\n"
            "Free models: polyhaven.com, free3d.com, sketchfab.com"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #4ec9b0; padding: 10px; background: #2d2d2d; border-radius: 5px;")
        scroll_layout.addWidget(info)
        
        # File selection
        file_widget = QWidget()
        file_layout = QVBoxLayout(file_widget)
        
        file_label = QLabel("Mesh File:")
        file_label.setStyleSheet("color: #dcdcaa; font-weight: bold;")
        file_layout.addWidget(file_label)
        
        # File path display and button
        file_row = QHBoxLayout()
        self.file_path_display = QLineEdit()
        self.file_path_display.setPlaceholderText("No file selected...")
        self.file_path_display.setReadOnly(True)
        self.file_path_display.setStyleSheet("background: #1e1e1e; color: #cccccc; padding: 5px;")
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._on_browse_clicked)
        browse_btn.setStyleSheet("""
            QPushButton {
                background: #0e639c;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: #1177bb;
            }
        """)
        
        file_row.addWidget(self.file_path_display, 1)
        file_row.addWidget(browse_btn)
        file_layout.addLayout(file_row)
        
        scroll_layout.addWidget(file_widget)
        
        # Mesh transform parameters
        self.transform_params = ParameterWidget("Transform")
        self.transform_params.add_float_parameter(
            'mesh_scale', 'Scale:', default=1.0, min_val=0.1, max_val=10.0,
            step=0.1, tooltip="Scale the mesh"
        )
        self.transform_params.add_slider_parameter(
            'mesh_rotation_x', 'Rotation X:', default=0, min_val=0, max_val=360,
            tooltip="Rotation around X axis (degrees)"
        )
        self.transform_params.add_slider_parameter(
            'mesh_rotation_y', 'Rotation Y:', default=0, min_val=0, max_val=360,
            tooltip="Rotation around Y axis (degrees)"
        )
        self.transform_params.add_slider_parameter(
            'mesh_rotation_z', 'Rotation Z:', default=0, min_val=0, max_val=360,
            tooltip="Rotation around Z axis (degrees)"
        )
        self.transform_params.add_float_parameter(
            'mesh_pos_x', 'Position X:', default=0.0, min_val=-10.0, max_val=10.0,
            step=0.1, tooltip="X position"
        )
        self.transform_params.add_float_parameter(
            'mesh_pos_y', 'Position Y:', default=0.0, min_val=-10.0, max_val=10.0,
            step=0.1, tooltip="Y position"
        )
        self.transform_params.add_float_parameter(
            'mesh_pos_z', 'Position Z:', default=0.0, min_val=-10.0, max_val=10.0,
            step=0.1, tooltip="Z position"
        )
        
        # Material parameters
        self.material_params = ParameterWidget("Material")
        self.material_params.add_choice_parameter(
            'material_type', 'Material Type:',
            choices=['diffuse', 'plastic', 'conductor', 'dielectric'],
            default='plastic',
            tooltip="Material type"
        )
        self.material_params.add_slider_parameter(
            'color_r', 'Color Red:', default=80, min_val=0, max_val=100,
            tooltip="Red component (0-100)"
        )
        self.material_params.add_slider_parameter(
            'color_g', 'Color Green:', default=80, min_val=0, max_val=100,
            tooltip="Green component (0-100)"
        )
        self.material_params.add_slider_parameter(
            'color_b', 'Color Blue:', default=80, min_val=0, max_val=100,
            tooltip="Blue component (0-100)"
        )
        self.material_params.add_slider_parameter(
            'roughness', 'Roughness:', default=10, min_val=0, max_val=100,
            tooltip="Material roughness (0=smooth, 100=rough)"
        )
        
        # Camera parameters
        self.camera_params = ParameterWidget("Camera")
        self.camera_params.add_float_parameter(
            'camera_distance', 'Distance:', default=5.0, min_val=1.0, max_val=20.0,
            step=0.5, tooltip="Camera distance from origin"
        )
        self.camera_params.add_float_parameter(
            'camera_height', 'Height:', default=2.0, min_val=-5.0, max_val=10.0,
            step=0.5, tooltip="Camera height"
        )
        
        # Scene options
        self.scene_params = ParameterWidget("Scene Options")
        self.scene_params.add_bool_parameter(
            'use_ground', 'Show Ground Plane', default=True,
            tooltip="Add ground plane"
        )
        self.scene_params.add_choice_parameter(
            'light_type', 'Lighting:',
            choices=['point', 'hdri'],
            default='point',
            tooltip="Lighting type (HDRI requires environment map)"
        )
        
        scroll_layout.addWidget(self.transform_params)
        scroll_layout.addWidget(self.material_params)
        scroll_layout.addWidget(self.camera_params)
        scroll_layout.addWidget(self.scene_params)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        self.content_layout.addWidget(scroll)
    
    def _on_browse_clicked(self):
        """Handle browse button click"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select 3D Mesh File",
            "",
            "3D Models (*.obj *.ply *.stl);;OBJ Files (*.obj);;PLY Files (*.ply);;STL Files (*.stl);;All Files (*.*)"
        )
        
        if file_path:
            self.mesh_file_path = file_path
            self.file_path_display.setText(file_path)
            logger.info(f"Selected mesh file: {file_path}")
    
    def get_scene_dict(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Build the custom mesh scene"""
        if not self.mesh_file_path:
            raise ValueError("Please select a mesh file first!")
        
        transform_params = self.transform_params.get_parameters()
        material_params = self.material_params.get_parameters()
        camera_params = self.camera_params.get_parameters()
        scene_params = self.scene_params.get_parameters()
        
        width = params.get('width', 800)
        height = params.get('height', 600)
        
        # Import the generator
        from gui_examples.custom_mesh import CustomMeshGenerator
        
        # Build parameters
        gen_params = {
            'width': width,
            'height': height,
            'mesh_file': self.mesh_file_path,
            'mesh_scale': transform_params['mesh_scale'],
            'mesh_rotation_x': float(transform_params['mesh_rotation_x']),
            'mesh_rotation_y': float(transform_params['mesh_rotation_y']),
            'mesh_rotation_z': float(transform_params['mesh_rotation_z']),
            'mesh_position': (
                transform_params['mesh_pos_x'],
                transform_params['mesh_pos_y'],
                transform_params['mesh_pos_z']
            ),
            'camera_distance': camera_params['camera_distance'],
            'camera_height': camera_params['camera_height'],
            'material_type': material_params['material_type'],
            'material_color': (
                material_params['color_r'] / 100.0,
                material_params['color_g'] / 100.0,
                material_params['color_b'] / 100.0
            ),
            'roughness': material_params['roughness'] / 100.0,
            'use_ground': scene_params['use_ground'],
            'light_type': scene_params['light_type']
        }
        
        scene_dict = CustomMeshGenerator.generate(gen_params)
        
        logger.debug(f"Custom mesh scene generated for: {Path(self.mesh_file_path).name}")
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
        if self.mesh_file_path:
            mesh_name = Path(self.mesh_file_path).stem
            return f"custom_mesh_{mesh_name}.png"
        return "custom_mesh.png"
