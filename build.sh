#!/bin/bash
# Script to build the Grade Calculator executable using PyInstaller.

# --- Prerequisites ---
# If you need to install PyInstaller, use: pip3 install pyinstaller

# --- Configuration ---
SPEC_FILE="grade_calculator.spec"
EXE_NAME="GradeCalculator"
BUILD_FOLDER="build/${SPEC_FILE%.*}" # e.g., build/grade_calculator

# --- Clean up previous builds ---
echo "Cleaning up previous build directories..."
rm -rf build
rm -rf dist
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# --- 1. Run PyInstaller to build the components ---
echo "Starting PyInstaller build..."
# We run without --onefile flag here, as it's defined in the spec file
pyinstaller "$SPEC_FILE"

# --- 2. Check Build Success and Copy Executable ---

if [ -f "$BUILD_FOLDER/$EXE_NAME" ]; then
    echo "PyInstaller build successful. Copying executable..."
    mkdir -p dist
    
    # Check if running on Windows (for .exe naming)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows executable
        cp "$BUILD_FOLDER/$EXE_NAME" "dist/${EXE_NAME}.exe"
        FINAL_EXE="dist/${EXE_NAME}.exe"
    else
        # macOS/Linux executable
        cp "$BUILD_FOLDER/$EXE_NAME" "dist/$EXE_NAME"
        FINAL_EXE="dist/$EXE_NAME"
    fi

    # Ensure the executable has correct permissions (critical for macOS/Linux)
    chmod +x "$FINAL_EXE"

    # --- 3. Post-Build Information ---
    echo "================================================="
    echo "✅ Final executable successfully created!"
    echo "Location: $FINAL_EXE"
    echo "================================================="
    
    # Automatically run the executable for testing (optional)
    echo "Attempting to run the executable now:"
    "$FINAL_EXE"
else
    echo "❌ Build failed. Executable not found in $BUILD_FOLDER."
    echo "Please inspect the PyInstaller output above for errors."
fi