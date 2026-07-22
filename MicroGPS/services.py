"""
MicroGPS

Interactive image registration and coordinate transformation tool for
scientific surface analysis.

Copyright (c) 2026 Nicolas Gros

Licensed under the ? License.
See the LICENSE file in the project root for details.
"""

from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from MicroGPS.core.report_utils import build_report_dataframe
from MicroGPS.core.transform_utils import compute_affine_matrix
from MicroGPS.models import AffineTransform, Point
from MicroGPS.state import state


# =============================================================================
# IMAGE
# =============================================================================


def load_image(path: str | Path) -> None:
    """
    Load an image from disk into the application state.

    Parameters
    ----------
    path
        Image filename.
    """

    image = Image.open(path)

    state.image = np.asarray(image)
    state.image_path = str(path)

    state.image_height, state.image_width = state.image.shape[:2]
    state.project_modified = True


def load_image_from_bytes(file_bytes: bytes) -> None:
    """
    Load an image from raw bytes.

    Useful for project import or drag-and-drop.
    """

    image = Image.open(BytesIO(file_bytes))

    state.image = np.asarray(image)
    state.image_path = None

    state.image_height, state.image_width = state.image.shape[:2]
    state.project_modified = True


# =============================================================================
# POINTS
# =============================================================================


def add_point(x: float, y: float, system: str = "image") -> Point:
    """
    Add a point to the current project.

    The first three points are calibration points.
    Subsequent points are measurement points.
    """

    kind = (
        "calibration"
        if count_calibration_points() < 3
        else "measurement"
    )

    label = (
        f"CP{count_calibration_points() + 1}"
        if kind == "calibration"
        else f"MP{count_measurement_points() + 1}"
    )

    point = Point(
        label=label,
        kind=kind,
        image_x=x,
        image_y=y,
    )

    state.points.append(point)
    state.project_modified = True

    return point


def get_calibration_points() -> list[Point]:
    """Return calibration points."""

    return [p for p in state.points if p.kind == "calibration"]


def get_measurement_points() -> list[Point]:
    """Return measurement points."""

    return [p for p in state.points if p.kind == "measurement"]


def count_calibration_points() -> int:
    return len(get_calibration_points())


def count_measurement_points() -> int:
    return len(get_measurement_points())


def clear_points(kind: str | None = None) -> None:
    """
    Clear project points.

    Parameters
    ----------
    kind
        "calibration", "measurement", or None for all points.
    """

    if kind is None:

        state.points.clear()
        state.transforms.clear()

    elif kind == "calibration":

        state.points = [
            p for p in state.points
            if p.kind != "calibration"
        ]

        #state.transforms.clear()

    elif kind == "measurement":

        state.points = [
            p for p in state.points
            if p.kind != "measurement"
        ]

    state.selected_point = None
    state.project_modified = True

def remove_points(points_to_remove: list[Point]) -> None:
    """
    Remove a list of points from the project.
    """

    for p in points_to_remove:
        if p in state.points:
            state.points.remove(p)

    # If a calibration point was removed,
    # previously computed transforms are no longer valid.
    if any(p.is_calibration for p in points_to_remove):
        state.transforms.clear()
        state.current_system = "image"

    state.selected_point = None
    state.project_modified = True


def remove_transform(name: str):

    if name in state.transforms:
        del state.transforms[name]

    if state.current_system == name:
        state.current_system = "image"

    state.project_modified = True

# =============================================================================
# TRANSFORMS
# =============================================================================


def compute_transform(
    src_points: list[tuple[float, float]],
    dst_points: list[tuple[float, float]],
    system_name: str,
) -> AffineTransform:
    """
    Compute and store an affine transformation.

    Returns
    -------
    AffineTransform
        The newly created transform.

    Raises
    ------
    ValueError
        If the point lists are invalid.
    """

    if len(src_points) != 3:
        raise ValueError("Exactly three source points are required.")

    if len(dst_points) != 3:
        raise ValueError("Exactly three destination points are required.")

    matrix = compute_affine_matrix(src_points, dst_points)

    transform = AffineTransform(
        name=system_name,
        matrix=matrix,
    )

    state.transforms[system_name] = transform
    state.current_system = system_name
    state.project_modified = True

    return transform


def image_to_coordinates(
    image_x: float,
    image_y: float,
    system: str,
) -> tuple[float, float]:
    """
    Convert image coordinates into a coordinate system.
    """

    if system == "image":
        return image_x, image_y

    transform = state.transforms[system]

    vec = np.array([image_x, image_y, 1.0])

    x, y, _ = transform.matrix @ vec

    return float(x), float(y)


def coordinates_to_image(
    x: float,
    y: float,
    system: str,
) -> tuple[float, float]:
    """
    Convert coordinates from a coordinate system back to image coordinates.
    """

    if system == "image":
        return x, y

    transform = state.transforms[system]

    inv = np.linalg.inv(transform.matrix)

    vec = np.array([x, y, 1.0])

    image_x, image_y, _ = inv @ vec

    return float(image_x), float(image_y)


# =============================================================================
# REPORT
# =============================================================================


def get_report_df() -> pd.DataFrame:
    """
    Build the current project report.
    """

    return build_report_dataframe()


# =============================================================================
# EXPORT
# =============================================================================


def export_points(filepath: str | Path) -> None:
    """
    Export points and transforms to a text file.
    """

    df = build_report_dataframe()

    if df.empty:
        raise ValueError("There is no data to export.")

    with open(filepath, "w", encoding="utf-8") as f:

        f.write("# MicroGPS export\n")

        for name, transform in state.transforms.items():

            params = transform.matrix.flatten()

            f.write(
                f"# Transform {name} "
                + " ".join(f"{value:.6f}" for value in params)
                + "\n"
            )

        df.to_csv(
            f,
            sep="\t",
            index=False,
        )


# =============================================================================
# RESET
# =============================================================================


def reset_all() -> None:
    """
    Reset the application state.
    """

    state.image = None
    state.image_path = None

    state.image_width = 0
    state.image_height = 0

    state.points.clear()
    state.transforms.clear()

    state.current_system = "image"
    state.selected_point = None

    state.project_modified = False


