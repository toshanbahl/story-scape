# Stage 5 – Home page

## What was done
`views/home.py` shows:
- a greeting with the user's name;
- three counts: my memories, drafts, and memories shared with me;
- an "Add a new memory" button;
- the 10 most recent activity entries.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the page | _Fill in: tested with 0 and several memories_ |

## Technical terms
- **Query**: a request for rows from the database.
- **st.metric**: a Streamlit widget that shows a big number with a label.

## Problem and fix
A brand-new user has no activity, which would leave the section blank. Fix: show a friendly "Nothing yet" message instead.

## Change from plan
None.

## Screenshots
1. Home page for a new user.
2. Home page after adding memories.
