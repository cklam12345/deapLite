set "repoDir=%UserProfile%\Documents\installcool\hpcooltoo4"
set "backendDir=%repoDir%\backend"
copy .env.example .env 
cmd /c npm install 
cmd /c npm run build 
cmd /c npm install n8n -g
cd %backendDir%
pip install -U virtualenv
python -m virtualenv venv 
copy .\venv\Scripts\activate.bat .\venv\Scripts\activate2.bat
copy .\venv\Scripts\activate.bat .\venv\Scripts\activate3.bat
copy .\venv\Scripts\activate.bat .\venv\Scripts\activate_ssl.bat
echo .\start_windows.bat >> .\venv\Scripts\activate3.bat
echo .\start_windows_ssl.bat >> .\venv\Scripts\activate_ssl.bat
echo pip install -r requirements.txt -U >>  .\venv\Scripts\activate2.bat
echo mkdir data >> .\venv\Scripts\activate2.bat
.\venv\Scripts\activate2.bat
