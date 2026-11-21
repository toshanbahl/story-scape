# Stage 10 – Family sharing and permissions

## What was done
- On the Memory page, the owner shares by email with **view** or **edit** permission, and can remove access.
- Sharing sets the memory's `visibility` to `family`. Removing the last person sets it back to `private`.
- "Edit" members can change the details, but never the photo or the story.
- Every share and unshare is logged in `activity`.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the sharing UI and edit form | _Fill in: tested with two accounts in two browsers_ |

## Technical terms
- **Permission level**: what someone is allowed to do (view or edit).
- **Private by default**: nothing is shared until the owner chooses to share it.
- **Join**: reading related rows from two tables at once (`permissions` + `users`).

## Problem and fix
Changing someone from view to edit hit a "duplicate" error. Fix: use an **upsert** on `(memory_id, grantee_id)` and add an update policy in Stage 11.

## Change from plan
Added the "Edit details" form so the edit permission actually does something.

## Screenshots
1. The share form.
2. A second account seeing the shared memory.
3. A third account NOT seeing it.
