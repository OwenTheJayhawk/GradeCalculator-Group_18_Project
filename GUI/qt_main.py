#import statements
import os
import sys

R = os.path.dirname(os.path.dirname(__file__)) #get parent directory
if R not in sys.path: #add parent directory to path
    sys.path.insert(0, R)
try: #try to import PyQt5
    from PyQt5.QtWidgets import(QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLable, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox, QScrollArea, QInputDialog, QListWidget, QFileDialog)
    from PyQt5.QtCore import Qt
except Exception as E: #Exception handling
    print("PyAt5 needed to run")
    print("Error:", E)
    sys.exit(1)
from assignment import Assignment
from category import Category
from class_profile import ClassProfile
from data_manager import(load_data, save_data, ClassOp, deleteClass)

class Grade_Calculator(QMainWindow): #Main window class
    def __init__(self): #initalize values
        super().__init__() #call parent constructor
        self.setWindowTitle("Grade Calculator") #make window title
        self.resize(800, 480) #set window size
        self.profile = None #set profile to None
        self.CreateUI() #Create UI
    def CreateUI(self): #Create UI elements
        Middle = QWidget() #main box
        MidLayout = QVBoxLayout() #main box layout
###############################Class Box################################
        classBox = QGroupBox("Course") #class box
        classLayout = QHBoxLayout() #layout 
        self.class_name_edit = QLineEdit() #input class name
        self.class_name_edit.setPlaceholderText("Enter Class Name") #placeholder text
        self.create_class_btn = QPushButton("Create Class") #create class button
        self.create_class_btn.clicked.connect(self.MakeClass) #create class button action
        classLayout.addWidget(QLabel("Class:")) #class label
        classLayout.addWidget(self.class_name_edit) #input for class name
        classLayout.addWidget(self.create_class_btn) #create class button
        self.load_data_btn = QPushButton("Load Class Data") #load class button
        self.load_data_btn.clicked.connect(self.load_data) #action to load class
        self.save_data_btn = QPushButton("Save Current Class") #save class button
        self.save_data_btn.clicked.connect(self.save_data)
        classLayout.addWidget(self.load_data_btn) #place load button in layout
        classLayout.addWidget(self.save_data_btn) #place save button in layout
        classBox.setLayout(classLayout) #set layout
###########################################################################

##############################Saved Classes Box##############################
        savedClassBox = QGroupBox("Saved Classes")
        savedClassLayout = QVBoxLayout()
        self.savedClasses = QListWidget()
        buttons = QHBoxLayout()
        self.refreshButton = QPushButton("refresh")
        self.refreshButton.clicked.connect(self.refreshSavedClasses)
        self.loadSelectedClassButton = QPushButton("Load Selected Class")
        self.loadSelectedClassButton.clicked.connect(self.loadSelectedClass)
        self.deleteSelectedClassButton = QPushButton("Delete Selected Class")
        self.deleteSelectedClassButton.clicked.connect(self.deleteSelectedClass)
        self.importButton = QPushButton("Import Class")
        self.importButton.clicked.connect(self.importClass)
        self.exportButton = QPushButton("Export Class")
        self.exportButton.clicked.connect(self.exportClass)
        buttons.addWidget(self.refreshButton)
        buttons.addWidget(self.loadSelectedClassButton)
        buttons.addWidget(self.deleteSelectedClassButton)
        buttons.addWidget(self.importButton)
        buttons.addWidget(self.exportButton)
        savedClassLayout.addWidget(self.savedClasses)
        savedClassLayout.addLayout(buttons)
        savedClassBox.setLayout(savedClassLayout)
##################################################################################

#############################Category Box####################################
        categoryBox = QGroupBox("weighted Categories")
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
        assignmentContainer.addWidget(self.categorySelector)
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
        AssignmentLayout.addLayout(AssignmentLayout)
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
        AssignmentLayout.addWidget(self.assignments)
        LayoutOfAssignments.setLayout(AssignmentLayout)
##########################################################################################

################################Show Grade################################################
        gradeShow = QHBoxLayout()
        self.shownGrade = QLabel("Current Grade: N/A")
        gradeShow.addStretch()
        gradeShow.addWidget(self.shownGrade)
###########################################################################################

################################General####################################################
        MidLayout.addWidget(classBox)
        MidLayout.addWidget(savedClassBox)
        MidLayout.addWidget(categoryBox)
        MidLayout.addWidget(Hypothetical_Box)
        MidLayout.addWidget(assignmentContainer)
        MidLayout.addLayout(ThreshFormat)
        MidLayout.addLayout(gradeShow)
        Middle.setLayout(MidLayout)
        UpDownScroll = QScrollArea()
        UpDownScroll.setWidgetResizable(True)
        UpDownScroll.setWidget(Middle)
        self.setCentralWidget(UpDownScroll)
        self.Thresh_reset()
        self.refreshSavedClasses()
############################################################################################


    def MakeClass(self):
        N = self.class_name_edit.text().strip()
        if not N:
            QMessageBox.warning(self, "Input Error", "Enter a valid class name")
            return
        self.profile = ClassProfile(N)
        self.categorySelector.clear()
        self.assignments.setRowCount(0)
        self.Thresh_reset()
        self.updateGradeDisplay()
        QMessageBox.information(self, "Class Created", f"Created class '{N}'.")
    
    def refreshSavedClasses(self):
        self.savedClasses.clear()
        try:
            N = listnames()
            for _ in N:
                self.savedClasses.addItem(_)
        except Exception:
            pass
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
            QMessageBox.information(self, "Loaded", f"Loaded class '{select.class_name}'.")

    def deleteSelectedClass(self):
        i = self.savedClasses.currentItem()
        if not i:
            QMessageBox.warning(self, "Select class", "Please select a saved class to delete.")
            return
        N = i.text()
        check = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete class '{N}'?", QMessageBox.Yes | QMessageBox.No)
        if check == QMessageBox.Yes:
            if deleteClass(N):
                QMessageBox.information(self, "Deleted", f"'{N}' deleted.")
                self.refreshSavedClasses()
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
                ClassOp(_)
            self.refreshSavedClasses()
            QMessageBox.information(self, "Imported", f"Imported {len(clss)} classes.")
        except Exception as E:
            QMessageBox.critical(self, "Error", "Import failed)")
    
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
        try:
            newCategory = Category(N, W)
            self.profile.AddCategory(newCategory)
            self.categorySelector.addItem(newCategory.cat_name)
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
        try:
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
            threshold = float(self.profile.grade_thresholds[let])
        except Exception:
            QMessageBox.critical(self, "Error", "Selected letter grade threshold not found.")
            return
        altScore = 0.0
        altWeight = 0.0
        mainCat = self.profile.class_categories.get(tempCatName)
        if mainCat is None:
            QMessageBox.critical(self, "Error", "Selected category not found.")
            return
        for N, C in self.profile.class_categories.items():
            if N == tempCatName:
                altWeight += C.cat_weight
                continue
            if C.cat_assignments:
                altCatScore = C.getCatScore()
                div = (altCatScore["percentage"] / 100.0) * C.cat_weight
                altScore += div
                altWeight += C.cat_weight
        altCatScore = mainCat.getCatScore()
        Earned = float(altCatScore["earned"])
        Possible = float(altCatScore["possible"])
        endWeight = float(mainCat.cat_weight)
        if endWeight <= 0:
            QMessageBox.warning(self, "Weight Error", "Selected category has zero weight.")
            return
        num = (threshold / 100.0) * (altWeight + endWeight) - altScore
        newVal = (num / endWeight) * (Possible + PossibleValue)
        final = (newVal - Earned) * 100.0 / PossibleValue
        if final <= 0:
            sendback = "You already meet (or exceed) this target without the new assignment."
        elif final > 100:
            sendback = f"Required score if {final:.2f}%. That's greater than 100% - target is unrealistic."
        else:
            sendback = f"You need {final:.2f}% on the new assignment to reach at least {threshold:.1f}% ({let})."
        self.HresLabel.setText(sendback)

    def getProfile(self, profile: ClassProfile):
        self.prof = profile
        self.categorySelector.clear()
        for _ in self.prof.class_categories.keys():
            self.categorySelector.addItem(_)
        self.ThreshreUP()
        self.newGrade()
        try:
            x = listnames().index(self.prof.class_name)
            self.savedClasses.setCurrentRow(x)
        except Exception:
            pass
        self.refreshHypotheticalCats()

    def ThreshreUP(self):
        if self.profile:
            thresholds = self.profile.get_Boundaries()
        else:
            thresholds = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0}
        self.A.setValue(thresholds["A"])
        self.B.setValue(thresholds["B"])
        self.C.setValue(thresholds["C"])
        self.D.setValue(thresholds["D"])
        self.F.setValue(thresholds["F"])

    def newGrade(self):
        if not self.profile:
            self.shownGrade.setText("Current Grade: N/A")
            return
        try:
            Grade = self.profile.calculateOverallGrade()
            letterGrade = self.profile.getLetterGrade(Grade)
            self.shownGrade.setText(f"Current Grade: {Grade} % ({letterGrade})")
        except Exception as E:
            self.shownGrade.setText("Current Grade: Error")

    def listnames() -> List[str]:
        return [_.class_name for _ in load_data()]
    
    def refreshHypotheticalCats(self):
        self.Hcat.clear()
        if not self.profile:
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
            self.assignments.setItem(row, 1, QTableWidgetItem(str(_.earned_points)))
            self.assignments.setItem(row, 2, QTableWidgetItem(str(_.possible_points)))

    def refreshClasses(self):
        self.savedClasses.clear()
        try:
            N = listnames()
            for _ in N:
                self.savedClasses.addItem(_)
        except Exception:
            pass
        self.refreshHypotheticalCats()

def run():
    try:
        from PyQt5.QtWidgets import QApplication
    except Exception:
        print("PyQt5 is required to run this application.")
        return
    Application = QApplication(sys.argv)
    ViewWindow = Grade_Calculator()
    ViewWindow.show()
    sys.exit(Application.exec_())

if __name__ == "__main__":
    run()

    
"""
    def load_data(self):
        try:
            clss = load_data()
        except Exception as E:
            QMessageBox.critical(self, "Error", f"Error to load data: {E}")
            return
        if not clss:
            QMessageBox.information(self, "No Data", "No saved classes found.")
            return
        if len(clss == 1):
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
"""
