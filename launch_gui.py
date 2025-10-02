"""
Mitsuba 3 Render Studio - GUI Launcher
A professional PyQt6 interface for Mitsuba 3 rendering
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from gui.core.main_window import MainWindow
from gui.tabs.basic_scene_tab import BasicSceneTab
from gui.tabs.materials_showcase_tab import MaterialsShowcaseTab
from gui.tabs.lighting_techniques_tab import LightingTechniquesTab
from gui.tabs.glass_demo_tab import GlassDemoTab
from gui.tabs.cornell_box_tab import CornellBoxTab
from gui.tabs.custom_mesh_tab import CustomMeshTab
from gui.tabs.inverse_rendering_tab import InverseRenderingTab
from loguru import logger


def main():
    """Launch the GUI application"""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Mitsuba 3 Render Studio")
    app.setOrganizationName("Mitsuba3-Learning-Demos")
    
    try:
        # Create main window
        window = MainWindow()
        
        # Add scene tabs in progressive learning order
        
        # 1. Basic fundamentals
        basic_tab = BasicSceneTab()
        window.add_scene_tab(basic_tab, "Basic Scene", "🔮")
        
        # 2. Material comparison
        materials_tab = MaterialsShowcaseTab()
        window.add_scene_tab(materials_tab, "Materials", "💎")
        
        # 3. Lighting techniques
        lighting_tab = LightingTechniquesTab()
        window.add_scene_tab(lighting_tab, "Lighting", "💡")
        
        # 4. Glass and transparency
        glass_tab = GlassDemoTab()
        window.add_scene_tab(glass_tab, "Glass", "🔬")
        
        # 5. Global illumination
        cornell_tab = CornellBoxTab()
        window.add_scene_tab(cornell_tab, "Cornell Box", "📦")
        
        # 6. Custom mesh loading
        custom_mesh_tab = CustomMeshTab()
        window.add_scene_tab(custom_mesh_tab, "Custom Mesh", "🎨")
        
        # 7. Inverse rendering (2D→3D)
        inverse_tab = InverseRenderingTab()
        window.add_scene_tab(inverse_tab, "Inverse Rendering", "🔄")
        
        # Show window
        window.show()
        
        logger.info("GUI launched successfully")
        logger.info("7 scene tabs loaded: Basic → Materials → Lighting → Glass → Cornell Box → Custom Mesh → Inverse Rendering")
        logger.info("Select a scene tab and adjust parameters to render")
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.exception(f"Failed to launch GUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
