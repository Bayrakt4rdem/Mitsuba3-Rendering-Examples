"""
Application configuration settings
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any


@dataclass
class AppConfig:
    """Global application configuration"""
    
    # Application info
    app_name: str = "Mitsuba 3 Render Studio"
    app_version: str = "1.0.0"
    
    # Paths
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    output_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "output")
    log_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "logs")
    
    # Window settings
    window_width: int = 1400
    window_height: int = 900
    window_title: str = "Mitsuba 3 Render Studio"
    
    # Theme
    theme: str = "Fusion"
    dark_mode: bool = True
    
    # Rendering defaults
    default_resolution: tuple = (800, 600)
    default_spp: int = 256  # samples per pixel
    default_variant: str = "scalar_rgb"
    
    # GUI settings
    sidebar_width: int = 400
    log_max_lines: int = 1000
    enable_auto_scroll: bool = True
    
    # Tab settings
    tabs_movable: bool = True
    tabs_closable: bool = False
    
    def __post_init__(self):
        """Ensure directories exist"""
        self.output_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "window_width": self.window_width,
            "window_height": self.window_height,
            "theme": self.theme,
            "dark_mode": self.dark_mode,
            "default_resolution": self.default_resolution,
            "default_spp": self.default_spp,
            "default_variant": self.default_variant,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        """Create config from dictionary"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})
