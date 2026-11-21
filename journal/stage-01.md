# Stage 1 – Project setup

**Date:** 2026-11-19

## What was done
- Created the project structure: `app.py`, `requirements.txt`, `.gitignore`, `.env.example`, `README.md`, `journal/`.
- `app.py` shows a title and a "setup check" that reports whether each API key is present, without displaying the key.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Drafted all Stage 1 files and this journal template | _Fill in: created the venv, installed packages, ran the app, created the GitHub repo, made the first commit_ |
| Suggested the setup-check idea | _Fill in: whether I accepted or changed it, and why_ |

## Technical terms
- **Virtual environment (venv)**: a private folder of Python packages for one project.
- **requirements.txt**: the list of libraries `pip` installs.
- **Environment variable**: a value the program reads from the system instead of hard-coding it.
- **.env file**: a local file that holds secret keys, loaded by **python-dotenv**.
- **.gitignore**: tells Git which files never to track, such as `.env`.
- **Streamlit**: a Python library that turns a script into a web app.

## Problem and fix
_Fill in a real problem you hit. If none came up, write "none", don't invent one. Common example: `streamlit` not recognised because the venv wasn't activated; fix: run `.venv\Scripts\activate`._

## Change from plan
- **Python 3.13 instead of 3.11.** 3.13 was already installed, and all the tests passed on it. The newest version (3.15) was avoided because new releases often lack support from libraries like Pillow, and Streamlit Cloud may not offer it yet.
- Added a setup check to `app.py`. It wasn't in the plan, but it makes Stage 2 easier to verify.

## Screenshots for evidence
1. Terminal: `pip install -r requirements.txt` finishing successfully.
2. Browser: the app running at `localhost:8501` with the setup check.
3. `git status` showing `.env` is **not** listed (proves secrets are ignored).
4. GitHub repo page after the first commit.
