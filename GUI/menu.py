import sys
import subprocess
import importlib.util


_launched_procs = []


def launch_gui_blocking():
	
	try:
		from GUI.qt_main import run_app
	except Exception as e:
		print("Unable to import GUI. Make sure PyQt5 is installed and available.")
		print("Error:", e)
		print("Install with: pip install PyQt5")
		return

	
	run_app()


def launch_gui_nonblocking():
	
	
	if importlib.util.find_spec('PyQt5') is None:
		print("PyQt5 not found in this environment. Install with: pip install PyQt5")
		return

	python = sys.executable or 'python'
	cmd = [python, '-m', 'GUI.qt_main']

	try:
		
		startupinfo = None
		creationflags = 0
		if sys.platform.startswith('win'):
			try:
				startupinfo = subprocess.STARTUPINFO()
				startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			except Exception:
				startupinfo = None

		proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
								stdin=subprocess.DEVNULL, startupinfo=startupinfo,
								creationflags=creationflags)
		_launched_procs.append(proc)
		print(f"Launched GUI in background (pid={proc.pid}). Return to menu to continue.")
	except Exception as e:
		print("Failed to launch GUI", e)


def main():
	while True:
		print("\nGrade Calculator Menu")
		print("1) Launch PyQt5 GUI (blocking)")
		print("2) Launch PyQt5 GUI (non-blocking)")
		print("3) Exit")
		choice = input("Select an option: ").strip()
		if choice == '1':
			launch_gui_blocking()
		elif choice == '2':
			launch_gui_nonblocking()
		elif choice == '3':
			print("Exiting.")
			break
		else:
			print("Invalid selection. Choose 1, 2, or 3.")


if __name__ == '__main__':
	main()



