from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from solver import solve_lp
from plotter import plot_2d_feasible_region


class LpSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Programming Solver / Form Mode")
        self.resize(650, 450)

        main_layout = QVBoxLayout()

        # ---------- FORM INPUTS ----------
        form = QFormLayout()
        self.var_input = QLineEdit()
        self.con_input = QLineEdit()
        self.obj_type = QComboBox()
        self.obj_type.addItems(["Maximize", "Minimize"])

        form.addRow("Number of Variables:", self.var_input)
        form.addRow("Number of Constraints:", self.con_input)
        form.addRow("Objective:", self.obj_type)

        main_layout.addLayout(form)

        # ---------- BUTTONS ----------
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate Fields")
        self.solve_btn = QPushButton("Solve")

        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.solve_btn)
        main_layout.addLayout(btn_layout)

        # ---------- TABLES ----------
        self.obj_table = QTableWidget()
        self.con_table = QTableWidget()

        main_layout.addWidget(QLabel("Objective Function"))
        main_layout.addWidget(self.obj_table)
        main_layout.addWidget(QLabel("Constraints"))
        main_layout.addWidget(self.con_table)

        # ---------- OUTPUT ----------
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-weight: bold; padding: 10px;")
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        # ---------- SIGNALS ----------
        self.generate_btn.clicked.connect(self.generate_fields)
        self.solve_btn.clicked.connect(self.solve_lp_from_tables)

    # ----------------------------------------------------------------------------------------
    def generate_fields(self):
        """Generate tables when user enters variable/constraint numbers."""
        try:
            n_vars = int(self.var_input.text())
            n_cons = int(self.con_input.text())
        except ValueError:
            self.result_label.setText("Please enter valid numbers.")
            return

        # Objective table
        self.obj_table.setRowCount(1)
        self.obj_table.setColumnCount(n_vars)
        self.obj_table.setHorizontalHeaderLabels([f"x{i+1}" for i in range(n_vars)])
        self.obj_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Constraint table
        self.con_table.setRowCount(n_cons)
        self.con_table.setColumnCount(n_vars + 1)
        headers = [f"x{i+1}" for i in range(n_vars)] + ["≤ b"]
        self.con_table.setHorizontalHeaderLabels(headers)
        self.con_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # ----------------------------------------------------------------------------------------
    def solve_lp_from_tables(self):
        """Read tables, call solver, and display results."""
        try:
            # Read objective function
            objective = {}
            for col in range(self.obj_table.columnCount()):
                item = self.obj_table.item(0, col)
                val = float(item.text()) if item and item.text() != "" else 0
                objective[f"x{col+1}"] = val

            # Read constraints
            constraints = []
            for row in range(self.con_table.rowCount()):
                coeffs = {}
                for col in range(self.con_table.columnCount() - 1):
                    item = self.con_table.item(row, col)
                    val = float(item.text()) if item and item.text() != "" else 0
                    coeffs[f"x{col+1}"] = val
                rhs_item = self.con_table.item(row, self.con_table.columnCount() - 1)
                rhs = float(rhs_item.text()) if rhs_item and rhs_item.text() != "" else 0
                constraints.append({
                    "name": f"c{row+1}",
                    "coefficients": coeffs,
                    "ineq": "<=",
                    "rhs": rhs
                })

            # Solve LP
            results, variables = solve_lp(objective, constraints)

            # Display results
            output_text = "\n".join(f"{k} = {v}" for k, v in results.items())
            self.result_label.setText(output_text)

            # Plot if exactly 2 variables
            if len(variables) == 2:
                plot_2d_feasible_region(constraints, variables)

        except Exception as e:
            self.result_label.setText(f"Error: {e}")
