@echo off

echo ============================================
echo Building NeuroAdaptiveBackend.exe
echo ============================================

python -m pip install pyinstaller

python -m PyInstaller --noconfirm --clean --onefile --name NeuroAdaptiveBackend ^
--hidden-import=uvicorn.logging ^
--hidden-import=uvicorn.loops.auto ^
--hidden-import=uvicorn.protocols.http.auto ^
--hidden-import=uvicorn.protocols.websockets.auto ^
run_backend.py

echo.
echo ============================================
echo Build complete.
echo ============================================
echo.
echo The executable should be located at:
echo dist\NeuroAdaptiveBackend.exe
echo.
pause