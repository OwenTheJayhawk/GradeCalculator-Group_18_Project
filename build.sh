#!/bin/bash
# Script to build the Grade Calculator executable using PyInstaller.

# --- Prerequisites ---
# If you need to install PyInstaller, use the following command:
# pip3 install pyinstaller

# --- Clean up previous builds ---
echo "Cleaning up previous build directories..."
rm -rf build
rm -rf dist
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# --- Run PyInstaller using the specification file ---
# --onefile: Creates a single executable file (recommended for ease of distribution)
# --name: Overrides the name in the spec file, but using the spec file name is fine.

echo "Starting PyInstaller build..."
pyinstaller grade_calculator.spec --onefile

# --- Post-Build Information ---
if [ -d "dist" ]; then
    echo "================================================="
    echo "✅ Build successful!"
    echo "The executable is located in the 'dist' folder."
    
    # Check OS to give specific instructions
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux Executable: dist/GradeCalculator"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS Executable: dist/GradeCalculator"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "Windows Executable: dist/GradeCalculator.exe"
    else
        echo "Executable name depends on the host OS."
    fi
    echo "================================================="
else
    echo "❌ Build failed. Check PyInstaller output for errors."
fi