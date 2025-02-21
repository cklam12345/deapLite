@echo off
setlocal enabledelayedexpansion

set "file=%1"

if "%file%"=="" (
  echo "Error: Input file not specified."
  exit /b 1
)

if not exist "%file%" (
  echo "Error: Input file '%file%' not found."
  exit /b 1
)

set "outfile=output.csv"

echo speaker,content,"time start","time stop" > "%outfile%"

for /f "tokens=1-4 delims=()" %%a in (%file%) do (
  set "speaker=%%a"
  set "rest=%%b"

  for /f "tokens=1-3 delims=^|" %%c in ("!rest!") do (  REM Escape the pipe!
    set "content=%%c"
    set "times=%%d"

    for /f "tokens=1-2 delims=- " %%e in ("!times!") do (
        set "start_time=%%e"
        set "end_time=%%f"

        echo "!speaker!","!content!","!start_time!","!end_time!" >> "%outfile%"
    )
  )
)


echo "CSV file '%outfile%' created successfully."

endlocal