# Not a Culture Fit — Polished GUI (Tkinter)

A clean, professional chat UI with a left-side sprite card and a chat console, powered by **Ollama**.

## Run (Windows)
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
python .\src\nacf_ui_polished.py
```
- Make sure Ollama is running and a model is pulled (`ollama pull llama3`).
- Change model / server at the top bar in the app.

## Assets
- Sprite lives at `assets/manager_sprite.png`. Replace with your own if desired (the app rescales it).

## Packaging (later)
We’ll add a PyInstaller spec that bundles `assets/manager_sprite.png` using `--add-data`:
```
pyinstaller --onefile --windowed --name NotACultureFitGUI ^
  --add-data "assets\manager_sprite.png;assets" ^
  src\nacf_ui_polished.py
```
(But we’ll hold packaging until you approve the UI.)
