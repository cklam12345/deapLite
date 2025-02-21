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

set "outfile=.\diarized_files\"

copy  "%file%" "%outfile%" >nul 2>&1

for /f %%i in ('dir .\diarized_files /b/a-d/od/t:c') do set LAST=%%i
echo %LAST%


endlocal