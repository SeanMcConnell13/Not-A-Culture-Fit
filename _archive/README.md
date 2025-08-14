# Not a Culture Fit

Tiny, unhinged AI interviewer powered by **Ollama**. Asks 10 absurd questions, critiques your answers with corporate-feral energy, then rejects you for a reason that would make HR blush.

## Project layout

```
not-a-culture-fit/
  ├─ src/
  │   └─ not_a_culture_fit.py
  ├─ requirements.txt
  ├─ build.ps1
  ├─ .gitignore
  └─ LICENSE
```

## Dev setup (Windows)

```powershell
# from repo root
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install and start **Ollama**, then pull a model (default is `llama3`):

```powershell
ollama pull llama3
```

Run it:

```powershell
python .\src\not_a_culture_fit.py
```

Optional envs:

```powershell
$env:OLLAMA_URL = "http://localhost:11434"
$env:NACF_MODEL = "llama3"
```

## Build a double-clickable `.exe`

```powershell
# from repo root (venv activated)
.\build.ps1
# output at: dist\NotACultureFit.exe
```

## Git init (first time)

```powershell
git init
git add .
git commit -m "chore: scaffold Not a Culture Fit (Ollama)"
```

## Notes

- Keep answers short; the critiquer replies with 1–3 punchy sentences.
- To tweak tone, edit `build_critique_prompt()` in `src/not_a_culture_fit.py`.
- Change the number of questions by editing `NUM_QUESTIONS_PER_INTERVIEW`.
- If Ollama isn't running, the app will print an error message.
- Want a GUI or icon/version metadata in the EXE? We can add that next.
