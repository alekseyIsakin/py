cd ..
set py=%cd%"\env\Scripts\python.exe" 
call "%cd%\env\Scripts\activate.bat"

%py% --version

cd "project"

py -m pdb "%~dp0src/main.py"