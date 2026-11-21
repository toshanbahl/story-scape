# Stage 2 – Supabase setup

## What was done
- `supabase/schema.sql` creates five tables: **users**, **memories**, **comics**, **permissions**, **activity**, plus a private **storage bucket** called `photos`.
- A **trigger** creates a `users` profile row automatically on sign-up.
- A second trigger, `protect_originals`, blocks any change to a memory's photo or owner, and blocks overwriting a story once it is written.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Designed the tables and wrote all the SQL | _Fill in: created the Supabase project, ran the SQL, checked the tables in Table Editor_ |

## Technical terms
- **Postgres**: the database Supabase runs on.
- **Primary key**: a column that uniquely identifies each row (here a **UUID**).
- **Foreign key**: a column that points to a row in another table, e.g. `memories.owner_id → users.id`.
- **Trigger**: code the database runs automatically when a row is inserted or updated.
- **Check constraint**: a rule that limits allowed values, e.g. `status` must be `draft` or `complete`.
- **Storage bucket**: a folder in the cloud for files; `public = false` means private.

## Problem and fix
The plan's "Original photo and story must never be overwritten" can't rely on the app alone, because a bug or a direct API call could bypass it. Fix: the `protect_originals` trigger enforces it inside the database.

## Change from plan
Added the six detail fields as columns: title, date, location, people, occasion, description.

## Screenshots
1. SQL Editor showing "Success. No rows returned".
2. Table Editor listing the five tables.
3. Storage showing the private `photos` bucket.
