# Not a Culture Fit — GUI

Tkinter-based GUI for the absurd AI interviewer (Ollama).

## Dev
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install requests

# run
python .\src\nacf_ui.py
```

## Build EXE
```powershell
# from repo root
.\build_gui.ps1
# => dist\NotACultureFitGUI.exe
```

## Model/Server
- Default model: `llama3` (env `NACF_MODEL`)
- Default URL: `http://localhost:11434` (env `OLLAMA_URL`)
Update the fields at the top of the UI to change at runtime.
