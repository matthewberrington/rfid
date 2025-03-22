::if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*)
ping -4 -n 1 google.com | find "TTL"
if errorlevel 1 echo "No internet connection. Aborting setup" & pause & exit /B
rmdir /Q/s .\env
py -m venv env
.\env\Scripts\pip.exe install .\keyboard-master\.
.\env\Scripts\pip.exe install install -e .\sllurp\.
pause