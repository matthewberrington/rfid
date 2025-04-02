::if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*)
py -m venv .venv_rfid
.venv_rfid\Scripts\python.exe -m pip install --upgrade pip'
.venv_rfid\Scripts\pip.exe install -e .
pause