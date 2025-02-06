set "repoDir=%UserProfile%\Documents\installcool\hpcooltoo4"
set "backendDir=%repoDir%\backend"
cd %backendDir%
.\venv\Scripts\activate_ssl.bat 
.\start_windows_ssl.bat
