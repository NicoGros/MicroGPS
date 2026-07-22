"""
MicroGPS

Interactive image registration and coordinate transformation tool for
scientific surface analysis.

Main application window.

Creates the graphical user interface, including menus, toolbars,
dockable widgets and user interactions.

Copyright (c) 2026 Nicolas Gros

Licensed under the ? License.
See the LICENSE file in the project root for details.
"""

from pathlib import Path

from MicroGPS.services import (
    load_image,
    export_points,
    image_to_coordinates,
)

from MicroGPS.gui.image_view import ImageView
from MicroGPS.gui.transform_dialog import TransformDialog
from MicroGPS.gui.add_point_dialog import AddPointDialog
from MicroGPS.state import state

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox, 
    QDockWidget, 
    QTableWidget, 
    QTableWidgetItem
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MicroGPS")
        self.resize(1400, 900)
                
        # ==========================================================
        # Central image viewer
        # ==========================================================

        self.view = ImageView()

        self.setCentralWidget(self.view)

        self.view.mousePositionChanged.connect(
            self.update_mouse_position
        )
        self.view.pointsChanged.connect(
            self.refresh_point_table
        )

        # ==========================================================
        # Build UI
        # ==========================================================

        self._create_actions()
        self._create_point_table()
        self._create_menu()
        self._create_toolbar()
        self._create_status_bar()

    # ==========================================================
    # UI
    # ==========================================================

    def _create_actions(self):
        """
        Create all actions.
        """

        self.open_action = QAction("Open Image", self)
        self.open_action.triggered.connect(
            self.on_open_image
        )

        self.export_action = QAction("Export", self)
        self.export_action.triggered.connect(
            self.on_export
        )

        self.refresh_action = QAction("Refresh", self)
        self.refresh_action.triggered.connect(
            self.on_refresh
        )

        self.fit_action = QAction("Resize image", self)
        self.fit_action.triggered.connect(
            self.view.fit_image
        )

        self.add_point_action = QAction("Add Point by Cliking", self)
        self.add_point_action.setCheckable(True)
        self.add_point_action.toggled.connect(
            self.view.set_add_point_mode
        )

        self.clear_calibration_action = QAction("Clear Calibration", self)
        self.clear_calibration_action.triggered.connect(
            self.on_clear_calibration
        )

        self.clear_measurements_action = QAction("Clear Measurements", self)
        self.clear_measurements_action.triggered.connect(
            self.on_clear_measurements
        )

        self.remove_points_action = QAction(
            "Remove Selected Points",
            self,
        )

        self.remove_points_action.triggered.connect(
            self.on_remove_selected_points
        )

        self.new_system_action = QAction("New Coordinate System", self)
        self.new_system_action.triggered.connect(
            self.on_new_coordinate_system
        )

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(
            self.close
        )

        self.add_point_coordinates_action = QAction(
            "Add Point by Coordinates",
            self,
        )

        self.add_point_coordinates_action.triggered.connect(
            self.on_add_point_coordinates
        )

    # ==========================================================

    def _create_menu(self):

        file_menu = self.menuBar().addMenu("File")

        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        view_menu = self.menuBar().addMenu("View")

        view_menu.addAction(self.refresh_action)
        view_menu.addAction(self.fit_action)
        view_menu.addSeparator()
        view_menu.addAction(self.points_dock.toggleViewAction())

        tools_menu = self.menuBar().addMenu("Tools")

        tools_menu.addAction(self.add_point_action)
        tools_menu.addAction(self.add_point_coordinates_action)
        tools_menu.addSeparator()
        tools_menu.addAction(self.new_system_action)
        tools_menu.addSeparator()
        tools_menu.addAction(self.clear_calibration_action)
        tools_menu.addAction(self.clear_measurements_action)

    # ==========================================================

    def _create_toolbar(self):

        toolbar = self.addToolBar("Main")

        toolbar.setMovable(False)

        toolbar.addAction(self.open_action)
        toolbar.addSeparator()

        toolbar.addAction(self.add_point_action)
        toolbar.addAction(self.add_point_coordinates_action)
        toolbar.addSeparator()

        toolbar.addAction(self.new_system_action)
        toolbar.addSeparator()

        toolbar.addAction(self.fit_action)
        toolbar.addAction(self.refresh_action)
        toolbar.addSeparator()

        toolbar.addAction(self.clear_calibration_action)
        toolbar.addAction(self.clear_measurements_action)
        toolbar.addSeparator()

    # ==========================================================

    def _create_status_bar(self):

        self.statusBar().showMessage("Ready")

    # ==========================================================
    # Slots
    # ==========================================================

    def update_mouse_position(self, x, y):

        text = f"Image: ({x:.1f}, {y:.1f})"

        for name in state.transforms:

            sx, sy = image_to_coordinates(
                x,
                y,
                name,
            )

            text += f"    |    {name}: ({sx:.2f}, {sy:.2f})"

        self.statusBar().showMessage(text)

    # ==========================================================

    def on_open_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.tif *.tiff *.bmp)",
        )

        if not file_path:
            return

        try:

            load_image(Path(file_path))

            self.view.load_image()
            self.refresh_point_table()
            self.refresh_system_table()

            self.statusBar().showMessage(
                f"Loaded: {Path(file_path).name}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e),
            )

    # ==========================================================

    def on_export(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export",
            "points_export.txt",
            "Text files (*.txt)",
        )

        if not file_path:
            return

        try:

            export_points(file_path)

            QMessageBox.information(
                self,
                "Export",
                "Export successful."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Error",
                str(e),
            )

    # ==========================================================

    def on_refresh(self):

        try:
            self.refresh_point_table()
            self.refresh_system_table()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                str(e),
            )
    
    def _create_point_table(self):

        from PySide6.QtWidgets import (
            QWidget,
            QVBoxLayout,
            QPushButton,
            QLabel,
            QAbstractItemView,
        )
        from PySide6.QtGui import QShortcut, QKeySequence

        # ==========================================================
        # Points table
        # ==========================================================

        self.point_table = QTableWidget()

        self.point_table.setColumnCount(4)
        self.point_table.setHorizontalHeaderLabels(
            ["Label", "Type", "Image X", "Image Y"]
        )

        self.point_table.setAlternatingRowColors(True)

        self.point_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.point_table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.point_table.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.EditKeyPressed
        )

        # ==========================================================
        # Buttons
        # ==========================================================

        self.remove_points_button = QPushButton(
            "Remove selected point(s)"
        )

        self.remove_points_button.clicked.connect(
            self.on_remove_selected_points
        )

        # ==========================================================
        # Coordinate systems table
        # ==========================================================

        self.system_table = QTableWidget()

        self.system_table.setColumnCount(2)
        self.system_table.setHorizontalHeaderLabels(
            ["System", "Affine transform"]
        )

        self.system_table.setAlternatingRowColors(True)

        self.system_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.system_table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.remove_system_button = QPushButton(
            "Remove selected coordinate system"
        )

        self.remove_system_button.clicked.connect(
            self.on_remove_selected_system
        )

        # ==========================================================
        # Export
        # ==========================================================

        self.export_table_button = QPushButton(
            "Export point table and systems"
        )

        self.export_table_button.clicked.connect(
            self.on_export
        )

        # ==========================================================
        # Layout
        # ==========================================================

        container = QWidget()

        layout = QVBoxLayout(container)

        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        layout.addWidget(self.point_table)
        layout.addWidget(self.remove_points_button)

        layout.addWidget(QLabel("<b>Coordinate systems</b>"))

        layout.addWidget(self.system_table)
        layout.addWidget(self.remove_system_button)

        layout.addWidget(self.export_table_button)

        # ==========================================================
        # Dock
        # ==========================================================

        self.points_dock = QDockWidget("Points", self)
        self.points_dock.setObjectName("PointsDock")
        self.points_dock.setWidget(container)

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            self.points_dock,
        )

        self.points_dock.setMinimumWidth(350)

        self.resizeDocks(
            [self.points_dock],
            [350],
            Qt.Horizontal,
        )

        # ==========================================================
        # Delete shortcut
        # ==========================================================

        shortcut = QShortcut(
            QKeySequence.Delete,
            self.point_table,
        )

        shortcut.activated.connect(
            self.on_remove_selected_points
        )

        # ==========================================================
        # Initial refresh
        # ==========================================================

        self.refresh_point_table()
        self.refresh_system_table()


    def refresh_point_table(self):

        from MicroGPS.state import state

        points = state.points
        transforms = state.transforms

        # ------------------------------------------------------------
        # Coordinate systems to display
        # ------------------------------------------------------------

        system_names = list(transforms.keys())

        # ------------------------------------------------------------
        # Table structure
        # ------------------------------------------------------------

        headers = [
            "Label",
            "Type",
            "X (img)",
            "Y (img)",
        ]

        for name in system_names:
            headers.extend([f"{name} X", f"{name} Y"])

        self.point_table.clearContents()
        self.point_table.setRowCount(len(points))
        self.point_table.setColumnCount(len(headers))
        self.point_table.setHorizontalHeaderLabels(headers)

        # ------------------------------------------------------------
        # Fill table
        # ------------------------------------------------------------

        for row, p in enumerate(points):

            self.point_table.setItem(row, 0, QTableWidgetItem(p.label))
            self.point_table.setItem(row, 1, QTableWidgetItem(p.kind))
            self.point_table.setItem(row, 2, QTableWidgetItem(f"{p.image_x:.3f}"))
            self.point_table.setItem(row, 3, QTableWidgetItem(f"{p.image_y:.3f}"))

            col = 4

            for name, transform in transforms.items():

                x, y = image_to_coordinates(
                    p.image_x,
                    p.image_y,
                    name,
                )

                self.point_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(f"{x:.3f}")
                )

                self.point_table.setItem(
                    row,
                    col + 1,
                    QTableWidgetItem(f"{y:.3f}")
                )

                col += 2

        self.point_table.resizeColumnsToContents()


    def refresh_system_table(self):

        from MicroGPS.state import state

        transforms = state.transforms

        self.system_table.clearContents()
        self.system_table.setRowCount(len(transforms))
        self.system_table.setColumnCount(2)
        self.system_table.setHorizontalHeaderLabels(
            ["System", "Affine transform"]
        )

        for row, (name, transform) in enumerate(transforms.items()):

            self.system_table.setItem(
                row,
                0,
                QTableWidgetItem(name)
            )

            m = transform.matrix

            matrix_text = (
                f"[{m[0,0]:.5f} {m[0,1]:.5f} {m[0,2]:.3f}] "
                f"[{m[1,0]:.5f} {m[1,1]:.5f} {m[1,2]:.3f}] "
                f"[{m[2,0]:.0f} {m[2,1]:.0f} {m[2,2]:.0f}]"
            )

            self.system_table.setItem(
                row,
                1,
                QTableWidgetItem(matrix_text)
            )

        self.system_table.resizeColumnsToContents()


    def on_new_coordinate_system(self):

        dialog = TransformDialog(self)

        if dialog.exec():

            self.refresh_point_table()
            self.refresh_system_table()

    def on_clear_measurements(self):

        from MicroGPS.services import clear_points

        clear_points("measurement")

        self.view.refresh_points()
        self.refresh_point_table()
        self.refresh_system_table()

    def on_clear_calibration(self):

        from MicroGPS.services import clear_points

        clear_points("calibration")

        self.view.refresh_points()
        self.refresh_point_table()
        self.refresh_system_table()

    def on_add_point_coordinates(self):

        dialog = AddPointDialog(self)

        if dialog.exec():

            self.view.refresh_points()
            self.refresh_point_table()
            self.refresh_system_table()
    
    def on_remove_selected_points(self):

        from MicroGPS.services import remove_points
        from MicroGPS.state import state

        rows = sorted(
            {
                index.row()
                for index in self.point_table.selectionModel().selectedRows()
            },
            reverse=True,
        )

        if not rows:
            return

        points = [
            state.points[row]
            for row in rows
        ]

        remove_points(points)

        self.view.refresh_points()
        self.refresh_point_table()
        self.refresh_system_table()

    def on_remove_selected_system(self):

        from MicroGPS.services import remove_transform

        rows = self.system_table.selectionModel().selectedRows()

        if not rows:
            return

        row = rows[0].row()

        name = self.system_table.item(row, 0).text()

        remove_transform(name)

        self.refresh_system_table()
        self.refresh_point_table()
