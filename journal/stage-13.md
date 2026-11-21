# Stage 13 – Testing

## What was done
`tests/test_core.py` has 6 automated tests:
- Captions parse correctly, and bad AI replies are rejected.
- Retry: one failure then success returns the captions.
- Two failures give a friendly error, and there is never a third attempt.
- The comic is a PNG, and the original photo bytes are unchanged.
- Search matches multiple words and handles an empty query.

**Result (run by the AI, 2026-11-19): 6 passed.** A headless run of `app.py` showed the login page with no errors.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote and ran the automated tests | _Fill in: the manual test table below, run against the real Supabase and OpenAI_ |

## Manual tests to run (fill in the results)
| # | Test | Expected | Result |
|---|---|---|---|
| 1 | Sign up, then log in | Home page appears | |
| 2 | Upload an 11 MB photo | "too big" error | |
| 3 | Save a draft, close the tab, reopen it from Library | Draft can be continued | |
| 4 | Record a voice story | Text appears in the box | |
| 5 | Generate, then "Try again" | Nothing in the `comics` table | |
| 6 | Approve | Comic saved, memory complete | |
| 7 | User B opens user A's private memory | No access | |
| 8 | Share with B (view) | B sees it, can't edit | |
| 9 | Wrong OpenAI key | Friendly error after 2 tries | |

## Technical terms
- **Unit test**: an automatic check of one small piece of code.
- **Mock / fake**: a pretend version of a service, so tests don't need the internet.
- **pytest**: a Python tool that finds and runs tests.

## Problem and fix
Creating the virtual environment inside the project folder failed (pip install error, probably because the Windows path was too long). Fix: create the venv in a shorter path.

## Screenshots
1. Terminal showing `6 passed`.
2. The filled-in manual test table.
