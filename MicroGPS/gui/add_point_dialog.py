"""
MicroGPS

Interactive image registration and coordinate transformation tool for
scientific surface analysis.

Point creation dialog.

Provides the user interface for creating and editing project points.

Copyright (c) 2026 Nicolas Gros

Licensed under the ? License.
See the LICENSE file in the project root for details.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
)

from MicroGPS.services import add_point, coordinates_to_image
from MicroGPS.state import state


class AddPointDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Add Point")

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.system = QComboBox()

        self.system.addItem("image")

        for name in state.transforms:
            self.system.addItem(name)

        form.addRow("Coordinate system", self.system)

        self.x = QDoubleSpinBox()
        self.y = QDoubleSpinBox()

        self.x.setDecimals(6)
        self.y.setDecimals(6)

        self.x.setRange(-1e12, 1e12)
        self.y.setRange(-1e12, 1e12)

        form.addRow("X", self.x)
        form.addRow("Y", self.y)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept_dialog)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def accept_dialog(self):

        system = self.system.currentText()

        image_x, image_y = coordinates_to_image(
            self.x.value(),
            self.y.value(),
            system,
        )

        add_point(image_x, image_y)

        self.accept()
