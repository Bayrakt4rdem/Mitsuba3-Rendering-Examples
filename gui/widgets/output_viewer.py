"""
Output viewer widget for displaying rendered images
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap, QImage
import numpy as np
from pathlib import Path
from loguru import logger


class OutputViewer(QWidget):
    """Widget for displaying rendered images"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image_path = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save As...")
        self.save_btn.clicked.connect(self._save_image)
        self.save_btn.setMaximumWidth(100)
        self.save_btn.setEnabled(False)
        
        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.clicked.connect(self._open_folder)
        self.open_folder_btn.setMaximumWidth(100)
        self.open_folder_btn.setEnabled(False)
        
        self.fit_btn = QPushButton("Fit to Window")
        self.fit_btn.setCheckable(True)
        self.fit_btn.setChecked(True)
        self.fit_btn.clicked.connect(self._toggle_fit)
        self.fit_btn.setMaximumWidth(110)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.open_folder_btn)
        button_layout.addWidget(self.fit_btn)
        button_layout.addStretch()
        
        # Info label
        self.info_label = QLabel("No image loaded")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("color: #888; padding: 5px;")
        
        # Scroll area for image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
            }
        """)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        
        self.scroll_area.setWidget(self.image_label)
        
        # Add to layout
        layout.addLayout(button_layout)
        layout.addWidget(self.info_label)
        layout.addWidget(self.scroll_area)
        
        self.fit_to_window = True
    
    def _toggle_fit(self):
        """Toggle fit to window mode"""
        self.fit_to_window = self.fit_btn.isChecked()
        if self.current_image_path:
            self._display_current_image()
    
    @pyqtSlot(object, str)
    def display_image(self, image_array: np.ndarray = None, image_path: str = None):
        """
        Display an image from array or file path
        
        Args:
            image_array: Numpy array of the image
            image_path: Path to the image file
        """
        try:
            if image_path:
                self.current_image_path = Path(image_path)
                pixmap = QPixmap(str(image_path))
            elif image_array is not None:
                # Convert numpy array to QPixmap
                height, width = image_array.shape[:2]
                
                # Normalize to 0-255
                img_normalized = np.clip(image_array, 0, 1)
                img_8bit = (img_normalized * 255).astype(np.uint8)
                
                # Handle different formats
                if len(img_8bit.shape) == 3:
                    if img_8bit.shape[2] == 4:
                        # RGBA
                        q_image = QImage(
                            img_8bit.data, width, height,
                            img_8bit.strides[0],
                            QImage.Format.Format_RGBA8888
                        )
                    else:
                        # RGB
                        q_image = QImage(
                            img_8bit.data, width, height,
                            img_8bit.strides[0],
                            QImage.Format.Format_RGB888
                        )
                else:
                    # Grayscale
                    q_image = QImage(
                        img_8bit.data, width, height,
                        img_8bit.strides[0],
                        QImage.Format.Format_Grayscale8
                    )
                
                pixmap = QPixmap.fromImage(q_image)
            else:
                logger.warning("No image data provided")
                return
            
            # Store original pixmap
            self.original_pixmap = pixmap
            
            # Display
            self._display_current_image()
            
            # Update info
            if self.current_image_path:
                self.info_label.setText(
                    f"{self.current_image_path.name} | "
                    f"{pixmap.width()}x{pixmap.height()}px"
                )
                self.save_btn.setEnabled(True)
                self.open_folder_btn.setEnabled(True)
            else:
                self.info_label.setText(f"Rendered Image | {pixmap.width()}x{pixmap.height()}px")
            
            logger.debug(f"Image displayed: {pixmap.width()}x{pixmap.height()}")
            
        except Exception as e:
            logger.error(f"Failed to display image: {e}")
            self.info_label.setText(f"Error: {str(e)}")
    
    def _display_current_image(self):
        """Display the current pixmap with current settings"""
        if not hasattr(self, 'original_pixmap'):
            return
        
        if self.fit_to_window:
            # Scale to fit
            scaled_pixmap = self.original_pixmap.scaled(
                self.scroll_area.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.adjustSize()
        else:
            # Original size
            self.image_label.setPixmap(self.original_pixmap)
            self.image_label.adjustSize()
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        if self.fit_to_window and hasattr(self, 'original_pixmap'):
            self._display_current_image()
    
    def _save_image(self):
        """Save the current image to a new location"""
        from PyQt6.QtWidgets import QFileDialog
        
        if not self.current_image_path:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            str(self.current_image_path.name),
            "PNG Images (*.png);;All Files (*.*)"
        )
        
        if file_path and hasattr(self, 'original_pixmap'):
            self.original_pixmap.save(file_path)
            logger.info(f"Image saved to {file_path}")
    
    def _open_folder(self):
        """Open the folder containing the current image"""
        if self.current_image_path:
            import os
            import subprocess
            folder_path = self.current_image_path.parent
            
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            else:
                subprocess.run(['xdg-open', folder_path])
            
            logger.debug(f"Opened folder: {folder_path}")
    
    @pyqtSlot()
    def clear(self):
        """Clear the displayed image"""
        self.image_label.clear()
        self.info_label.setText("No image loaded")
        self.current_image_path = None
        self.save_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        if hasattr(self, 'original_pixmap'):
            del self.original_pixmap
