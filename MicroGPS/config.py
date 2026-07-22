"""
MicroGPS

Interactive image registration and coordinate transformation tool for
scientific surface analysis.

Application configuration.

Defines global constants, default settings, colours and user-adjustable
parameters used throughout the application.

Copyright (c) 2026 Nicolas Gros

Licensed under the ? License.
See the LICENSE file in the project root for details.
"""

BASE_DATA_DIRECTORY = ...

# Supported image file extensions
IMAGE_EXTENSIONS = (
    ".bmp",
    ".gif",
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
)

# Default export filename
DEFAULT_EXPORT_FILE = "MicroGPS_coordinates.txt"

# Point label prefixes
CALIBRATION_PREFIX = "CP"
MEASUREMENT_PREFIX = "MP"
