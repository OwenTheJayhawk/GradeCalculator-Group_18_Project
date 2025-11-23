#import statements
import os
import sys
from typing import List

R = os.path.dirname(os.path.dirname(__file__)) #get parent directory
if R not in sys.path: #add parent directory to path
    sys.path.insert(0, R)
try: #try to import PyQt5
    from PyQt5.QtWidgets import(QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox, QScrollArea, QInputDialog, QListWidget, QFileDialog)
    from PyQt5.QtCore import Qt
except Exception as E: #Exception handling
    print("PyQt5 needed to run")
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
        savedClassBox = QGroupBox("Saved Classes") #saved classes box
        savedClassLayout = QVBoxLayout() #layout
        self.savedClasses = QListWidget() #list of saved classes
        buttons = QHBoxLayout() #button layout
        self.refreshButton = QPushButton("refresh") #refresh button
        self.refreshButton.clicked.connect(self.refreshSavedClasses) #refresh action_
        self.loadSelectedClassButton = QPushButton("Load Selected Class") #load selected class button
        self.loadSelectedClassButton.clicked.connect(self.loadSelectedClass) #Load class
        self.deleteSelectedClassButton = QPushButton("Delete Selected Class") #delete class
        self.deleteSelectedClassButton.clicked.connect(self.deleteSelectedClass) #delete action
        self.importButton = QPushButton("Import Class") # import class button
        self.importButton.clicked.connect(self.importClass) #import class
        self.exportButton = QPushButton("Export Class") #export class button
        self.exportButton.clicked.connect(self.exportClass) #export class
        buttons.addWidget(self.refreshButton) # add refresh button
        buttons.addWidget(self.loadSelectedClassButton) #add load button
        buttons.addWidget(self.deleteSelectedClassButton) #add delete button
        buttons.addWidget(self.importButton) #add import button
        buttons.addWidget(self.exportButton) #add export button
        savedClassLayout.addWidget(self.savedClasses) #add list to layout
        savedClassLayout.addLayout(buttons) #add buttons to layout
        savedClassBox.setLayout(savedClassLayout) #set layout
##################################################################################

#############################Category Box####################################
        categoryBox = QGroupBox("weighted Categories") #category box
        categoryFormat = QFormLayout() #layout
        self.EditCategoryName = QLineEdit() #category name input
        self.moveCategoryWeight = QDoubleSpinBox() #category weight input
        self.moveCategoryWeight.setRange(0.0, 100.0) #weight range
        self.moveCategoryWeight.setSuffix(" %") #weight suffix
        self.AddCategoryButton = QPushButton("Add Category") #add category button
        self.AddCategoryButton.clicked.connect(self.newCategory) #add category action
        categoryFormat.addRow("Name:", self.EditCategoryName) #category name row
        categoryFormat.addRow("Weight:", self.moveCategoryWeight) # category weight row
        categoryFormat.addRow(self.AddCategoryButton) #add category weight format
        categoryBox.setLayout(categoryFormat)  #set layout
################################################################################

###########################Assignment Category Selector##########################
        assignmentContainer = QGroupBox("Assignments") #assignment box
        LayoutOfAssignments = QVBoxLayout() #layout
        select_Buttons = QHBoxLayout() #selection layout
        select_Buttons.addWidget(QLabel("Category:")) #category label
        self.categorySelector = QComboBox() #category selector
        self.categorySelector.currentIndexChanged.connect(self.switchCategory) #change category action
        select_Buttons.addWidget(self.categorySelector) #add selector to layout
        LayoutOfAssignments.addLayout(select_Buttons) #add selection layout to main layout
#################################################################################

##########################Assignments Box########################################
        AssignmentLayout = QFormLayout() #assignment layout
        self.assignmentName = QLineEdit() #assignment name input
        self.points_Earned = QDoubleSpinBox() #points earned input
        self.points_Earned.setRange(0.0, 1000000.0) # points earned range
        self.points_Possible = QDoubleSpinBox() #points possible input
        self.points_Possible.setRange(0.0, 1000000.0)#points possible ranges
        self.NewAssignementBtn = QPushButton("Add Assignment") #add assignment button
        self.NewAssignementBtn.clicked.connect(self.MakeAssignment) #add assignment action
        AssignmentLayout.addRow("Name:", self.assignmentName) #name of assignment _row
        AssignmentLayout.addRow("Points Earned:", self.points_Earned) #points earned row
        AssignmentLayout.addRow("Points Possible:", self.points_Possible) #points possible row
        AssignmentLayout.addRow(self.NewAssignementBtn) #add assignment button row
################################################################################

###############################Grade Thresholds Box################################
        Thresholds = QGroupBox("Grade Thresholds") #thresholds box
        ThreshFormat = QFormLayout() #layout
        self.A = QDoubleSpinBox() #A threshold input
        self.A.setRange(0.0, 100.0) #A range
        self.A.setSuffix(" %") #A suffix
        self.B = QDoubleSpinBox() #B threshold input
        self.B.setRange(0.0, 100.0) #B range
        self.B.setSuffix(" %") #B suffix
        self.C = QDoubleSpinBox() #C threshold input
        self.C.setRange(0.0, 100.0) #C range
        self.C.setSuffix(" %") #C suffix
        self.D = QDoubleSpinBox() #D threshold input
        self.D.setRange(0.0, 100.0) #D range
        self.D.setSuffix(" %") #D suffix
        self.F = QDoubleSpinBox() #F threshold input
        self.F.setRange(0.0, 100.0) #F range
        self.F.setSuffix(" %") #F suffix
        self.changeThreshB = QPushButton("Apply Thresholds") #apply thresholds button
        self.changeThreshB.clicked.connect(self.ThreshMod) #apply thresholds action
        self.Thresh_reset = QPushButton("Reset to Default") #reset thresholds button
        self.Thresh_reset.clicked.connect(self.ThreshAlph) #reset thresholds action
        ThreshFormat.addRow("A:", self.A) #A row
        ThreshFormat.addRow("B:", self.B) #B row
        ThreshFormat.addRow("C:", self.C) #C row
        ThreshFormat.addRow("D:", self.D) #D row
        ThreshFormat.addRow("F:", self.F) #F row
        ThreshFormat.addRow(self.changeThreshB) #apply button row
        ThreshFormat.addRow(self.Thresh_reset) #reset button row
        Thresholds.setLayout(ThreshFormat) #set layout
##################################################################################

##################################Hypothetical Grade Box##################################
        Hypothetical_Box = QGroupBox("Hypothetical Required Score") #hypothetical grade box
        LayoutForHypothetical = QFormLayout() #layout
        self.Hcat = QComboBox() #category selector
        self.Hcat.setToolTip("Select category to calculate required score for") 
        self.Hpossible = QDoubleSpinBox() #possible points input
        self.Hpossible.setRange(0.0, 1000000.0) #possible points range
        self.Hpossible.setValue(100.0) #default possible points
        self.HletterGrade = QComboBox() #letter grade selector
        self.HletterGrade.addItems(["A", "B", "C", "D", "F"]) #letter grade options
        self.Hfind = QPushButton("Calculate Required %") #calculate button
        self.Hfind.clicked.connect(self.CalcNeedToGet) #calculate action
        self.HresLabel = QLabel("") #result label
        LayoutForHypothetical.addRow("Category:", self.Hcat) #category row
        LayoutForHypothetical.addRow("New assignment possible points:", self.Hpossible) #possible points row
        LayoutForHypothetical.addRow("Target letter:", self.HletterGrade) #target letter row
        LayoutForHypothetical.addRow(self.Hfind) #calculate button row
        LayoutForHypothetical.addRow(self.HresLabel) #result label row
        Hypothetical_Box.setLayout(LayoutForHypothetical) #set layout
#########################################################################################

################################List of Assignments####################################
        self.assignments = QTableWidget(0, 3) #assignments table
        self.assignments.setHorizontalHeaderLabels(["Name", "Earned", "Possible"]) #table headers
        AssignmentLayout.addRow(self.assignments) #add table to layout
        LayoutOfAssignments.addLayout(AssignmentLayout) #add layout to container
        assignmentContainer.setLayout(LayoutOfAssignments) #set layout
##########################################################################################

################################Show Grade################################################
        gradeShow = QHBoxLayout() #layout
        self.shownGrade = QLabel("Current Grade: N/A") #current grade label
        gradeShow.addStretch() 
        gradeShow.addWidget(self.shownGrade) #add label to layout
###########################################################################################

################################General####################################################
        MidLayout.addWidget(classBox) #add class box to main layout
        MidLayout.addWidget(savedClassBox) #add saved class box to main layout
        MidLayout.addWidget(categoryBox) #add category box to main layout
        MidLayout.addWidget(Hypothetical_Box) #add hypothetical box to main layout
        MidLayout.addWidget(assignmentContainer) #add assignment container to main layout
        MidLayout.addWidget(Thresholds) #add thresholds box to main layout
        MidLayout.addLayout(gradeShow) #add grade show layout to main layout
        Middle.setLayout(MidLayout) #set main layout
        UpDownScroll = QScrollArea() #scroll area
        UpDownScroll.setWidgetResizable(True) #make scroll area resizable
        UpDownScroll.setWidget(Middle) #set main widget
        self.setCentralWidget(UpDownScroll) #set central widget
        self.ThreshAlph() #set default thresholds
        self.refreshSavedClasses() #refresh saved classes
############################################################################################


    def MakeClass(self): #create new class
        N = self.class_name_edit.text().strip() #get class name
        if not N: #check if empty
            QMessageBox.warning(self, "Input Error", "Enter a valid class name") #show warning
            return #exit
        self.profile = ClassProfile(N) #create profile
        self.categorySelector.clear() #clear category selector
        self.assignments.setRowCount(0) #clear assignments table
        self.ThreshAlph() #reset thresholds to default
        self.refreshHypotheticalCats() #refresh hypothetical categories
        self.newGrade() #update grade display
        QMessageBox.information(self, "Class Created", f"Created class '{N}'.") #show confirmation
    
    def refreshSavedClasses(self): #refresh saved classes list
        self.savedClasses.clear() #clear list
        try: #try to load classes
            N = listnames() #get class names
            for _ in N: #iterate through names
                self.savedClasses.addItem(_) #add to list
        except Exception: #handle errors
            pass #ignore errors
        self.refreshHypotheticalCats() #refresh hypothetical categories

    def loadSelectedClass(self): #load selected class
        i = self.savedClasses.currentItem() #get selected item
        if not i: #check if item selected
            QMessageBox.warning(self, "Select class", "Please select a class to load.") #show warning
            return #exit
        N = i.text() #get class name
        clss = load_data() #load all classes
        select = next((_ for _ in clss if _.class_name == N), None) #find matching class
        if select: #if found
            self.getProfile(select) #load profile
            QMessageBox.information(self, "Loaded", f"Loaded class '{select.class_name}'.") #show confirmation

    def deleteSelectedClass(self): #delete selected class
        i = self.savedClasses.currentItem() #get selected item
        if not i: #check if item selected
            QMessageBox.warning(self, "Select class", "Please select a saved class to delete.") #show warning
            return #exit
        N = i.text() #get class name
        check = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete class '{N}'?", QMessageBox.Yes | QMessageBox.No) #confirm deletion
        if check == QMessageBox.Yes: #if confirmed
            if deleteClass(N): #delete class
                QMessageBox.information(self, "Deleted", f"'{N}' deleted.") #show confirmation
                self.refreshSavedClasses() #refresh list
            else: #if delete failed
                QMessageBox.warning(self, "Error", "Selected class could not be found") #show error
                
    def importClass(self): #import class from file
        P, _ = QFileDialog.getOpenFileName(self, "Import Class Data", "", "JSON Files (*.json);;All Files (*)") #open file dialog
        if not P: #if no file selected
            return #exit
        try: #try to import
            clss = load_data(P) #load classes from file
            if not clss: #if no classes found
                QMessageBox.information(self, "No classes", "No classes found in the selected file.") #show message
                return #exit
            for _ in clss: #iterate through classes
                ClassOp(_) #save each class
            self.refreshSavedClasses() #refresh list
            QMessageBox.information(self, "Imported", f"Imported {len(clss)} classes.") #show confirmation
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Error", "Import failed)") #show error
    
    def exportClass(self): #export class to file
        i = self.savedClasses.currentItem() #get selected item
        if not i: #check if item selected
            QMessageBox.warning(self, "Select class", "Please select a saved class to export.") #show warning
            return #exit
        N = i.text() #get class name
        clss = load_data() #load all classes
        select = next((_ for _ in clss if _.class_name == N), None) #find matching class
        if not select: #if not found
            QMessageBox.warning(self, "Not Found", "Selected class could not be found") #show error
            return #exit
        P, _ = QFileDialog.getSaveFileName(self, "Export Class Data", f"{N}.json", "JSON Files (*.json);;All Files (*)") #open save dialog
        if not P: #if no file selected
            return #exit
        try: #try to export
            save_data([select], P) #save class to file
            QMessageBox.information(self, "Exported", f"Exported '{N}'") #show confirmation
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Failed export", str(E)) #show error

    def newCategory(self): #add new category
        if not self.profile: #check if profile exists
            QMessageBox.warning(self, "No Class", "Create a class first.") #show warning
            return #exit
        N = self.EditCategoryName.text().strip() #get category name
        W = float(self.moveCategoryWeight.value()) #get category weight
        if not N: #check if name empty
            QMessageBox.warning(self, "Input required", "Please enter a category name.") #show warning
            return #exit
        try: #try to add category
            newCategory = Category(N, W) #create category
            self.profile.AddCategory(newCategory) #add to profile
            self.categorySelector.addItem(newCategory.cat_name) #add to selector
            self.EditCategoryName.clear() #clear name input
            self.moveCategoryWeight.setValue(0.0) #reset weight input
            self.refreshHypotheticalCats() #refresh hypothetical categories
            self.newGrade() #update grade display
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Error", str(E)) #show error
            

    def switchCategory(self): #switch selected category
        self.refreshAssignments() #refresh assignments table

    def MakeAssignment(self): #add new assignment
        if not self.profile: #check if profile exists
            QMessageBox.warning(self, "No Class", "Create a class first.") #show warning
            return #exit
        tempCatName = self.categorySelector.currentText() #get selected category
        if not tempCatName: #check if category selected
            QMessageBox.warning(self, "No Category", "Add a category first.") #show warning
            return #exit
        new_name = self.assignmentName.text().strip() #get assignment name
        earned = float(self.points_Earned.value()) #get points earned
        possible = float(self.points_Possible.value()) #get points possible
        if not new_name: #check if name empty
            QMessageBox.warning(self, "Input Error", "Please enter an assignment name.") #show warning
            return #exit
        try: #try to add assignment
            newAssignment = Assignment(new_name, earned, possible) #create assignment
            NAcategory = self.profile.class_categories[tempCatName] #get category
            NAcategory.AddAssignment(newAssignment) #add assignment to category
            self.assignmentName.clear() #clear name input
            self.points_Earned.setValue(0.0) #reset earned input
            self.points_Possible.setValue(0.0) #reset possible input
            self.refreshAssignments() #refresh assignments table
            self.newGrade() #update grade display
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Error", str(E)) #show error

    def ThreshMod(self): #modify grade thresholds
        if not self.profile: #check if profile exists
            QMessageBox.warning(self, "No Class", "Create a class first.") #show warning
            return #exit
        thresholds = { #create thresholds dict
            "A": float(self.A.value()), #A threshold
            "B": float(self.B.value()), #B threshold
            "C": float(self.C.value()), #C threshold
            "D": float(self.D.value()), #D threshold
            "F": float(self.F.value()), #F threshold
        }
        try: #try to update thresholds
            self.profile.CreateThresholds(thresholds) #apply thresholds
            QMessageBox.information(self, "Thresholds Updated", "Grade thresholds updated successfully.") #show confirmation
            self.newGrade() #update grade display
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Invalid thresholds", str(E)) #show error

    def ThreshAlph(self): #set default thresholds
        default_values = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0} #default values
        self.A.setValue(default_values["A"]) #set A threshold
        self.B.setValue(default_values["B"]) #set B threshold
        self.C.setValue(default_values["C"]) #set C threshold
        self.D.setValue(default_values["D"]) #set D threshold
        self.F.setValue(default_values["F"]) #set F threshold

    def CalcNeedToGet(self): #calculate required score for target grade
        if not self.profile: #check if profile exists
            QMessageBox.warning(self, "No Class", "Create a class first.") #show warning
            return #exit
        tempCatName = self.Hcat.currentText() #get selected category
        if not tempCatName: #check if category selected
            QMessageBox.warning(self, "No Category", "Add a category first.") #show warning
            return #exit
        try: #try to get possible points
            PossibleValue = float(self.Hpossible.value()) #get possible points
        except Exception: #handle errors
            QMessageBox.warning(self, "Input Error", "Enter valid possible points.") #show warning
            return #exit
        if PossibleValue <= 0: #check if positive
            QMessageBox.warning(self, "Input Error", "Possible points must be greater than 0.") #show warning
            return #exit
        let = self.HletterGrade.currentText() #get target letter grade
        try: #try to get threshold
            threshold = float(self.profile.gradeBoundaries[let]) #get threshold value
        except Exception: #handle errors
            QMessageBox.critical(self, "Error", "Selected letter grade threshold not found.") #show error
            return #exit
        altScore = 0.0 #initialize score without target category
        altWeight = 0.0 #initialize weight without target category
        mainCat = self.profile.class_categories.get(tempCatName) #get target category
        if mainCat is None: #check if category exists
            QMessageBox.critical(self, "Error", "Selected category not found.") #show error
            return #exit
        for N, C in self.profile.class_categories.items(): #iterate through categories
            if N == tempCatName: #if target category
                altWeight += C.cat_weight #add weight
                continue #skip to next
            if C.cat_assignments: #if category has assignments
                altCatScore = C.getCatScore() #get category score
                div = (altCatScore["percentage"] / 100.0) * C.cat_weight #calculate weighted score
                altScore += div #add to total
                altWeight += C.cat_weight #add weight
        altCatScore = mainCat.getCatScore() #get target category score
        Earned = float(altCatScore["earned"]) #get earned points
        Possible = float(altCatScore["possible"]) #get possible points
        endWeight = float(mainCat.cat_weight) #get target category weight
        if endWeight <= 0: #check if weight positive
            QMessageBox.warning(self, "Weight Error", "Selected category has zero weight.") #show warning
            return #exit
        num = (threshold / 100.0) * (altWeight + endWeight) - altScore #calculate required weighted score
        newVal = (num / endWeight) * (Possible + PossibleValue) #calculate required total points
        final = (newVal - Earned) * 100.0 / PossibleValue #calculate required percentage
        if final <= 0: #if already meets target
            sendback = "You already meet (or exceed) this target without the new assignment." #message
        elif final > 100: #if target unrealistic
            sendback = f"Required score if {final:.2f}%. That's greater than 100% - target is unrealistic." #message
        else: #if target achievable
            sendback = f"You need {final:.2f}% on the new assignment to reach at least {threshold:.1f}% ({let})." #message
        self.HresLabel.setText(sendback) #display result

    def getProfile(self, profile: ClassProfile): #load profile into UI
        self.profile = profile #set active profile
        self.categorySelector.clear() #clear category selector
        for _ in self.profile.class_categories.keys(): #iterate through categories
            self.categorySelector.addItem(_) #add category to selector
        self.ThreshreUP() #update threshold values
        self.newGrade() #update grade display
        try: #try to select in saved classes list
            x = listnames().index(self.profile.class_name) #find index
            self.savedClasses.setCurrentRow(x) #select row
        except Exception: #handle errors
            pass #ignore errors
        self.refreshHypotheticalCats() #refresh hypothetical categories

    def ThreshreUP(self): #update threshold display
        if self.profile: #if profile exists
            thresholds = self.profile.get_Boundaries() #get profile thresholds
        else: #if no profile
            thresholds = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0} #use defaults
        self.A.setValue(thresholds["A"]) #set A threshold
        self.B.setValue(thresholds["B"]) #set B threshold
        self.C.setValue(thresholds["C"]) #set C threshold
        self.D.setValue(thresholds["D"]) #set D threshold
        self.F.setValue(thresholds["F"]) #set F threshold

    def newGrade(self): #update grade display
        if not self.profile: #check if profile exists
            self.shownGrade.setText("Current Grade: N/A") #show N/A
            return #exit
        try: #try to calculate grade
            Grade = self.profile.get_cur_grade() #get current grade
            letterGrade = self.profile.LetterGrade(Grade) #get letter grade
            self.shownGrade.setText(f"Current Grade: {Grade} % ({letterGrade})") #display grade
        except Exception as E: #handle errors
            self.shownGrade.setText("Current Grade: Error") #show error

    def refreshHypotheticalCats(self): #refresh hypothetical category selector
        self.Hcat.clear() #clear selector
        if not self.profile: #check if profile exists
            return #exit
        for _ in self.profile.class_categories.keys(): #iterate through categories
            self.Hcat.addItem(_) #add category to selector

    def refreshAssignments(self): #refresh assignments table
        self.assignments.setRowCount(0) #clear table
        category = self.categorySelector.currentText() #get selected category
        if not category or not self.profile: #check if category selected and profile exists
            return #exit
        cat = self.profile.class_categories.get(category) #get category
        if not cat: #check if category exists
            return #exit
        for _ in cat.cat_assignments: #iterate through assignments
            row = self.assignments.rowCount() #get current row count
            self.assignments.insertRow(row) #insert new row
            self.assignments.setItem(row, 0, QTableWidgetItem(str(_.name))) #set name
            self.assignments.setItem(row, 1, QTableWidgetItem(str(_.earned_points))) #set earned points
            self.assignments.setItem(row, 2, QTableWidgetItem(str(_.possible_points))) #set possible points

    def load_data(self): #load class data
        try: #try to load classes
            clss = load_data() #load all classes
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Error", f"Error to load data: {E}") #show error
            return #exit
        if not clss: #check if classes found
            QMessageBox.information(self, "No Data", "No saved classes found.") #show message
            return #exit
        if len(clss) == 1: #if only one class
            self.getProfile(clss[0]) #load that class
            QMessageBox.information(self, "Class Loaded", f"Loaded class '{clss[0].class_name}'.") #show confirmation
            return #exit
        dez = [_.class_name for _ in clss] #get class names
        X, Y = QInputDialog.getItem(self, "Select Class", "Class:", dez, 0, False) #show selection dialog
        if Y and X: #if class selected
            select = next((_ for _ in clss if _.class_name == X), None) #find class
            if select: #if found
                self.getProfile(select) #load profile
                QMessageBox.information(self, "Loaded", f"Loaded class '{select.class_name}'.") #show confirmation
        self.refreshSavedClasses() #refresh saved classes list

    def save_data(self): #save class data
        if not self.profile: #check if profile exists
            QMessageBox.warning(self, "No Class", "Make new class first.") #show warning
            return #exit
        try: #try to save
            ClassOp(self.profile) #save profile
            QMessageBox.information(self, "Saved", "Current Class saved.") #show confirmation
            self.refreshSavedClasses() #refresh saved classes list
        except Exception as E: #handle errors
            QMessageBox.critical(self, "Error", "Failed to save class") #show error

def listnames() -> List[str]: #get list of saved class names
    return [_.class_name for _ in load_data()] #return class names

def run(): #run application
    try: #try to import PyQt5
        from PyQt5.QtWidgets import QApplication #import QApplication
    except Exception: #handle errors
        print("PyQt5 is required to run this application.") #print error
        return #exit
    Application = QApplication(sys.argv) #create application
    ViewWindow = Grade_Calculator() #create window
    ViewWindow.show() #show window
    sys.exit(Application.exec_()) #execute application

if __name__ == "__main__": #if run as main
    run() #run application
