"""
Mitsuba rendering engine wrapper with progress tracking
"""

import numpy as np
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from PyQt6.QtCore import QObject, pyqtSignal
import mitsuba as mi
from loguru import logger
import threading


class RenderWorker(QObject):
    """Worker object for rendering (runs in separate Python thread, not QThread)"""
    
    progress = pyqtSignal(int)  # Progress percentage (0-100)
    finished = pyqtSignal(object)  # Rendered image
    error = pyqtSignal(str)  # Error message
    log = pyqtSignal(str)  # Log messages
    
    def __init__(self, scene_dict: Dict[str, Any], params: Dict[str, Any]):
        super().__init__()
        self.scene_dict = scene_dict
        self.params = params
        self._is_cancelled = False
    
    def run(self):
        """Execute rendering in background thread"""
        logger.debug("RenderWorker thread started")
        try:
            logger.debug("Beginning render process")
            self.log.emit("Starting render...")
            
            # Note: Variant should already be set in main thread
            
            # Preprocess scene dict to convert transform matrices
            self.log.emit("Preprocessing scene...")
            logger.debug("Starting scene preprocessing")
            try:
                scene_dict = self._preprocess_scene_dict(self.scene_dict)
                self.log.emit("Scene preprocessing complete")
                logger.debug("Preprocessing completed successfully")
            except Exception as e:
                logger.exception("Scene preprocessing failed")
                raise Exception(f"Scene preprocessing failed: {str(e)}")
            
            # Load scene
            self.progress.emit(10)
            self.log.emit("Loading scene...")
            logger.debug("Loading scene with mi.load_dict")
            try:
                scene = mi.load_dict(scene_dict)
                self.log.emit("Scene loaded successfully")
                logger.debug("Scene loaded successfully")
            except Exception as e:
                logger.exception("Scene loading failed")
                raise Exception(f"Scene loading failed: {str(e)}")
            
            if self._is_cancelled:
                return
            
            # Get integrator
            self.progress.emit(20)
            integrator = self.params.get('integrator', 'path')
            spp = self.params.get('spp', 256)
            
            self.log.emit(f"Rendering with {integrator} integrator ({spp} spp)...")
            logger.debug(f"Starting render: integrator={integrator}, spp={spp}")
            
            # Render the scene
            try:
                logger.debug("About to call mi.render()")
                image = mi.render(scene, spp=spp)
                logger.debug("mi.render() completed successfully")
            except Exception as e:
                logger.exception(f"mi.render() failed: {e}")
                raise Exception(f"Rendering failed: {str(e)}")
            
            if self._is_cancelled:
                return
            
            self.progress.emit(90)
            self.log.emit("Post-processing...")
            logger.debug("Converting to bitmap")
            
            # Convert to bitmap
            try:
                bitmap = mi.Bitmap(image)
                logger.debug("Bitmap created successfully")
            except Exception as e:
                logger.exception(f"Bitmap conversion failed: {e}")
                raise Exception(f"Bitmap conversion failed: {str(e)}")
            
            self.progress.emit(100)
            self.log.emit("Render complete!")
            
            # Convert to numpy array for display
            logger.debug("Converting bitmap to numpy array")
            img_array = np.array(bitmap)
            logger.debug(f"Image array shape: {img_array.shape}")
            
            self.finished.emit(img_array)
            
        except Exception as e:
            error_msg = f"Render error: {str(e)}"
            logger.error(error_msg)
            self.error.emit(error_msg)
    
    def _preprocess_scene_dict(self, scene_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Convert transform matrices in scene dict to Mitsuba transform objects"""
        import copy
        try:
            processed = copy.deepcopy(scene_dict)
            logger.debug("Scene dict deepcopy successful")
        except Exception as e:
            logger.error(f"Failed to deepcopy scene dict: {e}")
            raise
        
        # Recursively process all entries in the scene dict
        try:
            self._process_transforms_recursive(processed)
            logger.debug("Transform processing complete")
        except Exception as e:
            logger.error(f"Failed to process transforms: {e}")
            raise
        
        return processed
    
    def _process_transforms_recursive(self, obj: Any) -> None:
        """Recursively process transforms in the scene dictionary"""
        if isinstance(obj, dict):
            # Check if this dict has a 'to_world' key
            if 'to_world' in obj:
                to_world = obj['to_world']
                
                if isinstance(to_world, list):
                    # It's a matrix - convert to ScalarTransform4f
                    if isinstance(to_world[0], list):
                        # It's a 2D list (4x4 matrix)
                        matrix_np = np.array(to_world, dtype=np.float32)
                        obj['to_world'] = mi.ScalarTransform4f(matrix_np)
                    else:
                        # It's already a flat list of 16 values
                        matrix_np = np.array(to_world, dtype=np.float32).reshape(4, 4)
                        obj['to_world'] = mi.ScalarTransform4f(matrix_np)
                
                elif isinstance(to_world, dict):
                    # It's a transform operation dict - convert to ScalarTransform4f
                    obj['to_world'] = self._build_transform_from_dict(to_world)
            
            # Recursively process all nested dictionaries
            for key, value in obj.items():
                if key != 'to_world':  # Don't reprocess to_world
                    self._process_transforms_recursive(value)
        
        elif isinstance(obj, list):
            # Recursively process all items in lists
            for item in obj:
                self._process_transforms_recursive(item)
    
    def _build_transform_from_dict(self, transform_dict: Dict[str, Any]):
        """Convert transform dictionary to ScalarTransform4f object"""
        transform_type = transform_dict.get('type', 'identity')
        
        if transform_type == 'translate':
            # Translation
            value = transform_dict.get('value', [0, 0, 0])
            transform = mi.ScalarTransform4f.translate(value)
        elif transform_type == 'scale':
            # Scale (uniform or per-axis)
            value = transform_dict.get('value', 1.0)
            if isinstance(value, (int, float)):
                transform = mi.ScalarTransform4f.scale([value, value, value])
            else:
                transform = mi.ScalarTransform4f.scale(value)
        elif transform_type == 'rotate':
            # Rotation around axis
            axis = transform_dict.get('axis', [0, 0, 1])
            angle = transform_dict.get('angle', 0.0)
            transform = mi.ScalarTransform4f.rotate(axis, angle)
        else:
            # Default to identity
            transform = mi.ScalarTransform4f()
        
        # Check for nested/child transforms
        if 'child' in transform_dict:
            child_transform = self._build_transform_from_dict(transform_dict['child'])
            # Compose transforms (parent @ child)
            transform = transform @ child_transform
        
        return transform


class MitsubaRenderer(QObject):
    """
    High-level interface for Mitsuba rendering with GUI integration
    """
    
    progress_updated = pyqtSignal(int)
    render_complete = pyqtSignal(object, str)  # image_array, output_path
    render_failed = pyqtSignal(str)
    log_message = pyqtSignal(str)
    
    def __init__(self, output_dir: Path):
        super().__init__()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.current_worker = None
        self.current_thread = None
        self._is_rendering = False
        
        logger.info(f"MitsubaRenderer initialized, output: {self.output_dir}")
    
    def render_scene(
        self,
        scene_dict: Dict[str, Any],
        params: Dict[str, Any],
        output_filename: str = "render.exr"
    ):
        """
        Render a scene with the given parameters
        
        Args:
            scene_dict: Mitsuba scene dictionary
            params: Rendering parameters (spp, integrator, variant, etc.)
            output_filename: Name of the output file
        """
        if self._is_rendering:
            logger.warning("Render already in progress")
            self.log_message.emit("⚠️  Render already in progress")
            return
        
        try:
            # Set variant in MAIN thread before starting worker
            if 'variant' in params:
                logger.debug(f"Setting variant in main thread: {params['variant']}")
                mi.set_variant(params['variant'])
            
            # Create worker object
            logger.debug(f"Creating RenderWorker with params: {params}")
            self.current_worker = RenderWorker(scene_dict, params)
            logger.debug("RenderWorker created successfully")
            
            # Connect signals
            logger.debug("Connecting worker signals")
            self.current_worker.progress.connect(self._on_progress)
            self.current_worker.finished.connect(
                lambda img: self._on_render_complete(img, output_filename)
            )
            self.current_worker.error.connect(self._on_error)
            self.current_worker.log.connect(self._on_log)
            logger.debug("Signals connected")
            
            # Start rendering in a Python thread
            logger.debug("Starting render worker in Python thread")
            self._is_rendering = True
            self.current_thread = threading.Thread(target=self.current_worker.run, daemon=True)
            self.current_thread.start()
            logger.debug("Render worker thread started")
        except Exception as e:
            logger.exception(f"Failed to start render: {e}")
            self.log_message.emit(f"❌ Failed to start render: {str(e)}")
            self.render_failed.emit(str(e))
            self._is_rendering = False
    
    def cancel_render(self):
        """Cancel the current render operation"""
        if self.current_worker and self._is_rendering:
            self.current_worker.cancel()
            if self.current_thread:
                self.current_thread.join(timeout=5.0)  # Wait up to 5 seconds
            self._is_rendering = False
            logger.info("Render cancelled by user")
            self.log_message.emit("❌ Render cancelled")
    
    def _on_progress(self, value: int):
        """Handle progress updates"""
        self.progress_updated.emit(value)
    
    def _on_render_complete(self, image_array: np.ndarray, filename: str):
        """Handle render completion"""
        self._is_rendering = False
        try:
            # Save the image
            output_path = self.output_dir / filename
            
            # Save as PNG for easy viewing
            from PIL import Image
            
            # Convert to 8-bit for PNG
            img_normalized = np.clip(image_array, 0, 1)
            img_8bit = (img_normalized * 255).astype(np.uint8)
            
            # Handle different image shapes
            if len(img_8bit.shape) == 3 and img_8bit.shape[2] == 4:
                # RGBA
                img = Image.fromarray(img_8bit, 'RGBA')
            elif len(img_8bit.shape) == 3 and img_8bit.shape[2] == 3:
                # RGB
                img = Image.fromarray(img_8bit, 'RGB')
            else:
                # Grayscale
                img = Image.fromarray(img_8bit, 'L')
            
            # Save as PNG
            png_path = output_path.with_suffix('.png')
            img.save(png_path)
            
            logger.success(f"Render saved to {png_path}")
            self.render_complete.emit(image_array, str(png_path))
            
        except Exception as e:
            error_msg = f"Failed to save render: {str(e)}"
            logger.error(error_msg)
            self.render_failed.emit(error_msg)
    
    def _on_error(self, error_msg: str):
        """Handle render errors"""
        self._is_rendering = False
        self.render_failed.emit(error_msg)
    
    def _on_log(self, message: str):
        """Handle log messages from worker"""
        self.log_message.emit(message)
