@echo off
setlocal

:: Define variables
set "wav2beetle=%USERPROFILE%\wave1.0\soundskrit"

echo wave2beetle
cd %wav2beetle%
python beetle2wav_v2.py --no-doa