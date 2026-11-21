"""Library and search (Stage 9). RLS means this query only ever returns
memories the user owns or that were shared with them."""
import streamlit as st

from core.db import current_user, get_client, signed_url

SEARCH_FIELDS = ("title", "location", "people", "occasion", "description", "story")


def matches(memory, query):
    """True if every word of the search appears somewhere in the memory's text."""
    text = " ".join(str(memory.get(f) or "") for f in SEARCH_FIELDS).lower()
    return all(word in text for word in query.lower().split())


def show():
    st.title("Library")
    user = current_user()
    c1, c2 = st.columns([3, 1])
    query = c1.text_input("Search by title, people, place or story", placeholder="e.g. grandma beach")
    which = c2.selectbox("Show", ["All", "Mine", "Shared with me", "Drafts"])

    memories = get_client().table("memories").select("*").order("created_at", desc=True).execute().data
    if which == "Mine":
        memories = [m for m in memories if m["owner_id"] == user.id]
    elif which == "Shared with me":
        memories = [m for m in memories if m["owner_id"] != user.id]
    elif which == "Drafts":
        memories = [m for m in memories if m["status"] == "draft"]
    memories = [m for m in memories if matches(m, query)]

    if not memories:
        st.info("No memories found.")
        return

    cols = st.columns(3)
    for i, m in enumerate(memories):
        with cols[i % 3], st.container(border=True):
            st.image(signed_url(m["photo_path"]), caption=f"Photo: {m['title']}", use_container_width=True)
            st.markdown(f"**{m['title']}**")
            tag = "📝 Draft" if m["status"] == "draft" else ("👪 Shared with you" if m["owner_id"] != user.id else "🔒 " + m["visibility"].title())
            st.caption(f"{tag} · {m['memory_date'] or 'no date'} · {m['location'] or ''}")
            if st.button("Open", key=f"open_{m['id']}"):
                st.session_state.open_memory = m["id"]
                st.switch_page(st.session_state.pages["memory"])
