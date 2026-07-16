"""
Application data models.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass(slots=True)
class Point:
    """
    A project point.

    Calibration points define affine transformations.
    Measurement points are transformed into one or more coordinate systems.
    """

    label: str

    kind: str
    # "calibration" or "measurement"

    image_x: float
    image_y: float

    coordinates: dict[str, tuple[float, float]] = field(default_factory=dict)

    @property
    def is_calibration(self) -> bool:
        """Return True if this is a calibration point."""
        return self.kind == "calibration"

    @property
    def is_measurement(self) -> bool:
        """Return True if this is a measurement point."""
        return self.kind == "measurement"


@dataclass(slots=True)
class AffineTransform:
    """
    Affine transformation between image coordinates and a coordinate system.
    """

    name: str

    matrix: np.ndarray