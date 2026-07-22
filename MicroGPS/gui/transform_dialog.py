"""
MicroGPS

Interactive image registration and coordinate transformation tool for
scientific surface analysis.

Transformation dialog.

Collects calibration coordinates and computes affine transformations
between image and user-defined coordinate systems.

Copyright (c) 2026 Nicolas Gros

Licensed under the ? License.
See the LICENSE file in the project root for details.
"""


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QDialogButtonBox,
    QMessageBox,
)

from MicroGPS.state import state
from MicroGPS.services import compute_transform


class TransformDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New Coordinate System")

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.name = QLineEdit()

        form.addRow("System name", self.name)

        self.spinboxes = []

        for i in range(3):

            sx = QDoubleSpinBox()
            sy = QDoubleSpinBox()

            sx.setDecimals(6)
            sy.setDecimals(6)

            sx.setRange(-1e12, 1e12)
            sy.setRange(-1e12, 1e12)

            self.spinboxes.append((sx, sy))

            form.addRow(f"CP{i+1} X", sx)
            form.addRow(f"CP{i+1} Y", sy)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.compute)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def compute(self):

        name = self.name.text().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Enter a system name.")
            return

        calibration = [
            p for p in state.points
            if p.is_calibration
        ]

        if len(calibration) != 3:
            QMessageBox.warning(
                self,
                "Error",
                "Exactly three calibration points are required."
            )
            return

        src = []
        dst = []

        for point, (sx, sy) in zip(calibration, self.spinboxes):

            src.append(
                (
                    point.image_x,
                    point.image_y,
                )
            )

            dst.append(
                (
                    sx.value(),
                    sy.value(),
                )
            )

        compute_transform(
            src,
            dst,
            name,
        )

        self.accept()
