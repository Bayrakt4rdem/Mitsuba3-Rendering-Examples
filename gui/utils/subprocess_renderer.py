"""
Subprocess-based Mitsuba renderer - runs in separate process to avoid threading issues
"""

import numpy as np
from pathlib import Path
import subprocess
import sys
import pickle
import tempfile
import re
from typing import Dict, Any
from PyQt6.QtCore import QObject, pyqtSignal, QProcess
from loguru import logger


def strip_ansi_codes(text: str) -> str:
    """Remove ANSI color codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class SubprocessRenderer(QObject):
    """Renderer that uses subprocess to avoid Qt/Mitsuba threading conflicts"""
    
    progress_updated = pyqtSignal(int)
    render_complete = pyqtSignal(object, str)  # image_array, output_path
    render_failed = pyqtSignal(str)
    log_message = pyqtSignal(str)
    
    def __init__(self, output_dir: Path):
        super().__init__()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.process = None
        self.temp_files = []  # Track temp files for cleanup
        
        logger.info(f"SubprocessRenderer initialized, output: {self.output_dir}")
    
    def render_scene(
        self,
        scene_dict: Dict[str, Any],
        params: Dict[str, Any],
        output_filename: str = "render.png"
    ):
        """
        Render a scene using a subprocess
        
        Args:
            scene_dict: Mitsuba scene dictionary
            params: Rendering parameters
            output_filename: Output filename
        """
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            logger.warning("Render already in progress")
            self.log_message.emit("⚠️  Render already in progress")
            return
        
        try:
            # Create temp file for scene data
            temp_scene_file = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl')
            pickle.dump({'scene_dict': scene_dict, 'params': params}, temp_scene_file)
            temp_scene_file.close()
            
            # Track temp file for cleanup
            self.temp_files.append(temp_scene_file.name)
            
            # Output path
            output_path = self.output_dir / output_filename
            
            # Create QProcess
            self.process = QProcess(self)
            self.process.readyReadStandardOutput.connect(self._on_stdout)
            self.process.readyReadStandardError.connect(self._on_stderr)
            self.process.finished.connect(lambda: self._on_finished(output_path))
            
            # Get Python executable from current environment
            python_exe = sys.executable
            
            # Script path
            script_path = Path(__file__).parent / 'render_subprocess.py'
            
            # Start process
            logger.debug(f"Starting subprocess: {python_exe} {script_path}")
            self.log_message.emit("🚀 Starting render process...")
            
            self.process.start(python_exe, [
                str(script_path),
                temp_scene_file.name,
                str(output_path)
            ])
            
            if not self.process.waitForStarted(3000):
                raise Exception("Failed to start render process")
            
            logger.info("Render subprocess started")
            
        except Exception as e:
            logger.exception(f"Failed to start subprocess render: {e}")
            self.log_message.emit(f"❌ Failed to start render: {str(e)}")
            self.render_failed.emit(str(e))
    
    def _on_stdout(self):
        """Handle stdout from subprocess"""
        if self.process:
            data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
            data = strip_ansi_codes(data)  # Remove ANSI color codes
            for line in data.strip().split('\n'):
                if line:
                    if line.startswith('PROGRESS:'):
                        try:
                            progress = int(line.split(':')[1])
                            self.progress_updated.emit(progress)
                        except:
                            pass
                    elif line.startswith('LOG:'):
                        msg = line[4:].strip()
                        self.log_message.emit(msg)
                    else:
                        # Other output
                        logger.debug(f"Subprocess: {line}")
    
    def _on_stderr(self):
        """Handle stderr from subprocess"""
        if self.process:
            data = self.process.readAllStandardError().data().decode('utf-8', errors='ignore')
            if data.strip():
                # Filter out known harmless warnings
                if 'jitc_llvm_init' in data or 'LLVM' in data:
                    logger.debug(f"Subprocess info: {data.strip()}")
                elif 'DeprecationWarning' in data or 'mode' in data:
                    logger.debug(f"Subprocess warning: {data.strip()}")
                else:
                    logger.error(f"Subprocess error: {data.strip()}")
    
    def _on_finished(self, output_path: Path):
        """Handle subprocess completion"""
        exit_code = self.process.exitCode()
        logger.debug(f"Subprocess finished with exit code: {exit_code}")
        
        if exit_code == 0:
            # Load the rendered image
            try:
                from PIL import Image
                img = Image.open(output_path)
                img_array = np.array(img)
                
                logger.success(f"Render completed: {output_path}")
                self.log_message.emit(f"✅ Render complete: {output_path.name}")
                self.render_complete.emit(img_array, str(output_path))
            except Exception as e:
                logger.exception(f"Failed to load rendered image: {e}")
                self.render_failed.emit(f"Failed to load image: {str(e)}")
        else:
            error_msg = f"Render failed with exit code {exit_code}"
            logger.error(error_msg)
            self.log_message.emit(f"❌ {error_msg}")
            self.render_failed.emit(error_msg)
    
    def cancel_render(self):
        """Cancel the current render"""
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            logger.info("Terminating render process")
            self.process.terminate()
            if not self.process.waitForFinished(3000):
                logger.warning("Process did not terminate gracefully, killing...")
                self.process.kill()
                self.process.waitForFinished(1000)
            self.log_message.emit("❌ Render cancelled")
    
    def cleanup(self):
        """Clean up resources (call before exit)"""
        # Terminate any running process
        if self.process:
            if self.process.state() == QProcess.ProcessState.Running:
                logger.info("Cleaning up running subprocess...")
                self.process.terminate()
                if not self.process.waitForFinished(2000):
                    self.process.kill()
                    self.process.waitForFinished(500)
            self.process = None
        
        # Clean up temp files
        if self.temp_files:
            logger.debug(f"Cleaning up {len(self.temp_files)} temp files...")
            for temp_file in self.temp_files:
                try:
                    if Path(temp_file).exists():
                        Path(temp_file).unlink()
                except Exception as e:
                    logger.warning(f"Could not delete temp file {temp_file}: {e}")
            self.temp_files.clear()
