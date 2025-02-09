@echo off
setlocal

:: Define variables
set "wav2opus=%USERPROFILE%\wave1.0\python"

echo wave2opus
cd %wav2opus%
python wave2opus.py