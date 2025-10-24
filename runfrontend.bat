set "repoDir=%UserProfile%\Documents\installdeapLite\deapLite"
set "backendDir=%repoDir%\backend"
cd %backendDir%
.\venv\Scripts\activate.bat
exeN8n.bat
execWebui.bat