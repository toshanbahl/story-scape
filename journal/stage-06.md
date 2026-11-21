# Stage 6 – Add Memory steps 1–2

## What was done
`views/add_memory.py`:
- **Step 1, photo:** JPG or PNG only, max 10 MB, checked with Pillow so files that only pretend to be images are rejected.
- **Step 2, details:** six fields (title required, date, location, people, occasion, description).
- "Save draft" uploads the photo to `<user>/<memory>/original.jpg` and inserts a memory with `status = 'draft'`.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote both steps | _Fill in: tested a 12 MB file, a renamed .txt, an empty title_ |

## Technical terms
- **File uploader**: a widget for choosing a file from your computer.
- **Draft**: a saved but unfinished memory.
- **Upsert**: insert, or replace if the file already exists. It's left OFF so an original is never replaced.
- **Progress bar**: shows which step of 4 you're on.

## Problem and fix
A file renamed to `.jpg` would pass the type filter. Fix: `Image.open().verify()` checks the actual file contents.

## Change from plan
None.

## Screenshots
1. Step 1 with a preview.
2. The "too big" error.
3. The draft row in the Supabase `memories` table.
4. The file in the Storage bucket.
