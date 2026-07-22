"""
MicroGPS

Interactive image registration and coordinate transformation tool for
scientific surface analysis.

Global application state.

Stores the current project data (image, points, coordinate systems,
transformations and application settings) shared across the application.

Copyright (c) 2026 Nicolas Gros

Licensed under the ? License.
See the LICENSE file in the project root for details.
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
