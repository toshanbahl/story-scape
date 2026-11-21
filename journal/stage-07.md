# Stage 7 – Story, voice and AI comic

## What was done
- **Step 3:** type the story, or record it with `st.audio_input`. `core/voice.py` turns speech into text using SpeechRecognition (Google's free recogniser), and the text is added to the story box.
- `core/comic.py`:
  - GPT-4o writes four captions, returned as JSON.
  - 30-second **timeout**, then **one retry**, then a friendly error message.
  - Pillow builds a 2×2 comic. Each panel frames the photo differently (whole, left, close-up, right) with a posterised "comic" look and a caption strip.
- A spinner shows while it works.

## AI's role vs mine
| AI (Claude) | Me |
|---|---|
| Wrote the prompt, retry logic, comic layout and voice code | _Fill in: tested real stories, judged caption quality, adjusted the prompt?_ |

## Technical terms
- **API**: a way for one program to use another's service (here OpenAI).
- **Prompt**: the instructions sent to the AI.
- **JSON**: a text format for structured data.
- **Timeout**: the maximum wait before giving up.
- **Retry**: trying again automatically after a failure.
- **Speech-to-text**: converting spoken audio into written words.
- **Posterize**: reducing the number of colours for a flat, cartoon look.

## Problem and fix
The AI sometimes replies in the wrong format. Fix: `parse_captions` checks that there are exactly four non-empty captions. A bad reply counts as a failure, so it gets the one retry.

## Change from plan
- **Groq (free) with the `openai/gpt-oss-120b` model instead of OpenAI GPT-4o for captions.** GPT-4o costs money; Groq is free, fast, and doesn't train on user data. Groq offers an OpenAI-compatible API, so the same `openai` library works; only the base URL and model name change, and both are set in `.env` (`OPENAI_BASE_URL`, `AI_MODEL`). I first tried Qwen, then Llama, but Groq no longer offered Llama models (404 "model does not exist"), so I listed the available models and chose gpt-oss-120b. Switching back to GPT-4o needs no code change.
- Problem found while testing: `.env` lost its `OPENAI_BASE_URL` line, so the Groq key was sent to OpenAI and rejected ("AuthenticationError"). Fix: add the base URL and model lines back.
- The comic panels are styled crops of the user's own photo, made with Pillow, not AI-generated drawings. The stack lists GPT-4o for captions only, and this keeps the original photo's faces real.
- The story is saved at Approve (Stage 8), not at this step. That way, editing the story before approving never counts as "overwriting" it.

## Screenshots
1. The voice recording transcribed into the box.
2. The spinner.
3. The error message (test by putting a wrong `OPENAI_API_KEY` in `.env`).
