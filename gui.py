from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
import ast
from solver import solve_lp
from plotter import plot_2d_feasible_region

class LpSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LP Solver with Graph (Dynamic Input)")
        layout = QVBoxLayout()

        # Objective input
        self.obj_input = QTextEdit()
        self.obj_input.setPlaceholderText("Enter objective as a dictionary, e.g.\n{'x': 3, 'y': 2}")
        layout.addWidget(QLabel("Objective Function:"))
        layout.addWidget(self.obj_input)

        # Constraints input
        self.constraints_input = QTextEdit()
        self.constraints_input.setPlaceholderText(
            "Enter constraints as a list of dicts, e.g.\n"
            "[{'name': 'c1', 'coefficients': {'x': 1, 'y': 1}, 'ineq': '<=', 'rhs': 5}]"
        )
        layout.addWidget(QLabel("Constraints:"))
        layout.addWidget(self.constraints_input)

        # Solve button
        self.solve_button = QPushButton("Solve LP")
        self.solve_button.clicked.connect(self.solve_lp)
        layout.addWidget(self.solve_button)

        # Results output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.output)

        self.setLayout(layout)

    def solve_lp(self):
        try:
            # Parse inputs safely
            objective = ast.literal_eval(self.obj_input.toPlainText())
            constraints = ast.literal_eval(self.constraints_input.toPlainText())

            # Solve LP
            results, variables = solve_lp(objective, constraints)

            # Display results
            output_text = "\n".join(f"{k} = {v}" for k, v in results.items())
            self.output.setText(output_text)

            # Plot if exactly 2 variables
            if len(variables) == 2:
                plot_2d_feasible_region(constraints, variables)
            else:
                QMessageBox.information(self, "Notice", "Graph plotting only works for 2-variable problems.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input:\n{e}")
