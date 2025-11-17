#import commands
import sys
import subprocess
import importlib.util

procs = [] #process list

def launch_app_B(): #launch app
    try:
        from GUI.qt_main import run_app
    except Exception as E: #error handling
        print("Cannot import. Make sure PyQt5 is installed")
        print("Error: ", E)
        return
    run_app()

def launch_app_NB(): #launch app in new process
    if importlib.util.find_spec('PyQt') is None: #check for PyQT5
        print('PyQT5 not found')
        return
    pyth = sys.executable or 'python' #python executable
    command = [pyth, '-m', 'GUI.qt_main'] #run command
    try:
        start = None #default value
        flags = 0
        if sys.platform.startswith('win'): 
            try:
                start = subprocess.STARTUPINFO()
                start.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            except Exception:
                start = None
        P = subprocess.Popen(command, stdout=subprocess.DEVNULL, stdin = subprocess.DEVNULL, start = start, flags = flags)
        procs.append(P)
        print("launched GUI")
    except Exception as E:
        print("GUI launch failed")

def main():
    while True:
        print("\nGrade Calculator Menu")
        print("1) Lauch B")
        print("2) Launch NB")
        print("3) Exit")
        path = input("Select: ").strip()
        if path == '1':
            launch_app_B()
        elif path == '2':
            launch_app_NB()
        elif path == '3':
            print("Exiting")
            break
        else:
            print("Invalid selection")

if __name__ == '__main__':
    main()
