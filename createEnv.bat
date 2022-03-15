set py="C:\Users\Alex\AppData\Local\Programs\Python\Python39\python.exe" 

%py% --version

if not exist env (
  %py% -m venv env
  
  call "%~dp0env\Scripts\activate.bat"

  pip install opencv-python
  pip install numpy
  pip install pandas
  pip install matplotlib
)
