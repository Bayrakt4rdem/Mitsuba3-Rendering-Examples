# GUI Module Structure

Professional PyQt6-based GUI for Mitsuba 3 rendering with parametric scene controls.

## Architecture

```
gui/
├── core/               # Core application components
│   ├── config.py      # Application configuration
│   └── main_window.py # Main window with dark Fusion theme
├── widgets/           # Reusable UI widgets
│   ├── log_viewer.py  # Terminal-style log display
│   ├── output_viewer.py # Image viewer with zoom/pan
│   └── parameter_widget.py # Dynamic parameter controls
├── tabs/              # Scene-specific tab modules
│   ├── base_tab.py    # Abstract base class for tabs
│   ├── home_tab.py    # Welcome and settings tab
│   ├── basic_scene_tab.py # Basic sphere scene
│   └── cornell_box_tab.py # Cornell Box scene
└── utils/             # Utility modules
    ├── logger.py      # Loguru logging setup
    └── renderer.py    # Mitsuba renderer wrapper
```

## Features

### Main Window
- **Dark Fusion Theme**: Professional dark theme for comfortable viewing
- **Draggable Tabs**: Reorder tabs with drag & drop
- **Resizable Sidebar**: Adjust log/output viewer sizes
- **Dual Display**: Side-by-side log console and image viewer

### Logging System
- **Unified Logging**: All components log to central console
- **Color-Coded**: Different colors for INFO, WARN, ERROR, SUCCESS
- **Auto-Scroll**: Optional auto-scroll to latest messages
- **File Logging**: Automatic rotation and compression
- **Location**: Logs saved to `logs/` directory

### Parameter Controls
- **Dynamic UI**: Parameters auto-generate appropriate controls
- **Real-Time Updates**: Changes reflected immediately
- **Type-Safe**: Integer, float, boolean, choice, slider controls
- **Tooltips**: Helpful descriptions for each parameter

### Rendering
- **Async Rendering**: Non-blocking renders in background threads
- **Progress Tracking**: Real-time progress bars
- **Cancel Support**: Stop renders mid-execution
- **Auto-Display**: Results shown immediately in viewer

## Adding New Scene Tabs

1. **Create Scene Generator** (`gui_examples/your_scene.py`):
```python
class YourSceneGenerator:
    @staticmethod
    def generate(params: Dict[str, Any]) -> Dict[str, Any]:
        # Build and return Mitsuba scene dictionary
        return scene_dict
```

2. **Create Tab Class** (`gui/tabs/your_scene_tab.py`):
```python
from gui.tabs.base_tab import BaseTab
from gui.widgets.parameter_widget import ParameterWidget

class YourSceneTab(BaseTab):
    def setup_ui(self):
        # Add parameter widgets
        self.params = ParameterWidget("Parameters")
        self.params.add_float_parameter('size', 'Size:', ...)
        self.content_layout.addWidget(self.params)
    
    def get_scene_dict(self, params):
        # Convert UI params to scene
        return YourSceneGenerator.generate(...)
    
    def get_default_params(self):
        return {'spp': 256, 'integrator': 'path'}
```

3. **Register in Launcher** (`launch_gui.py`):
```python
from gui.tabs.your_scene_tab import YourSceneTab

your_tab = YourSceneTab()
window.add_scene_tab(your_tab, "Your Scene", "🎨")
```

## Code Guidelines

- **Modular Design**: Each file < 300 lines (2000-3000 max per module)
- **Type Hints**: All functions use type annotations
- **Docstrings**: All classes and public methods documented
- **Error Handling**: Try/catch with proper logging
- **Separation of Concerns**: UI ≠ Logic ≠ Rendering

## Dependencies

- PyQt6 >= 6.4.0 - GUI framework
- loguru >= 0.6.0 - Logging system
- mitsuba >= 3.0.0 - Rendering engine
- numpy, Pillow - Image processing
