from PySide6.QtWidgets import QApplication
from gui import LpSolverApp

if __name__ == "__main__":
    app = QApplication([])
    window = LpSolverApp()
    window.show()
    app.exec()
