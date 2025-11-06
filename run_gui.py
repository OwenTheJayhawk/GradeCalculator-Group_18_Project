
import sys
import os

if __name__ == '__main__':
    
    root = os.path.dirname(__file__)
    if root not in sys.path:
        sys.path.insert(0, root)

    try:
        from GUI.qt_main import run_app
    except Exception as e:
        print("Failed to import GUI. Is PyQt5 installed?", e)
        print("Install with: pip install PyQt5")
        sys.exit(1)

    run_app()
