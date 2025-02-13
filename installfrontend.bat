set "repoDir=%UserProfile%\Documents\installdeapLite\deapLite"
set "backendDir=%repoDir%\backend"
set "n8nDir=%UserProfile%\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-editor-ui\dist
set "n8nDirStatic=%UserProfile%\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-editor-ui\dist\static
set "n8nDirAssets=%UserProfile%\AppData\Roaming\npm\node_modules\n8n\node_modules\n8n-editor-ui\dist\assets
copy .env.example .env 
cmd /c npm install 
cmd /c npm run build 
cmd /c npm install n8n -g
copy DEAP.ico %backendDir%\favicon.ico
copy DEAP.png %backendDirStatic%\n8n-logo.png
copy Logo-vj6e7OLa.js %backendDirAssets%
copy index-DablXALM.js %backendDirAssets%
cd %backendDir%
pip install -U virtualenv
python -m virtualenv venv 
copy .\venv\Scripts\activate.bat .\venv\Scripts\activate2.bat
copy .\venv\Scripts\activate.bat .\venv\Scripts\activate3.bat
copy .\venv\Scripts\activate.bat .\venv\Scripts\activate_ssl.bat
echo .\start_windows.bat >> .\venv\Scripts\activate3.bat
echo pip install -r requirements.txt -U >>  .\venv\Scripts\activate2.bat
echo mkdir data >> .\venv\Scripts\activate2.bat
echo .\execN8n.bat >> .\venv\Scripts\activate_ssl.bat
.\venv\Scripts\activate2.bat
