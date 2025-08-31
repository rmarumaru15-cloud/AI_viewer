@echo off
rem Change current directory to the script's directory to ensure paths are correct
cd /d %~dp0

echo.
echo [INFO] AI Voice Chat - DEBUG Executable Builder
echo.
echo [INFO] This script will build a DEBUG version of the .exe.
echo [INFO] A console window will be shown for debugging purposes.
echo.

rem Check if pyinstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller is not installed or not found in PATH.
    echo [INFO] Please install it by running: pip install pyinstaller
    exit /b 1
)

echo [INFO] Starting DEBUG build process...
rem We run without the --windowed flag to keep the console open for debugging
pyinstaller --noconfirm --onefile --icon="NONE" main.py

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Build completed successfully!
    echo [INFO] You can find the debug executable at: dist/main.exe
    echo.
) else (
    echo.
    echo [ERROR] Build failed. Please check the output above for errors.
    echo.
)

pause
