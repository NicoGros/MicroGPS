"""
MicroGPS 3.0

Report utilities.

Builds tabular representations of all points and their transformed
coordinates for display/export.
"""

import numpy as np
import pandas as pd

from MicroGPS.state import state


def build_report_dataframe() -> pd.DataFrame:
    """
    Build a dataframe containing all points and their transformed
    coordinates in every available coordinate system.

    Returns
    -------
    pd.DataFrame
        Flattened table of all points with transformed coordinates.
    """

    if not state.points:
        return pd.DataFrame()

    rows = []

    for point in state.points:

        row = {
            "label": point.label,
            "kind": point.kind,
            "image_x": point.image_x,
            "image_y": point.image_y,
        }

        # Homogeneous coordinates
        p = np.array([point.image_x, point.image_y, 1.0])

        # Apply all transforms
        for system_name, transform in state.transforms.items():

            t = transform.matrix @ p

            row[f"{system_name}_x"] = round(float(t[0]), 2)
            row[f"{system_name}_y"] = round(float(t[1]), 2)

            # also store inside point (optional but useful)
            point.coordinates[system_name] = (float(t[0]), float(t[1]))

        rows.append(row)

    return pd.DataFrame(rows)