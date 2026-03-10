@echo off
echo Building Penina PDF417 Scanner & Encoder Windows Executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller. Please install it manually: python -m pip install pyinstaller
        pause
        exit /b 1
    )
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import PIL, zxingcpp, pylibdmtx, cv2, numpy, treepoem, xml.etree.ElementTree" 2>nul
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install pillow zxing-cpp pylibdmtx opencv-python numpy treepoem
    if %errorlevel% neq 0 (
        echo Failed to install dependencies. Please install them manually.
        echo pip install pillow zxing-cpp pylibdmtx opencv-python numpy treepoem
        pause
        exit /b 1
    )
)

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir "dist"

REM Build the executable
echo Building executable...
python -m PyInstaller penina_app.spec

if %errorlevel% equ 0 (
    echo.
    echo Build completed successfully!
    echo Executable location: dist\penina.exe
    echo.
    echo File size: 
    for %%F in (dist\penina.exe) do echo %%~zF bytes
    echo.
    echo You can now run the application by double-clicking penina.exe.
    echo.
    pause
) else (
    echo.
    echo Build failed! Please check the error messages above.
    echo.
    pause
    exit /b 1
)