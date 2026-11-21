"""Add Memory wizard.
Steps 1-2 (Stage 6): photo + six details, saved as a DRAFT.
Step 3 (Stage 7): story by text or voice, then generate the AI comic.
Step 4 (Stage 8): view the comic; NOTHING about the comic is saved until Approve.
"""
import io
import uuid

import streamlit as st
from openai import OpenAI
from PIL import Image

from core.comic import ComicError, build_comic, generate_captions
from core.db import current_user, get_client, get_secret, log_activity
from core.voice import transcribe

MAX_MB = 10


def show():
    st.title("Add a memory")
    step = st.session_state.get("step", 1)
    st.progress(step / 4, text=f"Step {step} of 4")
    [None, step_photo, step_details, step_story, step_review][step]()


# ---------- Step 1: photo ----------
def step_photo():
    file = st.file_uploader("Choose a photo (JPG or PNG, max 10 MB)", type=["jpg", "jpeg", "png"])
    if file is None:
        return
    data = file.getvalue()
    if len(data) > MAX_MB * 1024 * 1024:
        st.error("That photo is too big. Please choose one under 10 MB.")
        return
    try:
        Image.open(io.BytesIO(data)).verify()  # rejects files that only pretend to be images
    except Exception:
        st.error("That file isn't a valid image.")
        return
    st.image(data, caption="Your photo", width=400)
    if st.button("Next: add details", type="primary"):
        st.session_state.photo = {"bytes": data, "ext": file.name.rsplit(".", 1)[-1].lower(), "type": file.type}
        st.session_state.step = 2
        st.rerun()


# ---------- Step 2: six details, saved as draft ----------
def step_details():
    with st.form("details"):
        title = st.text_input("Title *", max_chars=100)
        memory_date = st.date_input("Date", value=None)
        location = st.text_input("Location", max_chars=100)
        people = st.text_input("People in the photo", max_chars=200)
        occasion = st.text_input("Occasion", max_chars=100)
        description = st.text_area("Short description", max_chars=300)
        saved = st.form_submit_button("Save draft and continue")
    if st.button("← Back"):
        st.session_state.step = 1
        st.rerun()
    if not saved:
        return
    if not title.strip():
        st.error("Please give your memory a title.")
        return

    sb, user = get_client(), current_user()
    memory_id = str(uuid.uuid4())
    photo = st.session_state.photo
    path = f"{user.id}/{memory_id}/original.{photo['ext']}"
    try:
        # upsert is off by default, so the original photo can never be replaced
        sb.storage.from_("photos").upload(path, photo["bytes"], {"content-type": photo["type"]})
        sb.table("memories").insert({
            "id": memory_id, "owner_id": user.id, "photo_path": path, "title": title.strip(),
            "memory_date": memory_date.isoformat() if memory_date else None,
            "location": location, "people": people, "occasion": occasion, "description": description,
        }).execute()
    except Exception as e:
        st.error(f"Could not save the draft: {e}")
        return
    log_activity(f"Saved draft '{title.strip()}'", memory_id)
    st.session_state.memory_id = memory_id
    st.session_state.step = 3
    st.rerun()


# ---------- Step 3: story (text or voice) + generate ----------
def step_story():
    memory = load_memory()
    st.subheader(memory["title"])
    st.write("Tell the story behind this photo. Type it, or record your voice.")

    audio = st.audio_input("Record your story")
    if audio and st.session_state.get("last_audio") != audio.file_id:
        st.session_state.last_audio = audio.file_id
        with st.spinner("Turning your voice into text..."):
            text, error = transcribe(audio.getvalue())
        if error:
            st.error(error)
        else:
            st.session_state.story_box = (st.session_state.get("story_box", "") + " " + text).strip()

    story = st.text_area("Your story", key="story_box", height=200, max_chars=3000)

    if st.button("✨ Create my comic", type="primary"):
        if len(story.strip()) < 20:
            st.error("Please write a little more (at least 20 characters) so the comic makes sense.")
            return
        details = {k: memory[k] for k in ("title", "memory_date", "location", "people", "occasion", "description")}
        try:
            with st.spinner("Creating your comic... this can take up to a minute"):
                # Any OpenAI-compatible service works (OpenAI, Qwen...): set base URL and model in .env
                ai = OpenAI(api_key=get_secret("OPENAI_API_KEY"), base_url=get_secret("OPENAI_BASE_URL"))
                captions = generate_captions(ai, story, details, get_secret("AI_MODEL") or "gpt-4o")
                photo_bytes = get_client().storage.from_("photos").download(memory["photo_path"])
                comic_png = build_comic(photo_bytes, captions)
        except ComicError as e:
            st.error(str(e))
            return
        # Held in memory only. Not saved anywhere until the user approves.
        st.session_state.pending = {"story": story.strip(), "captions": captions, "png": comic_png}
        st.session_state.step = 4
        st.rerun()


# ---------- Step 4: comic viewer + approval ----------
def step_review():
    pending = st.session_state.pending
    st.image(pending["png"], caption="Comic: " + " / ".join(pending["captions"]), use_container_width=True)
    st.info("This comic is NOT saved yet. Approve it to keep it, or try again.")

    c1, c2, c3 = st.columns(3)
    if c1.button("✅ Approve and save", type="primary"):
        approve(pending)
    if c2.button("🔄 Try again"):
        st.session_state.step = 3
        del st.session_state.pending
        st.rerun()
    if c3.button("✏️ Edit story"):
        st.session_state.step = 3
        st.rerun()


def approve(pending):
    sb, user = get_client(), current_user()
    memory_id = st.session_state.memory_id
    comic_path = f"{user.id}/{memory_id}/comic-{uuid.uuid4().hex[:8]}.png"
    try:
        sb.storage.from_("photos").upload(comic_path, pending["png"], {"content-type": "image/png"})
        # Story is written once, here. A database trigger blocks any later overwrite.
        sb.table("memories").update({"story": pending["story"], "status": "complete"}).eq("id", memory_id).execute()
        sb.table("comics").insert({
            "memory_id": memory_id, "owner_id": user.id, "image_path": comic_path, "captions": pending["captions"],
        }).execute()
    except Exception as e:
        st.error(f"Could not save: {e}")
        return
    log_activity("Approved a comic", memory_id)
    for key in ("step", "photo", "pending", "story_box", "last_audio"):
        st.session_state.pop(key, None)
    st.session_state.open_memory = memory_id
    st.switch_page(st.session_state.pages["memory"])


def load_memory():
    return get_client().table("memories").select("*").eq("id", st.session_state.memory_id).single().execute().data


def resume_draft(memory_id):
    """Called from the Memory page to finish a draft that was left at step 3."""
    st.session_state.memory_id = memory_id
    st.session_state.step = 3
    st.switch_page(st.session_state.pages["add"])
