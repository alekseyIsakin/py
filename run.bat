set project=%cd%

cd ..
set py=%cd%"\env\Scripts\python.exe" 
call "%cd%\env\Scripts\activate.bat"

%py% --version
echo _
cd %project%

py "%~dp0src/main.py"

pause
