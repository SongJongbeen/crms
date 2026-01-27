from PyQt6.QtWidgets import QApplication
import sys

from qt_material import apply_stylesheet

from carenote.database import init_database
from carenote.gui import MainWindow, apply_basic_style

if __name__ == "__main__":
    init_database()

    app = QApplication(sys.argv)
    apply_basic_style(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
