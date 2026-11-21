# Stage 9 – Library and search

## What was done
- `views/library.py`: a 3-column grid of memory cards (photo, title, status, date, place) with an Open button.
- Search matches every typed word across title, location, people, occasion, description and story.
- A filter shows All, Mine, Shared with me, or Drafts.
- `views/memory.py` shows one memory in full, and lets you continue a draft.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the library, search and memory page | _Fill in: tested searches like "grandma beach"_ |

## Technical terms
- **Signed URL**: a temporary link to a private file (it expires after 1 hour).
- **Filter**: keeping only the items that match a condition.
- **Case-insensitive search**: "Beach" matches "beach".

## Problem and fix
Photos are private, so a normal link doesn't work. Fix: `signed_url()` creates a 1-hour link for each photo.

## Change from plan
Search runs in Python over the user's memories instead of in SQL. That's simpler, and fast enough for family-sized libraries.

## Screenshots
1. The library grid.
2. A search with results.
3. A search with no results.
