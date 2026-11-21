# Story-scape

Families upload a photo, tell the story behind it, and get an AI four-panel comic.
MYP Year 5 Design, Criterion C product. Built with AI assistance (see `/journal`).

## Supabase setup
1. Create a project at supabase.com.
2. In SQL Editor, run `supabase/schema.sql` first, then `supabase/policies.sql`.
3. Copy the Project URL and anon key from Settings → API into `.env`.

## Tests
`python -m pytest tests`

## Run locally
```
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # then fill in real keys
streamlit run app.py
```
