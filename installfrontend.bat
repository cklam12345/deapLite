set "repoDir=%UserProfile%\Documents\installdeapLite\deapLite"
set "backendDir=%repoDir%\backend"
copy .env.example .env 
cmd /c npm install 
cmd /c npm run build 
cmd /c npm install n8n
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
echo .\execN8n.bat >> .\venv\Scripts\activate_ssl.bat
.\venv\Scripts\activate2.bat
copy ..\Logo-SPkbfh59.js %UserProfile%\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-editor-ui\dist\assets
