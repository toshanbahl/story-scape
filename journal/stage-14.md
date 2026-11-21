# Stage 14 – Deployment

## What was done
- The app is ready for **Streamlit Community Cloud**: `requirements.txt` and `.streamlit/config.toml` are in place, and `get_secret()` reads keys from `st.secrets` when the app is online.
- **Not yet deployed.** Deploying needs your own GitHub and Streamlit accounts.

## Steps (yours to do)
1. Create a GitHub repo, then run `git init`, `git add .`, `git commit -m "Story-scape"` and `git push`. Check first that `.env` is NOT in `git status`.
2. On share.streamlit.io: New app → pick the repo → main file `app.py` → Python 3.13 (Advanced settings).
3. Advanced settings → Secrets, then paste:
   ```
   SUPABASE_URL = "..."
   SUPABASE_ANON_KEY = "..."
   OPENAI_API_KEY = "..."
   ```
4. In Supabase, go to Authentication → URL Configuration and add the app's URL as the Site URL.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Prepared the config and wrote these steps | _Fill in: did the deployment, fixed any errors_ |

## Technical terms
- **Deployment**: putting the app online so others can use it.
- **Secrets manager**: a safe place for keys on the hosting service.
- **Repository (repo)**: a project folder tracked by Git.

## Problem and fix
_Fill in a real one from deploying._

## Change from plan
None.

## Screenshots
1. The GitHub repo, with no `.env` file.
2. The Streamlit Cloud deploy log.
3. The live URL working on a phone.
