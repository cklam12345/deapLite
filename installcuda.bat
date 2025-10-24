set "repoDir=%UserProfile%\Documents\installcool\hpcooltoo4"
set "backendDir=%repoDir%\backend"
cd %backendDir%
copy .\venv\Scripts\activate.bat .\venv\Scripts\installcudavenv.bat
echo pip uninstall torch torchaudio >> .\venv\Scripts\installcudavenv.bat
echo pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124 >> .\venv\Scripts\installcudavenv.bat
.\venv\Scripts\installcudavenv.bat
