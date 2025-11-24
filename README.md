🎓 Grade Calculator (Group 18 Project)

Welcome to the Grade Calculator, a robust desktop application designed to help students track their academic performance, manage weighted grading categories, and predict future scores needed to achieve a target grade.

✨ Key Features

Weighted Grading: Define custom grading categories (e.g., Homework, Midterms) and assign percentage weights.

Real-time Score: Instantly calculates and displays your current weighted percentage and letter grade.

Predictive Analysis: Use the Hypothetical Required Score tool to calculate the exact points needed on a future assignment (like a final exam) to reach a specific target grade (e.g., an 'A').

Local Persistence: Save and load multiple class profiles (e.g., "EECS 581," "History 101") locally on your machine.

Editable Data: Easily edit or delete assignments after they have been entered.

🚀 Installation & Launch (Standalone Executable)

We have successfully packaged the application into standalone executables. You do not need to install Python or any libraries to run the application.

The built files can be found in the dist/ directory of this repository after a successful build process.

Prerequisites

You only need to download the appropriate file for your operating system from the dist/ folder.

Operating System

Download File (Example)

macOS (Intel/Apple Silicon)

GradeCalculator (No extension)

Windows (64-bit)

GradeCalculator.exe

Launch Instructions

💻 macOS

Download: Download the GradeCalculator file from the dist/ folder.

Locate: Move the file to a preferred location (e.g., your Desktop).

Permissions: You must give the file permission to execute via the terminal:

# Navigate to the directory where you saved the file (e.g., Desktop)
cd ~/Desktop

# Give the file execute permission
chmod +x GradeCalculator

# Run the application
./GradeCalculator


If macOS displays a "Developer cannot be verified" security message, go to System Settings > Privacy & Security and click "Open Anyway" for the GradeCalculator app.

🖥️ Windows

Download: Download the GradeCalculator.exe file from the dist/ folder.

Run: Simply double-click the GradeCalculator.exe file.

⚙️ Running from Source (For Developers)

If you prefer to run the application directly from the Python files, follow these instructions.

Clone the Repository:

git clone [Insert Repository URL Here]
cd GradeCalculator-Group_18_Project


Install Dependencies:
You only need to install PyQt5. Use your specific pip3 command:

pip3 install PyQt5


Run the Application:
Execute the main script:

python3 run_gui.py


