"""
Parameter widget for controlling scene parameters
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QSpinBox, 
    QDoubleSpinBox, QComboBox, QLineEdit, QCheckBox,
    QGroupBox, QSlider, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any
from loguru import logger


class ParameterWidget(QWidget):
    """
    Widget for creating parameter controls
    Supports: int, float, bool, string, choice
    """
    
    parameters_changed = pyqtSignal(dict)  # Emits parameter dict when values change
    
    def __init__(self, title: str = "Parameters", parent=None):
        super().__init__(parent)
        self.title = title
        self.controls = {}
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Group box for parameters
        self.group_box = QGroupBox(self.title)
        self.form_layout = QFormLayout()
        self.group_box.setLayout(self.form_layout)
        
        layout.addWidget(self.group_box)
        layout.addStretch()
    
    def add_int_parameter(
        self, 
        name: str, 
        label: str, 
        default: int = 0, 
        min_val: int = 0, 
        max_val: int = 1000,
        tooltip: str = ""
    ):
        """Add an integer parameter with spinbox"""
        spinbox = QSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default)
        spinbox.setToolTip(tooltip)
        spinbox.valueChanged.connect(lambda: self._emit_changes())
        
        self.controls[name] = spinbox
        self.form_layout.addRow(label, spinbox)
    
    def add_float_parameter(
        self, 
        name: str, 
        label: str, 
        default: float = 0.0, 
        min_val: float = 0.0, 
        max_val: float = 100.0,
        decimals: int = 2,
        step: float = 0.1,
        tooltip: str = ""
    ):
        """Add a float parameter with spinbox"""
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(step)
        spinbox.setToolTip(tooltip)
        spinbox.valueChanged.connect(lambda: self._emit_changes())
        
        self.controls[name] = spinbox
        self.form_layout.addRow(label, spinbox)
    
    def add_slider_parameter(
        self,
        name: str,
        label: str,
        default: int = 50,
        min_val: int = 0,
        max_val: int = 100,
        tooltip: str = ""
    ):
        """Add an integer parameter with slider and value display"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.setToolTip(tooltip)
        
        value_label = QLabel(str(default))
        value_label.setMinimumWidth(40)
        
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        slider.valueChanged.connect(lambda: self._emit_changes())
        
        layout.addWidget(slider)
        layout.addWidget(value_label)
        
        self.controls[name] = slider
        self.form_layout.addRow(label, container)
    
    def add_choice_parameter(
        self, 
        name: str, 
        label: str, 
        choices: list, 
        default: str = None,
        tooltip: str = ""
    ):
        """Add a choice parameter with combobox"""
        combobox = QComboBox()
        combobox.addItems(choices)
        if default and default in choices:
            combobox.setCurrentText(default)
        combobox.setToolTip(tooltip)
        combobox.currentTextChanged.connect(lambda: self._emit_changes())
        
        self.controls[name] = combobox
        self.form_layout.addRow(label, combobox)
    
    def add_bool_parameter(
        self, 
        name: str, 
        label: str, 
        default: bool = False,
        tooltip: str = ""
    ):
        """Add a boolean parameter with checkbox"""
        checkbox = QCheckBox()
        checkbox.setChecked(default)
        checkbox.setToolTip(tooltip)
        checkbox.stateChanged.connect(lambda: self._emit_changes())
        
        self.controls[name] = checkbox
        self.form_layout.addRow(label, checkbox)
    
    def add_string_parameter(
        self, 
        name: str, 
        label: str, 
        default: str = "",
        tooltip: str = ""
    ):
        """Add a string parameter with line edit"""
        lineedit = QLineEdit()
        lineedit.setText(default)
        lineedit.setToolTip(tooltip)
        lineedit.textChanged.connect(lambda: self._emit_changes())
        
        self.controls[name] = lineedit
        self.form_layout.addRow(label, lineedit)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current parameter values as dictionary"""
        params = {}
        
        for name, control in self.controls.items():
            if isinstance(control, QSpinBox) or isinstance(control, QSlider):
                params[name] = control.value()
            elif isinstance(control, QDoubleSpinBox):
                params[name] = control.value()
            elif isinstance(control, QComboBox):
                params[name] = control.currentText()
            elif isinstance(control, QCheckBox):
                params[name] = control.isChecked()
            elif isinstance(control, QLineEdit):
                params[name] = control.text()
        
        return params
    
    def set_parameter(self, name: str, value: Any):
        """Set a parameter value programmatically"""
        if name not in self.controls:
            logger.warning(f"Parameter '{name}' not found")
            return
        
        control = self.controls[name]
        
        if isinstance(control, (QSpinBox, QSlider)):
            control.setValue(int(value))
        elif isinstance(control, QDoubleSpinBox):
            control.setValue(float(value))
        elif isinstance(control, QComboBox):
            control.setCurrentText(str(value))
        elif isinstance(control, QCheckBox):
            control.setChecked(bool(value))
        elif isinstance(control, QLineEdit):
            control.setText(str(value))
    
    def reset_to_defaults(self):
        """Reset all parameters to their default values"""
        # This would require storing defaults - can be implemented if needed
        logger.debug("Reset to defaults requested")
    
    def _emit_changes(self):
        """Emit signal when parameters change"""
        params = self.get_parameters()
        self.parameters_changed.emit(params)
