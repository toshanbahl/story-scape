# Stage 4 – Theme and navbar

## What was done
- `.streamlit/config.toml` sets the theme: orange #E8651A, cream #FDF8F3, dark text #2C1A0E, 16px font, 8px radius.
- `core/theme.py` adds CSS for 44px buttons and inputs, orange primary buttons and a visible focus ring.
- `app.py` puts a top navbar on every page: Home, Add Memory, Library, Memory, Log out.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the config, CSS and navbar | _Fill in: checked colours against my design spec (Criterion B), any tweaks I made_ |

## Technical terms
- **CSS**: rules that control how a web page looks.
- **Theme config**: Streamlit's built-in settings for colours and fonts.
- **st.navigation**: Streamlit's function for building a multi-page menu.

## Problem and fix
Pages needed to jump to each other, e.g. the Home button opening Add Memory, but `st.switch_page` needs the page object. Fix: `app.py` stores all pages in `st.session_state.pages`.

## Change from plan
None.

## Screenshots
1. The navbar on the Home page.
2. Browser dev tools showing a button height of 44px or more.
