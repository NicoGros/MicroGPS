"""
Application state.

This module contains the global application state shared by the
service and GUI layers.

The state should never contain GUI objects (widgets, scenes, etc.),
only application data.
"""

from dataclasses import dataclass, field

import numpy as np

from MicroGPS.models import Point, AffineTransform


@dataclass
class AppState:
    """Global application state."""

    # ==================================================================
    # Image
    # ==================================================================

    image: np.ndarray | None = None
    image_path: str | None = None

    image_width: int = 0
    image_height: int = 0

    scale_x: float = 1.0
    scale_y: float = 1.0

    x_min_real: float = 0.0
    x_max_real: float = 1.0

    y_min_real: float = 0.0
    y_max_real: float = 1.0

    # ==================================================================
    # Project
    # ==================================================================

    points: list[Point] = field(default_factory=list)

    transforms: dict[str, AffineTransform] = field(default_factory=dict)

    current_system: str = "image"

    selected_point: Point | None = None

    project_modified: bool = False


# Singleton application state
state = AppState()