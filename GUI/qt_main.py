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
        QDoubleSpinBox, QTabWidget
    )
    from PyQt5.QtCore import Qt
except Exception as e:
    print("PyQt5 is required to run the GUI. Install it with: pip install PyQt5")
    print("Import error:", e)
    sys.exit(1)

from assignment import Assignment
from category import Category
from class_profile import ClassProfile
# Import data manager for save/load functions
from data_manger import save_class_data, load_class_data


class GradeCalculatorWindow(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Calculator - Sprint 2/3")
        self.resize(1000, 650)

        self.profile = None  # The currently active ClassProfile instance
        self.all_profiles = [] # List to hold all class profiles (Req ID 7/8)

        self._build_ui()
        self.load_data_on_startup() # Load data when the app starts

    def load_data_on_startup(self):
        """Loads data, updates the profile list selector, and sets the active profile."""
        self.all_profiles = load_class_data()
        self._sync_profile_selector()
        
        if self.all_profiles:
            # Set the first loaded profile as active
            self.set_active_profile(self.all_profiles[0])
            QMessageBox.information(self, "Data Loaded", 
                                    f"Loaded {len(self.all_profiles)} class(es). Select a class to view.")
        else:
            QMessageBox.information(self, "Welcome", "No saved data found. Create a new class to begin.")

    def _build_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()

        # Top Control Bar (Class Selector, Creation, Delete, Save)
        top_bar = QHBoxLayout()
        
        # Left Group: Class Selection and Deletion (NEW)
        profile_group = QGroupBox("Class Management")
        profile_layout = QVBoxLayout()
        
        # Existing Class Creator
        create_layout = QHBoxLayout()
        self.class_name_edit = QLineEdit()
        self.class_name_edit.setPlaceholderText("New course name")
        self.create_class_btn = QPushButton("Create New")
        self.create_class_btn.clicked.connect(self.create_class)
        create_layout.addWidget(self.class_name_edit)
        create_layout.addWidget(self.create_class_btn)
        profile_layout.addLayout(create_layout)

        # Class Selector & Delete Button (NEW)
        selector_delete_layout = QHBoxLayout()
        self.profile_selector = QComboBox()
        self.profile_selector.currentIndexChanged.connect(self.switch_profile) # NEW connection
        self.delete_class_btn = QPushButton("Delete Selected") # NEW delete button
        self.delete_class_btn.clicked.connect(self.delete_active_profile)
        
        selector_delete_layout.addWidget(QLabel("Active Class:"))
        selector_delete_layout.addWidget(self.profile_selector)
        selector_delete_layout.addWidget(self.delete_class_btn)
        
        profile_layout.addLayout(selector_delete_layout)
        profile_group.setLayout(profile_layout)
        top_bar.addWidget(profile_group, 3) 

        # Data Persistence Controls (NEW)
        data_box = QGroupBox("Data Persistence")
        data_layout = QVBoxLayout()
        self.save_btn = QPushButton("Save All Data")
        self.save_btn.clicked.connect(self.save_data)
        data_layout.addWidget(self.save_btn)
        data_box.setLayout(data_layout)
        top_bar.addWidget(data_box, 1)
        
        main_layout.addLayout(top_bar)

        # Tab Widget for Assignment/Category vs Analysis
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # --- TAB 1: Grading Data ---
        grading_widget = QWidget()
        grading_layout = QHBoxLayout()
        
        # Left Panel: Category Controls
        cat_panel = QVBoxLayout()
        cat_box = QGroupBox("Category (Weighted)")
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
        cat_panel.addWidget(cat_box)
        cat_panel.addStretch()
        
        # Right Panel: Assignment Controls and Table
        assign_box = QGroupBox("Assignments & Details")
        assign_layout = QVBoxLayout()

        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Category:"))
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

        # Assignment list table
        self.assign_table = QTableWidget(0, 3)
        self.assign_table.setHorizontalHeaderLabels(["Name", "Earned", "Possible"])
        assign_layout.addWidget(self.assign_table)

        assign_box.setLayout(assign_layout)
        
        grading_layout.addLayout(cat_panel, 1)
        grading_layout.addWidget(assign_box, 3)
        self.tabs.addTab(grading_widget, "Grade Entry & Status")
        grading_widget.setLayout(grading_layout)
        
        # --- TAB 2: Predictive Analysis ---
        analysis_widget = QWidget()
        analysis_layout = QVBoxLayout()
        
        # What-If Analysis Group (ID 5)
        what_if_box = QGroupBox("What-If Grade Projection (ID 9)")
        wi_form = QFormLayout()
        self.wi_cat_selector = QComboBox()
        self.wi_score = QDoubleSpinBox()
        self.wi_score.setRange(0.0, 1e6)
        self.wi_possible = QDoubleSpinBox()
        self.wi_possible.setRange(0.0, 1e6)
        self.calculate_wi_btn = QPushButton("Calculate Projected Grade")
        self.calculate_wi_btn.clicked.connect(self.calculate_what_if)
        self.wi_result_label = QLabel("Projected Grade: N/A")
        
        wi_form.addRow("Target Category:", self.wi_cat_selector)
        wi_form.addRow("Hypothetical Score Earned:", self.wi_score)
        wi_form.addRow("Hypothetical Points Possible:", self.wi_possible)
        wi_form.addRow(self.calculate_wi_btn)
        wi_form.addRow(self.wi_result_label)
        what_if_box.setLayout(wi_form)
        
        # Score Needed Analysis Group (ID 10)
        needed_box = QGroupBox("Score Needed to Achieve Target (ID 10)")
        needed_form = QFormLayout()
        self.needed_cat_selector = QComboBox()
        self.needed_target = QDoubleSpinBox()
        self.needed_target.setRange(0.0, 100.0)
        self.needed_target.setSuffix(" %")
        self.needed_possible = QDoubleSpinBox()
        self.needed_possible.setRange(0.0, 1e6)
        self.calculate_needed_btn = QPushButton("Calculate Required Score")
        self.calculate_needed_btn.clicked.connect(self.calculate_score_needed_ui)
        self.needed_result_label = QLabel("Points Needed: N/A")
        
        needed_form.addRow("Remaining Assignment Category:", self.needed_cat_selector)
        needed_form.addRow("Target Final Grade:", self.needed_target)
        needed_form.addRow("Points Possible for Remaining Assignment:", self.needed_possible)
        needed_form.addRow(self.calculate_needed_btn)
        needed_form.addRow(self.needed_result_label)
        needed_box.setLayout(needed_form)
        
        analysis_layout.addWidget(what_if_box)
        analysis_layout.addWidget(needed_box)
        analysis_layout.addStretch()
        analysis_widget.setLayout(analysis_layout)
        
        self.tabs.addTab(analysis_widget, "Predictive Analysis")

        # Grade display (Final output bar)
        grade_layout = QHBoxLayout()
        self.grade_label = QLabel("Current Grade: N/A")
        self.grade_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        grade_layout.addStretch()
        grade_layout.addWidget(self.grade_label)
        
        main_layout.addLayout(grade_layout)

        central.setLayout(main_layout)
        self.setCentralWidget(central)
    
    def set_active_profile(self, profile):
        """Sets the current active profile and refreshes the GUI elements."""
        self.profile = profile
        self.class_name_edit.setText(profile.name)
        self._sync_category_selector()
        self.refresh_assignment_table()
        self.update_grade()
        
    def switch_profile(self, index):
        """Handles switching the active class profile via the QComboBox."""
        if index < 0 or index >= len(self.all_profiles):
            self.profile = None
            self.class_name_edit.clear()
            self._sync_category_selector()
            self.refresh_assignment_table()
            self.update_grade()
            return
            
        new_profile = self.all_profiles[index]
        self.set_active_profile(new_profile)

    def _sync_profile_selector(self):
        """Updates the top-level QComboBox with all saved class names."""
        self.profile_selector.blockSignals(True)
        self.profile_selector.clear()
        
        names = [p.name for p in self.all_profiles]
        self.profile_selector.addItems(names)
        
        # Set the selector to the current active profile
        if self.profile:
            try:
                index = names.index(self.profile.name)
                self.profile_selector.setCurrentIndex(index)
            except ValueError:
                self.profile_selector.setCurrentIndex(-1)
                
        self.profile_selector.blockSignals(False)


    def _sync_category_selector(self):
        """Helper to update all category selectors."""
        self.cat_selector.blockSignals(True)
        self.wi_cat_selector.blockSignals(True)
        self.needed_cat_selector.blockSignals(True)
        
        for selector in [self.cat_selector, self.wi_cat_selector, self.needed_cat_selector]:
            selector.clear()
        
        if self.profile:
            cat_names = sorted(self.profile.categories.keys())
            for selector in [self.cat_selector, self.wi_cat_selector, self.needed_cat_selector]:
                selector.addItems(cat_names)
        
        self.cat_selector.blockSignals(False)
        self.wi_cat_selector.blockSignals(False)
        self.needed_cat_selector.blockSignals(False)


    def create_class(self):
        name = self.class_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input required", "Please enter a class name.")
            return
        
        # Create new profile and make it the active one
        new_profile = ClassProfile(name)
        self.all_profiles.append(new_profile)
        self.set_active_profile(new_profile)
        self._sync_profile_selector()
        
        QMessageBox.information(self, "Class created", f"Created new active class '{name}'.")

    def delete_active_profile(self):
        """Deletes the currently active profile (NEW)."""
        if not self.profile:
            QMessageBox.warning(self, "Error", "No class is currently active to delete.")
            return

        reply = QMessageBox.question(self, 'Confirm Delete',
            f"Are you sure you want to delete the class '{self.profile.name}'? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.all_profiles.remove(self.profile)
            self.profile = None
            
            # Set a new active profile or clear the GUI
            if self.all_profiles:
                self.set_active_profile(self.all_profiles[0])
            else:
                self.switch_profile(-1) # Clears the interface
                
            self._sync_profile_selector()
            self.save_data(silent=True) # Automatically save the deletion
            QMessageBox.information(self, "Deleted", "Class successfully deleted and data saved.")


    def save_data(self, silent=False):
        """Saves all profiles using the data manager (Req ID 7)."""
        if not self.all_profiles:
            if not silent:
                 QMessageBox.warning(self, "No Data", "No classes to save.")
            return
        
        # Note: data_manger prints confirmation to the console
        save_class_data(self.all_profiles)
        if not silent:
            QMessageBox.information(self, "Success", "Data saved to local file!")

    def add_category(self):
        if not self.profile:
            QMessageBox.warning(self, "No class", "Create a class first.")
            return
        name = self.cat_name_edit.text().strip()
        weight = float(self.cat_weight_spin.value())
        if not name:
            QMessageBox.warning(self, "Input required", "Please enter a category name.")
            return
        
        # Simple check for 100% total weight (Req ID 3/8)
        current_weight = self.profile.get_total_declared_weight()
        if current_weight + weight > 100.001 and len(self.profile.categories) > 0:
             QMessageBox.critical(self, "Weight Error", 
                                  f"Total weight will exceed 100%. Current total is {current_weight}%.")
             return

        try:
            cat = Category(name, weight)
            self.profile.add_category(cat)
            self._sync_category_selector()
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
        if possible == 0:
            QMessageBox.critical(self, "Input Error", "Points possible cannot be zero.")
            return

        try:
            # Assignment validation handles negative scores and earned > possible (Req ID 7)
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
            self.assign_table.setItem(row, 1, QTableWidgetItem(f"{a.points_earned:.2f}"))
            self.assign_table.setItem(row, 2, QTableWidgetItem(f"{a.points_possible:.2f}"))

    def update_grade(self):
        if not self.profile:
            self.grade_label.setText("Current Grade: N/A")
            return
        try:
            percent = self.profile.calculate_current_grade()
            letter = self.profile.get_letter_grade(percent)
            self.grade_label.setText(f"Current Grade: {percent:.2f} % ({letter})")
        except Exception as e:
            self.grade_label.setText(f"Current Grade: Error ({e})")
            
    # --- PREDICTIVE METHODS ---
    
    def calculate_what_if(self):
        """Calculates and displays the projected grade (Req ID 9)."""
        if not self.profile:
            QMessageBox.warning(self, "Error", "Please select a class first.")
            return

        cat_name = self.wi_cat_selector.currentText()
        if not cat_name:
             QMessageBox.warning(self, "Error", "Please select a category.")
             return
             
        earned = float(self.wi_score.value())
        possible = float(self.wi_possible.value())
        
        if possible == 0:
            self.wi_result_label.setText("Projected Grade: Error - Points possible must be > 0.")
            return

        try:
            projected = self.profile.calculate_what_if_grade(cat_name, earned, possible)
            letter = self.profile.get_letter_grade(projected)
            self.wi_result_label.setText(f"Projected Grade: {projected:.2f} % ({letter})")
        except Exception as e:
            self.wi_result_label.setText(f"Projected Grade: Calculation Error ({e})")
            
    def calculate_score_needed_ui(self):
        """Calculates and displays the score needed on a remaining assignment (Req ID 10)."""
        if not self.profile:
            QMessageBox.warning(self, "Error", "Please select a class first.")
            return

        cat_name = self.needed_cat_selector.currentText()
        if not cat_name:
             QMessageBox.warning(self, "Error", "Please select a category.")
             return
             
        target_percent = float(self.needed_target.value())
        possible_points = float(self.needed_possible.value())
        
        if possible_points == 0:
            self.needed_result_label.setText("Points Needed: Error - Points possible must be > 0.")
            return

        try:
            points_needed = self.profile.calculate_score_needed(cat_name, possible_points, target_percent)
            
            if points_needed == -1.0:
                result_text = f"Target {target_percent:.2f}% Impossible! (Need > {possible_points:.2f} points)"
            else:
                result_text = f"Points Needed: {points_needed:.2f} / {possible_points:.2f}"
                
            self.needed_result_label.setText(result_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An error occurred during calculation: {str(e)}")
            self.needed_result_label.setText("Points Needed: Calculation Error")


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