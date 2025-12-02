from PySide6.QtWidgets import QApplication
from gui import LpSolverApp

if __name__ == "__main__":
    app = QApplication([])
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = LpSolverApp()
    window.show()
    app.exec()
