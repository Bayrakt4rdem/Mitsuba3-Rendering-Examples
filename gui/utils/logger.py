"""
Loguru-based logging configuration for the GUI application
Provides unified logging with file rotation and GUI integration
"""

import sys
from pathlib import Path
from loguru import logger
from typing import Optional

# Store GUI log handler reference
_gui_log_handler = None


def setup_logger(log_dir: Optional[Path] = None) -> None:
    """
    Configure loguru for the application
    
    Args:
        log_dir: Directory for log files (default: project_root/logs)
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="DEBUG",
        colorize=True
    )
    
    # Setup log directory
    if log_dir is None:
        log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Add file handler with rotation
    logger.add(
        log_dir / "mitsuba_gui_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )
    
    logger.info("Logging system initialized")


def add_gui_handler(handler_func):
    """
    Add a custom handler for GUI log display
    
    Args:
        handler_func: Callable that receives log messages
    """
    global _gui_log_handler
    
    def gui_sink(message):
        """Custom sink that calls the GUI handler"""
        if _gui_log_handler:
            _gui_log_handler(message)
    
    _gui_log_handler = handler_func
    logger.add(
        gui_sink,
        format="[{time:HH:mm:ss}] [{level}] {message}",
        level="INFO",
        colorize=False  # No ANSI colors for GUI
    )
    logger.debug("GUI log handler registered")


def get_logger(name: str = None):
    """
    Get a logger instance
    
    Args:
        name: Optional name for the logger context
        
    Returns:
        Configured logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger
