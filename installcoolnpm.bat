cd open-webui
copy .env.example .env
npm install
npm run build
cd .\backend
pip install -U virtualenv
python -m virtualenv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt -U
mkdir data
.\start_windows.bat
