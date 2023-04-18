@echo off
echo.
echo ***********************
echo INSTALLING DEPENDENCIES
echo ***********************
pip install -r requirements.txt
echo.
echo ***********************
echo BUILDING API CLIENT CLI
echo ***********************
pyinstaller main.spec
echo.
echo **************
echo BUILD COMPLETE
echo **************
echo. 
start /d .\dist main.exe
echo Press enter to exit
set /p input=