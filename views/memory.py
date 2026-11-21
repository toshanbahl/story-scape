"""One memory: photo, details, story, approved comics, and family sharing (Stage 10)."""
import streamlit as st

from core.db import current_user, get_client, log_activity, signed_url
from views.add_memory import resume_draft


def show():
    memory_id = st.session_state.get("open_memory")
    if not memory_id:
        st.info("Choose a memory from your Library.")
        return
    sb, user = get_client(), current_user()
    rows = sb.table("memories").select("*").eq("id", memory_id).execute().data
    if not rows:  # deleted, or RLS says you may not see it
        st.error("This memory doesn't exist or you don't have access.")
        return
    m = rows[0]
    is_owner = m["owner_id"] == user.id

    st.title(m["title"])
    left, right = st.columns(2)
    left.image(signed_url(m["photo_path"]), caption=f"Original photo: {m['title']}", use_container_width=True)
    with right:
        for label, key in [("Date", "memory_date"), ("Location", "location"), ("People", "people"),
                           ("Occasion", "occasion"), ("Description", "description")]:
            if m[key]:
                st.markdown(f"**{label}:** {m[key]}")
        st.markdown("**Story:**")
        st.write(m["story"] or "_No story yet._")

    if m["status"] == "draft" and is_owner:
        st.warning("This memory is a draft.")
        if st.button("Continue: add story and comic", type="primary"):
            resume_draft(memory_id)

    st.subheader("Comics")
    comics = sb.table("comics").select("*").eq("memory_id", memory_id).order("approved_at").execute().data
    for c in comics:
        st.image(signed_url(c["image_path"]), caption="Comic: " + " / ".join(c["captions"]), use_container_width=True)
    if not comics:
        st.caption("No approved comic yet.")

    can_edit = is_owner or bool(sb.table("permissions").select("id").eq("memory_id", memory_id)
                                .eq("grantee_id", user.id).eq("level", "edit").execute().data)
    if can_edit:
        edit_details(m)
    if is_owner:
        sharing(m)


def edit_details(m):
    """Owner and 'edit' family members can fix details. Photo and story are not editable."""
    with st.expander("Edit details"), st.form("edit"):
        title = st.text_input("Title", m["title"], max_chars=100)
        location = st.text_input("Location", m["location"] or "", max_chars=100)
        people = st.text_input("People", m["people"] or "", max_chars=200)
        occasion = st.text_input("Occasion", m["occasion"] or "", max_chars=100)
        description = st.text_area("Description", m["description"] or "", max_chars=300)
        if st.form_submit_button("Save changes"):
            if not title.strip():
                st.error("Title can't be empty.")
                return
            get_client().table("memories").update({"title": title.strip(), "location": location, "people": people,
                                                   "occasion": occasion, "description": description}).eq("id", m["id"]).execute()
            log_activity(f"Edited details of '{title.strip()}'", m["id"])
            st.rerun()


def sharing(m):
    sb = get_client()
    st.subheader("Family sharing")
    st.caption("Memories are private until you share them. 'View' can see; 'Edit' can also change the details (never the photo or story).")

    with st.form("share", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        email = c1.text_input("Family member's email")
        level = c2.selectbox("Permission", ["view", "edit"])
        if st.form_submit_button("Share"):
            found = sb.table("users").select("id, email").eq("email", email.strip().lower()).execute().data
            if not found:
                st.error("No Story-scape account uses that email. Ask them to sign up first.")
            elif found[0]["id"] == m["owner_id"]:
                st.error("That's you!")
            else:
                sb.table("permissions").upsert(
                    {"memory_id": m["id"], "grantee_id": found[0]["id"], "level": level},
                    on_conflict="memory_id,grantee_id",
                ).execute()
                sb.table("memories").update({"visibility": "family"}).eq("id", m["id"]).execute()
                log_activity(f"Shared '{m['title']}' with {found[0]['email']} ({level})", m["id"])
                st.rerun()

    grants = sb.table("permissions").select("id, level, users(email)").eq("memory_id", m["id"]).execute().data
    for g in grants:
        c1, c2 = st.columns([3, 1])
        c1.write(f"{g['users']['email']} — can {g['level']}")
        if c2.button("Remove", key=f"rm_{g['id']}"):
            sb.table("permissions").delete().eq("id", g["id"]).execute()
            if len(grants) == 1:  # last person removed: back to private
                sb.table("memories").update({"visibility": "private"}).eq("id", m["id"]).execute()
            log_activity(f"Stopped sharing '{m['title']}' with {g['users']['email']}", m["id"])
            st.rerun()
