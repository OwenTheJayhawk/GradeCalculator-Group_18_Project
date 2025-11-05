import os
import sys

# Ensure project root is on path so we can import modules next to this GUI folder
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget,
        QTableWidgetItem, QMessageBox, QGroupBox, QFormLayout, QSpinBox,
        QDoubleSpinBox, QScrollArea
    )
    from PyQt5.QtCore import Qt
except Exception as e:
    # Fail fast with a helpful message instead of leaving Qt names undefined.
    print("PyQt5 is required to run the GUI. Install it with: pip install PyQt5")
    print("Import error:", e)
    # Exit so importing this module doesn't leave undefined symbols (which
    # previously caused a NameError when the class definition executed).
    sys.exit(1)

from assignment import Assignment
from category import Category
from class_profile import ClassProfile


class GradeCalculatorWindow(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Calculator - PyQt5")
        self.resize(800, 480)

        self.profile = None  # ClassProfile instance

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()

        # Class controls
        class_box = QGroupBox("Course")
        class_layout = QHBoxLayout()
        self.class_name_edit = QLineEdit()
        self.class_name_edit.setPlaceholderText("Enter course name")
        self.create_class_btn = QPushButton("Create Class")
        self.create_class_btn.clicked.connect(self.create_class)
        class_layout.addWidget(QLabel("Class:"))
        class_layout.addWidget(self.class_name_edit)
        class_layout.addWidget(self.create_class_btn)
        class_box.setLayout(class_layout)

        # Category controls
        cat_box = QGroupBox("Category (weighted)")
        cat_form = QFormLayout()
        self.cat_name_edit = QLineEdit()
        self.cat_weight_spin = QDoubleSpinBox()
        self.cat_weight_spin.setRange(0.0, 100.0)
        self.cat_weight_spin.setSuffix(" %")
        self.add_cat_btn = QPushButton("Add Category")
        self.add_cat_btn.clicked.connect(self.add_category)
        cat_form.addRow("Name:", self.cat_name_edit)
        cat_form.addRow("Weight:", self.cat_weight_spin)
        cat_form.addRow(self.add_cat_btn)
        cat_box.setLayout(cat_form)

        # Category selector and assignments
        assign_box = QGroupBox("Assignments")
        assign_layout = QVBoxLayout()

        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Category:"))
        self.cat_selector = QComboBox()
        self.cat_selector.currentIndexChanged.connect(self.on_category_changed)
        selector_layout.addWidget(self.cat_selector)
        assign_layout.addLayout(selector_layout)

        # Assignment form
        aform = QFormLayout()
        self.a_name = QLineEdit()
        self.a_earned = QDoubleSpinBox()
        self.a_earned.setRange(0.0, 1e6)
        self.a_possible = QDoubleSpinBox()
        self.a_possible.setRange(0.0, 1e6)
        self.add_assignment_btn = QPushButton("Add Assignment to Category")
        self.add_assignment_btn.clicked.connect(self.add_assignment)
        aform.addRow("Name:", self.a_name)
        aform.addRow("Points earned:", self.a_earned)
        aform.addRow("Points possible:", self.a_possible)
        aform.addRow(self.add_assignment_btn)

        assign_layout.addLayout(aform)

        # Grade thresholds controls
        thr_box = QGroupBox("Grade Thresholds")
        thr_form = QFormLayout()
        self.thr_A = QDoubleSpinBox()
        self.thr_A.setRange(0.0, 100.0)
        self.thr_A.setSuffix(" %")
        self.thr_B = QDoubleSpinBox()
        self.thr_B.setRange(0.0, 100.0)
        self.thr_B.setSuffix(" %")
        self.thr_C = QDoubleSpinBox()
        self.thr_C.setRange(0.0, 100.0)
        self.thr_C.setSuffix(" %")
        self.thr_D = QDoubleSpinBox()
        self.thr_D.setRange(0.0, 100.0)
        self.thr_D.setSuffix(" %")
        self.thr_F = QDoubleSpinBox()
        self.thr_F.setRange(0.0, 100.0)
        self.thr_F.setSuffix(" %")
        self.apply_thr_btn = QPushButton("Apply Thresholds")
        self.apply_thr_btn.clicked.connect(self.apply_thresholds)
        self.reset_thr_btn = QPushButton("Reset to Defaults")
        self.reset_thr_btn.clicked.connect(self.reset_thresholds)

        thr_form.addRow("A:", self.thr_A)
        thr_form.addRow("B:", self.thr_B)
        thr_form.addRow("C:", self.thr_C)
        thr_form.addRow("D:", self.thr_D)
        thr_form.addRow("F:", self.thr_F)
        thr_form.addRow(self.apply_thr_btn)
        thr_form.addRow(self.reset_thr_btn)
        thr_box.setLayout(thr_form)

        # Assignment list table
        self.assign_table = QTableWidget(0, 3)
        self.assign_table.setHorizontalHeaderLabels(["Name", "Earned", "Possible"])
        assign_layout.addWidget(self.assign_table)

        assign_box.setLayout(assign_layout)

        # Grade display (create before adding to main layout)
        grade_layout = QHBoxLayout()
        self.grade_label = QLabel("Current grade: N/A")
        grade_layout.addStretch()
        grade_layout.addWidget(self.grade_label)

        main_layout.addWidget(class_box)
        main_layout.addWidget(cat_box)
        main_layout.addWidget(assign_box)
        main_layout.addWidget(thr_box)
        main_layout.addLayout(grade_layout)

        central.setLayout(main_layout)
        # Wrap the central widget in a scroll area so a vertical scrollbar appears when needed
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(central)
        self.setCentralWidget(scroll)

        # initialize threshold widgets with defaults (no profile yet)
        self.reset_thresholds()

    def create_class(self):
        name = self.class_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input required", "Please enter a class name.")
            return
        self.profile = ClassProfile(name)
        self.cat_selector.clear()
        self.assign_table.setRowCount(0)
        # populate threshold widgets from the new profile
        self.refresh_threshold_widgets()
        self.update_grade()
        QMessageBox.information(self, "Class created", f"Created class '{name}'.")

    def add_category(self):
        if not self.profile:
            QMessageBox.warning(self, "No class", "Create a class first.")
            return
        name = self.cat_name_edit.text().strip()
        weight = float(self.cat_weight_spin.value())
        if not name:
            QMessageBox.warning(self, "Input required", "Please enter a category name.")
            return
        try:
            cat = Category(name, weight)
            self.profile.add_category(cat)
            self.cat_selector.addItem(cat.name)
            self.cat_name_edit.clear()
            self.cat_weight_spin.setValue(0.0)
            self.update_grade()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_category_changed(self, index):
        self.refresh_assignment_table()

    def add_assignment(self):
        if not self.profile:
            QMessageBox.warning(self, "No class", "Create a class first.")
            return
        cat_name = self.cat_selector.currentText()
        if not cat_name:
            QMessageBox.warning(self, "No category", "Add or select a category first.")
            return
        name = self.a_name.text().strip()
        earned = float(self.a_earned.value())
        possible = float(self.a_possible.value())
        if not name:
            QMessageBox.warning(self, "Input required", "Please enter an assignment name.")
            return
        try:
            assignment = Assignment(name, earned, possible)
            cat = self.profile.categories[cat_name]
            cat.add_assignment(assignment)
            self.a_name.clear()
            self.a_earned.setValue(0.0)
            self.a_possible.setValue(0.0)
            self.refresh_assignment_table()
            self.update_grade()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def refresh_assignment_table(self):
        self.assign_table.setRowCount(0)
        cat_name = self.cat_selector.currentText()
        if not cat_name or not self.profile:
            return
        cat = self.profile.categories.get(cat_name)
        if not cat:
            return
        for a in cat.assignments:
            row = self.assign_table.rowCount()
            self.assign_table.insertRow(row)
            self.assign_table.setItem(row, 0, QTableWidgetItem(str(a.name)))
            self.assign_table.setItem(row, 1, QTableWidgetItem(str(a.points_earned)))
            self.assign_table.setItem(row, 2, QTableWidgetItem(str(a.points_possible)))

    def update_grade(self):
        if not self.profile:
            self.grade_label.setText("Current grade: N/A")
            return
        try:
            g = self.profile.calculate_current_grade()
            letter = self.profile.get_letter_grade(g)
            self.grade_label.setText(f"Current grade: {g} % ({letter})")
        except Exception as e:
            self.grade_label.setText("Current grade: Error")

    # Threshold helpers
    def refresh_threshold_widgets(self):
        """Load current profile thresholds into the widgets (or defaults if no profile)."""
        if self.profile:
            thr = self.profile.get_grade_thresholds()
        else:
            # same defaults as ClassProfile
            thr = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0}
        self.thr_A.setValue(thr["A"])
        self.thr_B.setValue(thr["B"])
        self.thr_C.setValue(thr["C"])
        self.thr_D.setValue(thr["D"])
        self.thr_F.setValue(thr["F"])

    def apply_thresholds(self):
        if not self.profile:
            QMessageBox.warning(self, "No class", "Create a class first.")
            return
        thr = {
            "A": float(self.thr_A.value()),
            "B": float(self.thr_B.value()),
            "C": float(self.thr_C.value()),
            "D": float(self.thr_D.value()),
            "F": float(self.thr_F.value()),
        }
        try:
            self.profile.set_grade_thresholds(thr)
            QMessageBox.information(self, "Thresholds updated", "Grade thresholds updated.")
            self.update_grade()
        except Exception as e:
            QMessageBox.critical(self, "Invalid thresholds", str(e))

    def reset_thresholds(self):
        """Reset the spin boxes to default thresholds (does not change profile unless applied)."""
        defaults = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0}
        self.thr_A.setValue(defaults["A"])
        self.thr_B.setValue(defaults["B"])
        self.thr_C.setValue(defaults["C"])
        self.thr_D.setValue(defaults["D"])
        self.thr_F.setValue(defaults["F"])


def run_app():
    # Helpful message if PyQt5 is missing
    try:
        from PyQt5.QtWidgets import QApplication  # re-check
    except Exception:
        print("PyQt5 is not installed. Install it with: pip install PyQt5")
        return

    app = QApplication(sys.argv)
    w = GradeCalculatorWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
