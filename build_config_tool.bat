@echo off
echo Building Config Tool...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
pyinstaller config_tool.spec --clean
echo.
echo Build complete! Executable should be in the dist folder.
pause

