"""
MicroGPS

Image viewer based on pyqtgraph.
"""

import numpy as np
import pyqtgraph as pg

from PySide6.QtCore import Qt, Signal

from MicroGPS.state import state
from MicroGPS.services import add_point

from MicroGPS.gui.point_item import PointItem

pointsChanged = Signal()

class ImageView(pg.PlotWidget):
    """
    Central image viewer.
    """

    mousePositionChanged = Signal(float, float)
    pointsChanged = Signal()

    def __init__(self):
        super().__init__()

        self.add_point_mode = False

        # ----------------------------------------------------------
        # Plot configuration
        # ----------------------------------------------------------

        self.setBackground("white")

        self.plotItem.hideAxis("left")
        self.plotItem.hideAxis("bottom")

        self.plotItem.setAspectLocked(True)

        self.viewbox = self.plotItem.getViewBox()

        self.viewbox.setMouseMode(pg.ViewBox.PanMode)

        # image coordinates start in upper-left
        self.viewbox.invertY(True)

        # ----------------------------------------------------------
        # Image item
        # ----------------------------------------------------------

        self.image_item = pg.ImageItem()

        self.plotItem.addItem(self.image_item)

        self.point_items = []

        # ----------------------------------------------------------
        # Signals
        # ----------------------------------------------------------

        self.scene().sigMouseMoved.connect(
            self._mouse_moved
        )

        self.scene().sigMouseClicked.connect(
            self._mouse_clicked
        )

    # ==============================================================
    # Public API
    # ==============================================================

    def set_add_point_mode(self, enabled: bool):

        self.add_point_mode = enabled

    def refresh(self):

        self.load_image()

    def fit_image(self):

        self.viewbox.autoRange()

    # ==============================================================
    # Image
    # ==============================================================

    def load_image(self):

        if state.image is None:
            return

        image = np.asarray(state.image)

        # pyqtgraph expects x,y ordering
        if image.ndim == 2:

            image = image.T

        else:

            image = np.transpose(image, (1, 0, 2))

        self.image_item.setImage(image)

        h = state.image_height
        w = state.image_width

        self.image_item.setRect(0, 0, w, h)

        self.fit_image()

        self.refresh_points()
        self.pointsChanged.emit()

    # ==============================================================
    # Points
    # ==============================================================

    def refresh_points(self):

        for item in self.point_items:
            self.plotItem.removeItem(item)

        self.point_items.clear()

        for point in state.points:

            item = PointItem(point)

            self.plotItem.addItem(item)

            self.point_items.append(item)

    # ==============================================================
    # Mouse interaction
    # ==============================================================

    def _mouse_moved(self, pos):
        """
        Emit mouse coordinates in image space.
        """

        if state.image is None:
            return

        if not self.sceneBoundingRect().contains(pos):
            return

        mouse = self.viewbox.mapSceneToView(pos)

        self.mousePositionChanged.emit(
            mouse.x(),
            mouse.y(),
        )

    def _mouse_clicked(self, event):
        """
        Add a point when add-point mode is enabled.
        """

        if state.image is None:
            return

        if not self.add_point_mode:
            return

        if event.button() != Qt.LeftButton:
            return

        mouse = self.viewbox.mapSceneToView(
            event.scenePos()
        )

        add_point(
            mouse.x(),
            mouse.y(),
        )

        self.refresh_points()
        self.pointsChanged.emit()

    # ==============================================================
    # Utilities
    # ==============================================================

    def clear_points(self):

        for item in self.point_items:
            self.plotItem.removeItem(item)

        self.point_items.clear()

    def zoom_in(self):
        self.viewbox.scaleBy((0.8, 0.8))

    def zoom_out(self):
        self.viewbox.scaleBy((1.25, 1.25))

    def reset_view(self):
        self.fit_image()