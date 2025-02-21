@echo off
setlocal

:: Get the process ID (PID) of the Python process running wave2opus.py
for /f "tokens=2 delims==" %%i in ('wmic process where "caption='python.exe' and commandline like '%%python%%wave2opus.py%%'" get processid /format:value') do (
    set PID=%%i
)

:: Check if PID is found
if "%PID%"=="" (
    echo No python app.py process found.
) else (
    :: Kill the specific python process
    taskkill /PID %PID% /F
    echo Process with PID %PID% has been terminated.
)

endlocal