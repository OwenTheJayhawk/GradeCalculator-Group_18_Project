#import commands
import sys
import os

if __name__ == '__main__':
    R = os.path.dirname(__file__) #file path
    if R not in sys.path:# add to path
        sys.path.insert(0, R)
    try:
        # --- FIXED IMPORT: Import the module instead of the function directly ---
        import GUI.qt_main as qt_main #import the GUI runner
    except Exception as E: #error handling
        print("GUI import failed. Install PyQt5", E)
        print("use 'pip install PyQt5' to install")
        sys.exit(1)

    # Call the function from the imported module
    qt_main.run_app()