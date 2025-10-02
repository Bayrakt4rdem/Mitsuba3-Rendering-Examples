"""
Main application window with draggable tabs and resizable sidebar
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QSplitter, QWidget, QVBoxLayout,
    QApplication, QMessageBox, QTabBar
)
from PyQt6.QtCore import Qt, QSize, QProcess
from PyQt6.QtGui import QIcon, QPalette, QColor

from gui.core.config import AppConfig
from gui.widgets.log_viewer import LogViewer
from gui.widgets.output_viewer import OutputViewer
from gui.tabs.home_tab import HomeTab
from gui.utils.subprocess_renderer import SubprocessRenderer
from gui.utils.logger import setup_logger, add_gui_handler, get_logger

from loguru import logger


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize config
        self.config = AppConfig()
        
        # Setup logging
        setup_logger(self.config.log_dir)
        logger.info("=" * 60)
        logger.info("Mitsuba 3 Render Studio Starting")
        logger.info("=" * 60)
        
        # Initialize renderer
        self.renderer = SubprocessRenderer(self.config.output_dir)
        
        # Setup UI
        self._setup_window()
        self._apply_theme()
        self._setup_ui()
        self._connect_signals()
        
        # Register GUI log handler
        add_gui_handler(self._on_log_message)
        
        logger.info("Application initialized successfully")
    
    def _setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle(self.config.window_title)
        self.resize(self.config.window_width, self.config.window_height)
        
        # Center on screen
        from PyQt6.QtGui import QScreen
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def _apply_theme(self):
        """Apply dark Fusion theme"""
        app = QApplication.instance()
        app.setStyle("Fusion")
        
        # Dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        app.setPalette(dark_palette)
        
        # Additional stylesheet
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a2a2a;
                border: 1px solid #555555;
            }
            QTabWidget::pane {
                border: 1px solid #3e3e3e;
                background: #2d2d2d;
            }
            QTabBar::tab {
                background: #3e3e3e;
                color: #d4d4d4;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #555555;
            }
            QTabBar::tab:selected {
                background: #4ec9b0;
                color: #000000;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #505050;
            }
            QPushButton {
                padding: 6px 12px;
                background: #3e3e3e;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: #505050;
            }
            QPushButton:pressed {
                background: #2a2a2a;
            }
            QPushButton:disabled {
                background: #2a2a2a;
                color: #666666;
            }
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 3px;
                text-align: center;
                background: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #4ec9b0;
            }
        """)
        
        logger.debug("Dark Fusion theme applied")
    
    def _setup_ui(self):
        """Setup the main UI layout"""
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Main splitter (horizontal: tabs | sidebar)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(self.config.tabs_closable)
        self.tab_widget.setMovable(self.config.tabs_movable)
        self.tab_widget.setDocumentMode(True)
        
        # Add home tab
        self.home_tab = HomeTab(self.config)
        self.tab_widget.addTab(self.home_tab, "🏠 Home")
        
        # Right side: Sidebar with log and output viewers
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar splitter (vertical: output | logs)
        self.sidebar_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Output viewer
        self.output_viewer = OutputViewer()
        
        # Log viewer
        self.log_viewer = LogViewer(max_lines=self.config.log_max_lines)
        
        self.sidebar_splitter.addWidget(self.output_viewer)
        self.sidebar_splitter.addWidget(self.log_viewer)
        self.sidebar_splitter.setSizes([300, 300])  # Equal split
        
        sidebar_layout.addWidget(self.sidebar_splitter)
        
        # Add to main splitter
        self.main_splitter.addWidget(self.tab_widget)
        self.main_splitter.addWidget(sidebar)
        
        # Set initial sizes (70% tabs, 30% sidebar)
        self.main_splitter.setSizes([700, 300])
        
        main_layout.addWidget(self.main_splitter)
        
        logger.debug("UI layout created")
    
    def _connect_signals(self):
        """Connect signals and slots"""
        # Home tab settings
        self.home_tab.settings_changed.connect(self._on_settings_changed)
        self.home_tab.log_message.connect(self._on_tab_log)
        
        # Renderer signals
        self.renderer.progress_updated.connect(self._on_render_progress)
        self.renderer.render_complete.connect(self._on_render_complete)
        self.renderer.render_failed.connect(self._on_render_failed)
        self.renderer.log_message.connect(self._on_renderer_log)
        
        # Tab changes
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        logger.debug("Signals connected")
    
    def add_scene_tab(self, tab_widget, tab_name: str, icon: str = ""):
        """
        Add a new scene tab to the interface
        
        Args:
            tab_widget: The tab widget to add
            tab_name: Display name for the tab
            icon: Optional icon/emoji for the tab
        """
        # Connect tab signals
        if hasattr(tab_widget, 'render_requested'):
            tab_widget.render_requested.connect(self._on_render_requested)
        if hasattr(tab_widget, 'log_message'):
            tab_widget.log_message.connect(self._on_tab_log)
        
        # Add to tab widget
        full_name = f"{icon} {tab_name}" if icon else tab_name
        self.tab_widget.addTab(tab_widget, full_name)
        
        logger.info(f"Tab added: {tab_name}")
    
    def _on_settings_changed(self, settings: dict):
        """Handle global settings changes"""
        logger.info(f"Settings updated: {settings}")
        self.log_viewer.log_success("Settings updated successfully")
    
    def _on_tab_log(self, message: str):
        """Handle log messages from tabs"""
        # Add timestamp if not present
        if not message.startswith('['):
            from datetime import datetime
            timestamp = datetime.now().strftime('%H:%M:%S')
            message = f"[{timestamp}] [INFO] {message}"
        self.log_viewer.append_log(message)
    
    def _on_renderer_log(self, message: str):
        """Handle log messages from renderer"""
        # Messages from subprocess already have timestamp
        # Just ensure they're displayed
        if not message.startswith('['):
            from datetime import datetime
            timestamp = datetime.now().strftime('%H:%M:%S')
            message = f"[{timestamp}] [INFO] {message}"
        self.log_viewer.append_log(message)
    
    def _on_log_message(self, message: str):
        """Handle log messages from loguru"""
        # This receives formatted HTML from loguru
        self.log_viewer.append_log(str(message))
    
    def _on_render_requested(self, scene_dict: dict, params: dict, output_name: str):
        """Handle render request from a tab"""
        # Get global settings
        global_settings = self.home_tab.get_current_settings()
        
        # Merge with tab params (global settings override if not specified)
        merged_params = {
            'spp': params.get('spp', global_settings['spp']),
            'variant': params.get('variant', global_settings['variant']),
            'integrator': params.get('integrator', 'path'),
        }
        
        logger.info(f"Render request: {output_name} with params: {merged_params}")
        
        # Start rendering
        self.renderer.render_scene(scene_dict, merged_params, output_name)
    
    def _on_render_progress(self, progress: int):
        """Handle render progress updates"""
        # Update current tab's progress bar
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'update_progress'):
            current_tab.update_progress(progress)
    
    def _on_render_complete(self, image_array, output_path: str):
        """Handle render completion"""
        # Update current tab
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'on_render_complete'):
            current_tab.on_render_complete()
        
        # Display in output viewer
        self.output_viewer.display_image(image_path=output_path)
        
        # Log success
        self.log_viewer.log_success(f"Render complete: {Path(output_path).name}")
        logger.success(f"Render displayed: {output_path}")
    
    def _on_render_failed(self, error: str):
        """Handle render failure"""
        # Update current tab
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'on_render_failed'):
            current_tab.on_render_failed(error)
        
        # Log error
        self.log_viewer.log_error(error)
    
    def _on_tab_changed(self, index: int):
        """Handle tab changes"""
        tab = self.tab_widget.widget(index)
        tab_name = self.tab_widget.tabText(index)
        logger.debug(f"Tab switched to: {tab_name}")
    
    def closeEvent(self, event):
        """Handle window close"""
        # Cancel any ongoing render
        try:
            # Check if subprocess renderer has an active process
            if hasattr(self.renderer, 'process') and self.renderer.process is not None:
                if self.renderer.process.state() == QProcess.ProcessState.Running:
                    reply = QMessageBox.question(
                        self,
                        "Render in Progress",
                        "A render is currently in progress. Cancel and quit?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        self.renderer.cancel_render()
                        # Give process time to terminate
                        self.renderer.process.waitForFinished(2000)
                        event.accept()
                    else:
                        event.ignore()
                        return
                
                # Clean up renderer resources
                if hasattr(self.renderer, 'cleanup'):
                    self.renderer.cleanup()
                    
            # Handle old threaded renderer (if used)
            elif hasattr(self.renderer, 'current_worker') and self.renderer.current_worker is not None:
                if self.renderer.current_worker.isRunning():
                    reply = QMessageBox.question(
                        self,
                        "Render in Progress",
                        "A render is currently in progress. Cancel and quit?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        self.renderer.cancel_render()
                        event.accept()
                    else:
                        event.ignore()
                        return
        except Exception as e:
            logger.error(f"Error during close event: {e}")
            # Continue with close anyway
        
        logger.info("Application closing gracefully")
        event.accept()
