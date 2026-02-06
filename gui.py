from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QFrame, QScrollArea, QCheckBox, QRadioButton, QButtonGroup, QSpinBox
)
from PySide6.QtCore import Qt
from solver import solve_lp
from plotter import plot_2d_feasible_region

class LpSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linear Programming Solver")
        self.resize(900, 600)
        # Dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial;
                font-size: 13px;
            }
            QFrame#leftPanel, QFrame#rightPanel {
                background-color: #2d2d2d;
                border-radius: 8px;
                padding: 20px;
            }
            QFrame#section {
                background-color: #252525;
                border-radius: 6px;
                padding: 12px;
                margin: 5px 0;
            }
            QLineEdit {
                background-color: #3a3a3a;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 6px;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #006cbd;
            }
            QPushButton#secondaryBtn {
                background-color: #3a3a3a;
            }
            QPushButton#secondaryBtn:hover {
                background-color: #4a4a4a;
            }
            QComboBox, QSpinBox {
                background-color: #3a3a3a;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 6px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #4a4a4a;
                border: none;
                width: 16px;
            }
            QLabel#sectionHeader {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 8px;
            }
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #0078d4;
            }
            QLabel#resultHeader {
                font-size: 16px;
                font-weight: bold;
                color: #4caf50;
            }
            QLabel#resultValue {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                padding: 8px 0;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Title
        title = QLabel("LINEAR PROGRAMMING SOLVER")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Two-column layout
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(15)
        main_layout.addLayout(columns_layout)

        # Left panel
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(12)
        columns_layout.addWidget(left_panel, stretch=3)

        # Setup section
        setup_section = QFrame()
        setup_section.setObjectName("section")
        setup_layout = QVBoxLayout(setup_section)
        
        setup_header = QLabel("SETUP")
        setup_header.setObjectName("sectionHeader")
        setup_layout.addWidget(setup_header)

        # Problem type
        problem_type_layout = QHBoxLayout()
        self.objective_group = QButtonGroup()
        self.min_radio = QRadioButton("Minimize")
        self.max_radio = QRadioButton("Maximize")
        self.min_radio.setChecked(True)
        self.objective_group.addButton(self.min_radio)
        self.objective_group.addButton(self.max_radio)
        problem_type_layout.addWidget(self.min_radio)
        problem_type_layout.addWidget(self.max_radio)
        problem_type_layout.addStretch()
        setup_layout.addLayout(problem_type_layout)

        # Variables and constraints
        vc_layout = QHBoxLayout()
        vc_layout.addWidget(QLabel("Variables:"))
        self.var_spinbox = QSpinBox()
        self.var_spinbox.setRange(2, 10)
        self.var_spinbox.setValue(2)
        self.var_spinbox.setFixedWidth(70)
        vc_layout.addWidget(self.var_spinbox)
        
        vc_layout.addSpacing(15)
        
        vc_layout.addWidget(QLabel("Constraints:"))
        self.constr_spinbox = QSpinBox()
        self.constr_spinbox.setRange(1, 10)
        self.constr_spinbox.setValue(2)
        self.constr_spinbox.setFixedWidth(70)
        vc_layout.addWidget(self.constr_spinbox)
        vc_layout.addStretch()
        setup_layout.addLayout(vc_layout)
        
        left_layout.addWidget(setup_section)

        # Objective section
        obj_section = QFrame()
        obj_section.setObjectName("section")
        obj_layout = QVBoxLayout(obj_section)
        
        obj_header = QLabel("OBJECTIVE")
        obj_header.setObjectName("sectionHeader")
        obj_layout.addWidget(obj_header)

        self.obj_layout = QHBoxLayout()
        obj_layout.addLayout(self.obj_layout)
        
        left_layout.addWidget(obj_section)

        # Constrains section
        constr_section = QFrame()
        constr_section.setObjectName("section")
        constr_layout = QVBoxLayout(constr_section)
        
        constr_header = QLabel("CONSTRAINTS")
        constr_header.setObjectName("sectionHeader")
        constr_layout.addWidget(constr_header)

        # Scrollable constraints area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        self.constr_grid_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        constr_layout.addWidget(scroll)

        # Non-negativity
        self.non_neg_check = QCheckBox("All variables ≥ 0")
        self.non_neg_check.setChecked(True)
        constr_layout.addWidget(self.non_neg_check)
        
        left_layout.addWidget(constr_section)

        # Solve button
        self.solve_btn = QPushButton("SOLVE")
        self.solve_btn.setFixedHeight(45)
        left_layout.addWidget(self.solve_btn)

        # Right panel
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(15)
        columns_layout.addWidget(right_panel, stretch=2)

        # Results section
        result_header_label = QLabel("RESULTS")
        result_header_label.setObjectName("sectionHeader")
        right_layout.addWidget(result_header_label)

        self.status_label = QLabel("Press SOLVE to see results")
        self.status_label.setObjectName("resultHeader")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #888;")
        right_layout.addWidget(self.status_label)

        # Optimal value
        self.optimal_label = QLabel("")
        self.optimal_label.setObjectName("resultValue")
        self.optimal_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.optimal_label)

        # Variable values
        var_values_label = QLabel("Variable Values:")
        var_values_label.setStyleSheet("font-size: 13px; color: #bbb; margin-top: 10px;")
        right_layout.addWidget(var_values_label)

        self.variables_label = QLabel("")
        self.variables_label.setStyleSheet("font-size: 14px; padding: 10px;")
        self.variables_label.setWordWrap(True)
        right_layout.addWidget(self.variables_label)

        right_layout.addStretch()

        # Action buttons
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)

        self.view_graph_btn = QPushButton("View Graph")
        self.view_graph_btn.setObjectName("secondaryBtn")
        self.view_graph_btn.setEnabled(False)
        btn_layout.addWidget(self.view_graph_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setObjectName("secondaryBtn")
        btn_layout.addWidget(self.clear_btn)

        right_layout.addLayout(btn_layout)

        # Signals
        self.var_spinbox.valueChanged.connect(self.rebuild_ui)
        self.constr_spinbox.valueChanged.connect(self.rebuild_ui)
        self.solve_btn.clicked.connect(self.solve_lp)
        self.clear_btn.clicked.connect(self.clear_all)
        self.view_graph_btn.clicked.connect(self.view_graph)

        # Initialize
        self.last_constraints = None
        self.last_variables = None
        self.rebuild_ui()

    def rebuild_ui(self):
        """Rebuild objective and constraints when counts change"""
        self.rebuild_objective()
        self.rebuild_constraints()

    def rebuild_objective(self):
        # Clear existing
        while self.obj_layout.count():
            item = self.obj_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        num_vars = self.var_spinbox.value()
        self.obj_inputs = []

        self.obj_layout.addWidget(QLabel("Z ="))
        
        for i in range(num_vars):
            line = QLineEdit()
            line.setFixedWidth(50)
            line.setPlaceholderText("0")
            self.obj_inputs.append(line)
            self.obj_layout.addWidget(line)
            
            var_label = QLabel(f"X{i+1}")
            self.obj_layout.addWidget(var_label)
            
            if i < num_vars - 1:
                plus_label = QLabel("+")
                self.obj_layout.addWidget(plus_label)
        
        self.obj_layout.addStretch()

    def rebuild_constraints(self):
        # Clear existing
        while self.constr_grid_layout.count():
            item = self.constr_grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        num_constraints = self.constr_spinbox.value()
        num_vars = self.var_spinbox.value()
        
        self.constraint_rows = []

        # Constraint rows
        for c in range(num_constraints):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)
            
            c_label = QLabel(f"C{c+1}:")
            c_label.setFixedWidth(30)
            row_layout.addWidget(c_label)
            
            inputs = []
            for v in range(num_vars):
                line = QLineEdit()
                line.setFixedWidth(45)
                line.setPlaceholderText("0")
                inputs.append(line)
                row_layout.addWidget(line)
                
                var_label = QLabel(f"X{v+1}")
                var_label.setFixedWidth(25)
                row_layout.addWidget(var_label)
                
                if v < num_vars - 1:
                    plus_label = QLabel("+")
                    plus_label.setFixedWidth(15)
                    row_layout.addWidget(plus_label)
            
            type_combo = QComboBox()
            type_combo.addItems(["≤", "≥", "="])
            type_combo.setFixedWidth(55)
            row_layout.addWidget(type_combo)
            
            rhs = QLineEdit()
            rhs.setFixedWidth(50)
            rhs.setPlaceholderText("0")
            row_layout.addWidget(rhs)
            
            row_layout.addStretch()
            
            self.constraint_rows.append((inputs, type_combo, rhs))
            self.constr_grid_layout.addLayout(row_layout)

    def clear_layout(self, layout):
        """Helper to recursively clear a layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_all(self):
        for line in self.obj_inputs:
            line.clear()
        
        for inputs, type_combo, rhs in self.constraint_rows:
            for line in inputs:
                line.clear()
            rhs.clear()
            type_combo.setCurrentIndex(0)
        
        self.status_label.setText("Press SOLVE to see results")
        self.status_label.setStyleSheet("font-size: 14px; color: #888;")
        self.optimal_label.setText("")
        self.variables_label.setText("")
        self.view_graph_btn.setEnabled(False)

    def solve_lp(self):
        try:
            # Get objective
            objective = {}
            for i, line in enumerate(self.obj_inputs):
                val = line.text().strip()
                objective[f"X{i+1}"] = float(val) if val else 0.0

            # Get constraints
            constraints = []
            for idx, (inputs, type_combo, rhs) in enumerate(self.constraint_rows):
                coeffs = {}
                for i, line in enumerate(inputs):
                    val = line.text().strip()
                    coeffs[f"X{i+1}"] = float(val) if val else 0.0
                
                rhs_val = rhs.text().strip()
                constraints.append({
                    "name": f"C{idx+1}",
                    "coefficients": coeffs,
                    "ineq": type_combo.currentText(),
                    "rhs": float(rhs_val) if rhs_val else 0.0
                })

            # Determine if minimizing or maximizing
            is_minimize = self.min_radio.isChecked()

            # Solve
            results, variables = solve_lp(objective, constraints, minimize=is_minimize)
            
            # Store for graph
            self.last_constraints = constraints
            self.last_variables = variables
            
            # Display results
            self.status_label.setText("✓ Optimal Solution Found")
            self.status_label.setStyleSheet("font-size: 14px; color: #4caf50;")
            
            # Optimal value
            z_value = results.get("Z", "N/A")
            self.optimal_label.setText(f"Z = {z_value}")
            
            # Variable values
            var_lines = []
            for k, v in results.items():
                if k != "Z":
                    var_lines.append(f"{k} = {v}")
            self.variables_label.setText("\n".join(var_lines))
            
            # Enable graph button if 2D
            if len(variables) == 2:
                self.view_graph_btn.setEnabled(True)
                
        except Exception as e:
            self.status_label.setText("✗ Error")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            self.optimal_label.setText("")
            self.variables_label.setText(str(e))
            self.view_graph_btn.setEnabled(False)

    def view_graph(self):
        if self.last_constraints and self.last_variables and len(self.last_variables) == 2:
            plot_2d_feasible_region(self.last_constraints, self.last_variables)


if __name__ == "__main__":
    app = QApplication([])
    window = LpSolverApp()
    window.show()
    app.exec()