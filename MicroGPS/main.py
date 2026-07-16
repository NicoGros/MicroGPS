"""
MicroGPS

Application entry point.
"""

import sys

from PySide6.QtWidgets import QApplication

from MicroGPS.gui.main_window import MainWindow


def main():

    app = QApplication.instance()

    owns_app = False

    if app is None:
        app = QApplication(sys.argv)
        owns_app = True

    app.setApplicationName("MicroGPS")
    app.setApplicationVersion("3.0")
    app.setOrganizationName("MicroGPS")

    window = MainWindow()
    window.show()

    if owns_app:
        return app.exec()

    return window

if __name__ == "__main__":
    sys.exit(main())