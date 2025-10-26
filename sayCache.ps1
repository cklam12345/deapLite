$UserProfile = [Environment]::GetFolderPath("UserProfile")
$InputFile = Join-Path $UserProfile "n8n_tts\input.txt"
$TextToSpeak = Get-Content $InputFile -Raw

# 1. Change to backend directory and activate virtual environment
$BackendPath = Join-Path $UserProfile "Documents\installdeapLite\deapLite\backend"
Set-Location $BackendPath
cmd /c "venv\Scripts\activate.bat"

# 2. Change to TTS script directory
$TTSPath = Join-Path $UserProfile "n8n_tts"
Set-Location $TTSPath


echo "The listening device is leaving session, starting Caching on device" > $InputFile
.\tts_n8n_2.ps1