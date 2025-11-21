#import statements
import os
import sys

R = os.path.dirname(os.path.dirname(__file__)) #get parent directory
if R not in sys.path: #add parent directory to path
    sys.path.insert(0, R)
try:
    from PyQt5.QtWidgets import(QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox, QScrollArea, QInputDialog, QListWidget, QFileDialog)
    from PyQt5.QtCore import Qt
except Exception as E:
    print("PyAt5 needed to run")
    print("Error:", E)
    sys.exit(1)
from assignment import Assignment
from category import Category
from class_profile import ClassProfile
from data_manger import(load_data, save_data, ClassOp, deleteClass)

class Grade_Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Calculator")
        self.resize(800, 480)
        self.profile = None
        self.CreateUI()
    def CreateUI(self):
        Middle = QWidget()
        MidLayout = QVBoxLayout()
###############################Class Box################################
        classBox = QGroupBox("Course")
        classLayout = QHBoxLayout()
        self.class_name_edit = QLineEdit()
        self.class_name_edit.setPlaceholderText("Enter Class Name")
        self.create_class_btn = QPushButton("Create Class")
        self.create_class_btn.clicked.connect(self.MakeClass)
        classLayout.addWidget(QLabel("Class:"))
        classLayout.addWidget(self.class_name_edit)
        classLayout.addWidget(self.create_class_btn)
        self.load_data_btn = QPushButton("Load Class Data")
        self.load_data_btn.clicked.connect(self.load_data)
        self.save_data_btn = QPushButton("Save Current Class")
        self.save_data_btn.clicked.connect(self.save_data)
        classLayout.addWidget(self.load_data_btn)
        classLayout.addWidget(self.save_data_btn)
        classBox.setLayout(classLayout)
###########################################################################

##############################Saved Classes Box##############################
        savedClassBox = QGroupBox("Saved Classes")
        savedClassLayout = QVBoxLayout()
        self.savedClasses = QListWidget()
        buttons = QHBoxLayout()
        self.refreshButton = QPushButton("Refresh List")
        self.refreshButton.clicked.connect(self.refreshSavedClasses)
        self.loadSelectedClassButton = QPushButton("Load Selected")
        self.loadSelectedClassButton.clicked.connect(self.loadSelectedClass)
        self.deleteSelectedClassButton = QPushButton("Delete Selected")
        self.deleteSelectedClassButton.clicked.connect(self.deleteSelectedClass)
        self.importButton = QPushButton("Import")
        self.importButton.clicked.connect(self.importClass)
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.exportClass)
        
        buttons.addWidget(self.loadSelectedClassButton) # Use Load Selected instead of general load_data
        buttons.addWidget(self.refreshButton)
        buttons.addWidget(self.deleteSelectedClassButton)
        buttons.addWidget(self.importButton)
        buttons.addWidget(self.exportButton)
        
        savedClassLayout.addWidget(self.savedClasses)
        savedClassLayout.addLayout(buttons)
        savedClassLayout.addWidget(self.save_data_btn )# Add save button here
        
        savedClassBox.setLayout(savedClassLayout)
##################################################################################

#############################Category Box####################################
        categoryBox = QGroupBox("Weighted Categories")
        categoryFormat = QFormLayout()
        self.EditCategoryName = QLineEdit()
        self.moveCategoryWeight = QDoubleSpinBox()
        self.moveCategoryWeight.setRange(0.0, 100.0)
        self.moveCategoryWeight.setSuffix(" %")
        self.AddCategoryButton = QPushButton("Add Category")
        self.AddCategoryButton.clicked.connect(self.newCategory)
        categoryFormat.addRow("Name:", self.EditCategoryName)
        categoryFormat.addRow("Weight:", self.moveCategoryWeight)
        categoryFormat.addRow(self.AddCategoryButton)
        categoryBox.setLayout(categoryFormat)
################################################################################

###########################Assignment Category Selector##########################
        assignmentContainer = QGroupBox("Assignments")
        LayoutOfAssignments = QVBoxLayout()
        select_Buttons = QHBoxLayout()
        select_Buttons.addWidget(QLabel("Category:"))
        self.categorySelector = QComboBox()
        self.categorySelector.currentIndexChanged.connect(self.switchCategory)
        select_Buttons.addWidget(self.categorySelector)
        LayoutOfAssignments.addLayout(select_Buttons)        
#################################################################################

##########################Assignments Box########################################
        AssignmentLayout = QFormLayout()
        self.assignmentName = QLineEdit()
        self.points_Earned = QDoubleSpinBox()
        self.points_Earned.setRange(0.0, 1000000.0)
        self.points_Possible = QDoubleSpinBox()
        self.points_Possible.setRange(0.0, 1000000.0)
        self.NewAssignementBtn = QPushButton("Add Assignment")
        self.NewAssignementBtn.clicked.connect(self.MakeAssignment)
        AssignmentLayout.addRow("Name:", self.assignmentName)
        AssignmentLayout.addRow("Points Earned:", self.points_Earned)
        AssignmentLayout.addRow("Points Possible:", self.points_Possible)
        AssignmentLayout.addRow(self.NewAssignementBtn)
        # FIX: The original code had AssignmentLayout.addLayout(AssignmentLayout) which caused the AttributeError. 
        # Since AssignmentLayout is a QFormLayout, it should only contain rows.
        # The list of assignments needs to be placed into the container below the form fields.
################################################################################

###############################Grade Thresholds Box################################
        Thresholds = QGroupBox("Grade Thresholds")
        ThreshFormat = QFormLayout()
        self.A = QDoubleSpinBox()
        self.A.setRange(0.0, 100.0)
        self.A.setSuffix(" %")
        self.B = QDoubleSpinBox()
        self.B.setRange(0.0, 100.0)
        self.B.setSuffix(" %")
        self.C = QDoubleSpinBox()
        self.C.setRange(0.0, 100.0)
        self.C.setSuffix(" %")
        self.D = QDoubleSpinBox()
        self.D.setRange(0.0, 100.0)
        self.D.setSuffix(" %")
        self.F = QDoubleSpinBox()
        self.F.setRange(0.0, 100.0)
        self.F.setSuffix(" %")
        self.changeThreshB = QPushButton("Apply Thresholds")
        self.changeThreshB.clicked.connect(self.ThreshMod)
        self.Thresh_reset = QPushButton("Reset to Default")
        self.Thresh_reset.clicked.connect(self.ThreshAlph)
        ThreshFormat.addRow("A:", self.A)
        ThreshFormat.addRow("B:", self.B)
        ThreshFormat.addRow("C:", self.C)
        ThreshFormat.addRow("D:", self.D)
        ThreshFormat.addRow("F:", self.F)
        ThreshFormat.addRow(self.changeThreshB)
        ThreshFormat.addRow(self.Thresh_reset)
        Thresholds.setLayout(ThreshFormat)
##################################################################################

##################################Hypothetical Grade Box##################################
        Hypothetical_Box = QGroupBox("Hypothetical Required Score")
        LayoutForHypothetical = QFormLayout()
        self.Hcat = QComboBox()
        self.Hcat.setToolTip("Select category to calculate required score for")
        self.Hpossible = QDoubleSpinBox()
        self.Hpossible.setRange(0.0, 1000000.0)
        self.Hpossible.setValue(100.0)
        self.HletterGrade = QComboBox()
        self.HletterGrade.addItems(["A", "B", "C", "D", "F"])
        self.Hfind = QPushButton("Calculate Required %")
        self.Hfind.clicked.connect(self.CalcNeedToGet)
        self.HresLabel = QLabel("")
        LayoutForHypothetical.addRow("Category:", self.Hcat)
        LayoutForHypothetical.addRow("New assignment possible points:", self.Hpossible)
        LayoutForHypothetical.addRow("Target letter:", self.HletterGrade)
        LayoutForHypothetical.addRow(self.Hfind)
        LayoutForHypothetical.addRow(self.HresLabel)
        Hypothetical_Box.setLayout(LayoutForHypothetical)
#########################################################################################

################################List of Assignments####################################
        self.assignments = QTableWidget(0, 3)
        self.assignments.setHorizontalHeaderLabels(["Name", "Earned", "Possible"])
        
        LayoutOfAssignments.addLayout(AssignmentLayout) # Add the assignment input form
        LayoutOfAssignments.addWidget(self.assignments) # Add the table widget
        assignmentContainer.setLayout(LayoutOfAssignments)
##########################################################################################

################################Show Grade################################################
        gradeShow = QHBoxLayout()
        self.shownGrade = QLabel("Current Grade: N/A")
        self.shownGrade.setStyleSheet("font-size: 16px; font-weight: bold;") # Style for emphasis
        gradeShow.addStretch()
        gradeShow.addWidget(self.shownGrade)
###########################################################################################

################################General####################################################
        MidLayout.addWidget(classBox)
        MidLayout.addWidget(savedClassBox)
        
        # Horizontal layout for Category and Hypothetical boxes
        TopSectionLayout = QHBoxLayout()
        TopSectionLayout.addWidget(categoryBox)
        TopSectionLayout.addWidget(Hypothetical_Box)
        
        MidLayout.addLayout(TopSectionLayout)
        
        MidLayout.addWidget(assignmentContainer)
        
        # Add Thresholds box below the main content, ensure it's scrollable
        MidLayout.addWidget(Thresholds) 
        
        MidLayout.addLayout(gradeShow)
        
        Middle.setLayout(MidLayout)
        UpDownScroll = QScrollArea()
        UpDownScroll.setWidgetResizable(True)
        UpDownScroll.setWidget(Middle)
        self.setCentralWidget(UpDownScroll)
        
        # Initialize default values and load saved data
        self.ThreshAlph()
        self.refreshSavedClasses()
############################################################################################


    def MakeClass(self):
        N = self.class_name_edit.text().strip()
        if not N:
            QMessageBox.warning(self, "Input Error", "Enter a valid class name")
            return
        # Check for duplicate name among saved classes
        if N in self.listnames():
            QMessageBox.critical(self, "Duplicate Error", f"A class named '{N}' already exists.")
            return

        self.profile = ClassProfile(N)
        self.categorySelector.clear()
        self.Hcat.clear() # Clear hypothetical selector too
        self.assignments.setRowCount(0)
        self.ThreshreUP() # Update thresholds to profile defaults (90/80/...)
        self.newGrade() # Update grade display
        self.class_name_edit.clear() # Clear input box
        QMessageBox.information(self, "Class Created", f"Created class '{N}'.")
    
    def refreshSavedClasses(self):
        self.savedClasses.clear()
        try:
            N = self.listnames()
            for _ in N:
                self.savedClasses.addItem(_)
        except Exception as E:
            print(f"Error refreshing class list: {E}")
        self.refreshHypotheticalCats()


    def loadSelectedClass(self):
        i = self.savedClasses.currentItem()
        if not i:
            QMessageBox.warning(self, "Select class", "Please select a class to load.")
            return
        N = i.text()
        clss = load_data()
        select = next((_ for _ in clss if _.class_name == N), None)
        if select:
            self.getProfile(select)
            # QMessageBox.information(self, "Loaded", f"Loaded class '{select.class_name}'.")

    def deleteSelectedClass(self):
        i = self.savedClasses.currentItem()
        if not i:
            QMessageBox.warning(self, "Select class", "Please select a saved class to delete.")
            return
        N = i.text()
        
        # Clear profile if active class is deleted
        if self.profile and self.profile.class_name == N:
            self.profile = None

        check = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete class '{N}'?", QMessageBox.Yes | QMessageBox.No)
        if check == QMessageBox.Yes:
            if deleteClass(N):
                QMessageBox.information(self, "Deleted", f"'{N}' deleted.")
                self.refreshSavedClasses()
                self.newGrade() # Update display after potential deletion
            else:
                QMessageBox.warning(self, "Error", "Selected class could not be found")
                
    def importClass(self):
        P, _ = QFileDialog.getOpenFileName(self, "Import Class Data", "", "JSON Files (*.json);;All Files (*)")
        if not P:
            return
        try:
            clss = load_data(P)
            if not clss:
                QMessageBox.information(self, "No classes", "No classes found in the selected file.")
                return
            for _ in clss:
                ClassOp(_) # Use ClassOp to save and overwrite/add existing classes
            self.refreshSavedClasses()
            QMessageBox.information(self, "Imported", f"Imported {len(clss)} classes.")
        except Exception as E:
            QMessageBox.critical(self, "Error", f"Import failed: {str(E)}")
    
    def exportClass(self):
        i = self.savedClasses.currentItem()
        if not i:
            QMessageBox.warning(self, "Select class", "Please select a saved class to export.")
            return
        N = i.text()
        clss = load_data()
        select = next((_ for _ in clss if _.class_name == N), None)
        if not select:
            QMessageBox.warning(self, "Not Found", "Selected class could not be found")
            return
        P, _ = QFileDialog.getSaveFileName(self, "Export Class Data", f"{N}.json", "JSON Files (*.json);;All Files (*)")
        if not P:
            return
        try:
            save_data([select], P)
            QMessageBox.information(self, "Exported", f"Exported '{N}'")
        except Exception as E:
            QMessageBox.critical(self, "Failed export", str(E))

    def newCategory(self):
        if not self.profile:
            QMessageBox.warning(self, "No Class", "Create a class first.")
            return
        N = self.EditCategoryName.text().strip()
        W = float(self.moveCategoryWeight.value())
        if not N:
            QMessageBox.warning(self, "Input required", "Please enter a category name.")
            return
        
        # Check if total weight exceeds 100%
        current_weight = self.profile.weightSum()
        if current_weight + W > 100.001: 
             QMessageBox.critical(self, "Weight Error", 
                                  f"Total weight will exceed 100%. Current total: {current_weight}%.")
             return
             
        try:
            newCategory = Category(N, W)
            self.profile.AddCategory(newCategory)
            self.categorySelector.addItem(newCategory.cat_name)
            self.Hcat.addItem(newCategory.cat_name) # Add to Hypothetical selector too
            self.EditCategoryName.clear()
            self.moveCategoryWeight.setValue(0.0)
            self.newGrade()
        except Exception as E:
            QMessageBox.critical(self, "Error", str(E))
            

    def switchCategory(self):
        self.refreshAssignments()

    def MakeAssignment(self):
        if not self.profile:
            QMessageBox.warning(self, "No Class", "Create a class first.")
            return
        tempCatName = self.categorySelector.currentText()
        if not tempCatName:
            QMessageBox.warning(self, "No Category", "Add a category first.")
            return
        new_name = self.assignmentName.text().strip()
        earned = float(self.points_Earned.value())
        possible = float(self.points_Possible.value())
        if not new_name:
            QMessageBox.warning(self, "Input Error", "Please enter an assignment name.")
            return
        
        if possible == 0:
            QMessageBox.warning(self, "Input Error", "Points possible must be greater than 0.")
            return

        try:
            # Assignment validation handles negative scores and earned > possible
            newAssignment = Assignment(new_name, earned, possible)
            NAcategory = self.profile.class_categories[tempCatName]
            NAcategory.AddAssignment(newAssignment)
            self.assignmentName.clear()
            self.points_Earned.setValue(0.0)
            self.points_Possible.setValue(0.0)
            self.refreshAssignments()
            self.newGrade()
        except Exception as E:
            QMessageBox.critical(self, "Error", str(E))

    def ThreshMod(self):
        if not self.profile:
            QMessageBox.warning(self, "No Class", "Create a class first.")
            return
        thresholds = {
            "A": float(self.A.value()),
            "B": float(self.B.value()),
            "C": float(self.C.value()),
            "D": float(self.D.value()),
            "F": float(self.F.value()),
        }
        try:
            self.profile.CreateThresholds(thresholds)
            QMessageBox.information(self, "Thresholds Updated", "Grade thresholds updated successfully.")
            self.newGrade()
        except Exception as E:
            QMessageBox.critical(self, "Invalid thresholds", str(E))

    def ThreshAlph(self):
        default_values = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0}
        self.A.setValue(default_values["A"])
        self.B.setValue(default_values["B"])
        self.C.setValue(default_values["C"])
        self.D.setValue(default_values["D"])
        self.F.setValue(default_values["F"])
        
        if self.profile:
             try:
                 self.profile.CreateThresholds(default_values)
             except Exception:
                 pass # Ignore if profile is mid-creation

    def CalcNeedToGet(self):
        if not self.profile:
            QMessageBox.warning(self, "No Class", "Create a class first.")
            return
        tempCatName = self.Hcat.currentText()
        if not tempCatName:
            QMessageBox.warning(self, "No Category", "Add a category first.")
            return
        try:
            PossibleValue = float(self.Hpossible.value())
        except Exception:
            QMessageBox.warning(self, "Input Error", "Enter valid possible points.")
            return
        if PossibleValue <= 0:
            QMessageBox.warning(self, "Input Error", "Possible points must be greater than 0.")
            return
        let = self.HletterGrade.currentText()
        try:
            # FIX: Use the profile's grade_thresholds dictionary directly
            threshold = float(self.profile.gradeBoundaries[let]) 
        except Exception:
            QMessageBox.critical(self, "Error", "Selected letter grade threshold not found.")
            return
            
        try:
            # FIX: Use the fixed predictor method from the class_profile
            needed_points = self.profile.CalcNeedToGet(tempCatName, PossibleValue, threshold)

            if needed_points == -1.0:
                sendback = f"Required score > 100% - target {threshold:.1f}% ({let}) is unrealistic."
            elif needed_points <= 0:
                sendback = "You already meet (or exceed) this target without the new assignment."
            else:
                needed_percent = (needed_points / PossibleValue) * 100.0
                sendback = f"You need {needed_percent:.2f}% ({needed_points:.2f} points) on the new assignment to reach at least {threshold:.1f}% ({let})."
            
            self.HresLabel.setText(sendback)
            
        except Exception as E:
            QMessageBox.critical(self, "Calculation Error", f"Failed to calculate required score: {str(E)}")
            self.HresLabel.setText("Calculation Failed.")


    def getProfile(self, profile: ClassProfile):
        self.profile = profile
        self.class_name_edit.setText(profile.class_name) # Update the current class name field
        self.categorySelector.clear()
        self.assignments.setRowCount(0)
        for _ in self.profile.class_categories.keys():
            self.categorySelector.addItem(_)
        self.ThreshreUP()
        self.newGrade()
        self.refreshSavedClasses() # Refresh to highlight current row
        
    def ThreshreUP(self):
        if self.profile:
            thresholds = self.profile.get_Boundaries()
        else:
            # Load default if no profile is active
            thresholds = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0}
            
        self.A.setValue(thresholds.get("A", 90.0))
        self.B.setValue(thresholds.get("B", 80.0))
        self.C.setValue(thresholds.get("C", 70.0))
        self.D.setValue(thresholds.get("D", 60.0))
        self.F.setValue(thresholds.get("F", 0.0))

    def newGrade(self):
        if not self.profile:
            self.shownGrade.setText("Current Grade: N/A")
            return
        try:
            Grade = self.profile.get_cur_grade() # Use the standardized calculation method
            letterGrade = self.profile.LetterGrade(Grade)
            self.shownGrade.setText(f"Current Grade: {Grade:.2f} % ({letterGrade})")
        except Exception as E:
            self.shownGrade.setText(f"Current Grade: Error")

    
    def refreshHypotheticalCats(self):
        self.Hcat.clear()
        if not self.profile:
            # If no profile is active, populate Hcat from the saved list's categories
            # This is complex and usually skipped; relying on refreshSavedClasses to load a profile first.
            return
        for _ in self.profile.class_categories.keys():
            self.Hcat.addItem(_)


    def refreshAssignments(self):
        self.assignments.setRowCount(0)
        category = self.categorySelector.currentText()
        if not category or not self.profile:
            return
        cat = self.profile.class_categories.get(category)
        if not cat:
            return
        for _ in cat.cat_assignments:
            row = self.assignments.rowCount()
            self.assignments.insertRow(row)
            self.assignments.setItem(row, 0, QTableWidgetItem(str(_.name)))
            self.assignments.setItem(row, 1, QTableWidgetItem(f"{_.earned_points:.2f}"))
            self.assignments.setItem(row, 2, QTableWidgetItem(f"{_.possible_points:.2f}"))

    def refreshClasses(self):
        self.savedClasses.clear()
        try:
            N = self.listnames()
            for _ in N:
                self.savedClasses.addItem(_)
        except Exception:
            pass
        self.refreshHypotheticalCats()
        
    def load_data(self):
        try:
            clss = load_data()
        except Exception as E:
            QMessageBox.critical(self, "Error", f"Error to load data: {E}")
            return
        if not clss:
            QMessageBox.information(self, "No Data", "No saved classes found.")
            return
        
        # FIXED: Only prompt for input if more than one class is found
        if len(clss) == 1:
            self.getProfile(clss[0])
            QMessageBox.information(self, "Class Loaded", f"Loaded class '{clss[0].class_name}'.")
            return
            
        dez = [_.class_name for _ in clss]
        X, Y = QInputDialog.getItem(self, "Select Class", "Class:", dez, 0, False)
        if Y and X:
            select = next((_ for _ in clss if _.class_name == X), None)
            if select:
                self.getProfile(select)
                QMessageBox.information(self, "Loaded", f"Loaded class '{select.class_name}'.")
        self.refreshSavedClasses()

    def save_data(self):
        if not self.profile:
            QMessageBox.warning(self, "No Class", "Make new class first.")
            return
        try:
            ClassOp(self.profile)
            QMessageBox.information(self, "Saved", "Current Class saved.")
            self.refreshSavedClasses()
        except Exception as E:
            QMessageBox.critical(self, "Error", "Failed to save class")

    def run_app():
        # QApplication is already imported at the top of qt_main.py
        app = QApplication(sys.argv)
        window = Grade_Calculator()
        window.show()
        sys.exit(app.exec_())
