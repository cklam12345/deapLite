@echo off
setlocal

:: Define variables
set "repoURL=https://github.com/cklam12345/hpcooltoo4.git"
set "repoDir=%~dp0hpcooltoo4"
set "backendDir=%repoDir%\backend"
set "shortcutName=hpcooltoo4"
set "shortcutName2=startcool"
set "shortcutPath=%USERPROFILE%\Desktop\%shortcutName%.lnk"
set "shortcutPath2=%USERPROFILE%\Desktop\%shortcutName2%.lnk"
set "installNodePath=%repoDir%\node-v22.12.0-x64.msi"
set "installPythonPath=%repoDir%\python-3.11.0-amd64.exe"
set "installFrontend=%repoDir%\installfrontend.bat"
set "installollama=%repoDir%\installollama.exe"
set "installcplusplus=%repoDir%\vs_BuildTools.exe"
set "targetPath=.\runfrontend_ssl.bat"

set "iconPath=%repoDir%\hpcooltoo4.ico"
set "iconPath2=%repoDir%\hp.ico"


:: Clone the repository
echo Cloning repository...
git clone %repoURL% %repoDir%

:: Navigate to the repository directory
cd %repoDir%
echo install python
%installPythonPath%

echo install node
%installNodePath%

echo install c plus plus
%installcplusplus%

echo install ollama
type ollama.aa ollama.ab ollama.ac ollama.ad ollama.ae ollama.af ollama.ag ollama.ah > installollama.exe
%installollama%
echo install base model
cmd /c ollama pull llama3.2
echo install embedding rag model
cmd /c ollama pull nomic-embed-text
echo install retail agent model
cmd /c ollama create retail_agent -f .\model.retail
echo install home depot agent model
cmd /c ollama create homedepot_agent -f .\model.homedepot

:: Create the shortcut
echo Creating desktop shortcut...
powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%shortcutPath%'); $s.WorkingDirectory = '%repoDir%'; $s.TargetPath = 'cmd.exe'; $s.Arguments = '/c cd /d %repoDir% && %targetPath% '; $s.IconLocation = '%iconPath%'; $s.Save()"
echo Installation complete. Shortcut created on Desktop.

:: Create the shortcut
echo Creating desktop start server shortcut...
powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%shortcutPath2%'); $s.WorkingDirectory = '%repoDir%'; $s.TargetPath = 'cmd.exe'; $s.Arguments = '/c cd /d %repoDir% && %installFrontend% '; $s.IconLocation = '%iconPath2%'; $s.Save()"
echo Installation complete. Shortcut created on Desktop.

:: Reboot the machine
echo Rebooting the machine...
echo shutdown /r /t 0

endlocal
