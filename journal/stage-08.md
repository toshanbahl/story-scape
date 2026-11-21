# Stage 8 – Comic viewer and approval

## What was done
- **Step 4** shows the comic with three choices: Approve and save, Try again, or Edit story.
- Before Approve, the comic exists only in `st.session_state`, nothing is uploaded or inserted.
- **Approve** uploads the PNG, writes the story, marks the memory `complete`, inserts a `comics` row, logs the activity and opens the Memory page.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the viewer and the approve logic | _Fill in: checked that "Try again" left nothing in Supabase_ |

## Technical terms
- **Approval gate**: a step that blocks saving until a person says yes.
- **In-memory**: data held only while the app runs, and lost if not saved.

## Problem and fix
If a user approved, then somehow submitted a different story, it would overwrite the original. Fix: the database trigger from Stage 2 rejects any change to an existing story.

## Change from plan
None.

## Screenshots
1. The comic viewer with the "NOT saved yet" notice.
2. The `comics` table empty before Approve and with one row after.
