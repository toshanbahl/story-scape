# Stage 11 – Security (RLS)

## What was done
`supabase/policies.sql` turns on **Row Level Security** for all five tables and the photos bucket:
- You see a memory only if you own it or it was shared with you (`can_view`).
- Only the owner can create comics, share, or delete.
- You can upload files only into your own folder. There is no storage update policy, so files can never be overwritten.
- Activity logs are private to each user.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote all the policies and helper functions | _Fill in: ran the policies and tried to read another user's memory_ |

## Technical terms
- **RLS (Row Level Security)**: the database checks every row against rules before returning it.
- **Policy**: one RLS rule, e.g. "you can read a memory only if...".
- **auth.uid()**: the ID of the logged-in user making the request.
- **security definer**: a function that runs with its creator's rights, used here to avoid policy loops.
- **Anon key**: the public key; it's safe in the app *because* RLS protects the data.

## Problem and fix
1. The memories policy checks `permissions`, and the permissions policy checks `memories`. That's an infinite loop. Fix: the `security definer` helper functions `can_view` and `is_owner`.
2. Found while reviewing: an "edit" member could have changed `owner_id` to themselves and taken over a memory. Fix: the `protect_originals` trigger now also blocks owner changes.

## Change from plan
None.

## Screenshots
1. Authentication > Policies showing RLS enabled on every table.
2. A logged-in second user getting no rows for someone else's private memory.
