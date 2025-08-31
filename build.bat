@echo off
rem Change current directory to the script's directory to ensure paths are correct
cd /d %~dp0

echo.
echo [INFO] AI Voice Chat - Executable Builder
echo.
echo [INFO] This script will bundle the Python application into a single .exe file.
echo [INFO] The final executable will be located in the 'dist' directory.
echo [INFO] IMPORTANT: 'characters.json' and '.env' must be in the same directory as the final .exe
echo.

rem Check if pyinstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller is not installed or not found in PATH.
    echo [INFO] Please install it by running: pip install pyinstaller
    exit /b 1
)

echo [INFO] Starting build process...
pyinstaller --noconfirm --onefile --windowed --icon="NONE" main.py

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Build completed successfully!
    echo [INFO] You can find the executable at: dist/main.exe
    echo.
) else (
    echo.
    echo [ERROR] Build failed. Please check the output above for errors.
    echo.
)

pause
