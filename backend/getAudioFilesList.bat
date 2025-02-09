@echo off
setlocal

:: Define variables
set "wav2opus=%USERPROFILE%\wave1.0\python"

cd %wav2opus%
del  wavefileslist.txt
del diarizedwavefileslist.txt
echo " " > wavefileslist.txt
echo " " > diarizedwavefileslist.txt
for %%a in (.\records\*.wav) do (echo %%~fa >> wavefileslist.txt)
for %%a in (.\records\*.wav_diarized.txt) do (echo %%~fa >> diarizedwavefileslist.txt)
set "infile=diarizedwavefileslist.txt"
set "outfile=removed_diarizedwavefileslist.txt"

(
  for /f "usebackq delims=" %%a in ("%infile%") do (
    set "line=%%a"
    setlocal enabledelayedexpansion
    set "newline=!line:_diarized.txt=!"
    echo !newline!
    endlocal
  )
) > "%outfile%"

fc wavefileslist.txt removed_diarizedwavefileslist.txt /n > temp.txt

findstr /v /c:"*****" temp.txt | findstr /v /c:"---" > diff.txt

del temp.txt

@echo off
for /f "usebackq tokens=2 delims= " %%a in ("diff.txt") do (echo %%a | findstr /v /c:"files")