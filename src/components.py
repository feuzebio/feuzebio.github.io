from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class UIComponent:
    """Represents a single component in the UI hierarchy."""
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    layout_params: Dict[str, Any] = field(default_factory=dict)
    children: List['UIComponent'] = field(default_factory=list)

@dataclass
class DevicePreset:
    """Represents a device screen configuration."""
    name: str
    width: int
    height: int