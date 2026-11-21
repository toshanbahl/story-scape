# Stage 3 – Log in, sign up, log out

## What was done
- `views/auth.py`: Log in and Sign up tabs using **Supabase Auth**. Sign-up checks for a name, a valid email and a password of at least 8 characters.
- `app.py`: a login gate. Logged-out users see only the login page. "Log out" signs out and clears `st.session_state`.
- `core/db.py`: one Supabase client per browser session, so two people logged in at once never share a login.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the auth page, the login gate and the client helper | _Fill in: created test accounts, tested wrong passwords, confirmed emails_ |

## Technical terms
- **Authentication**: proving who you are (email and password).
- **Session state**: Streamlit's memory for one browser tab across reruns.
- **JWT (access token)**: the signed ticket Supabase gives after login; it's sent with every request.
- **Validation**: checking input before using it.

## Problem and fix
If one Supabase client were shared by everyone, user A's login would apply to user B. Fix: store the client in `st.session_state`, which gives one client per browser session.

## Change from plan
None.

## Screenshots
1. Sign-up success message.
2. Wrong-password error.
3. The Authentication > Users list in Supabase showing the test account.
