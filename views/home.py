"""Home page (Stage 5): greeting, quick stats, main action and recent activity."""
import streamlit as st

from core.db import current_user, get_client


def show():
    sb = get_client()
    user = current_user()
    name = (user.user_metadata or {}).get("display_name", user.email)
    st.title(f"Welcome, {name}")

    memories = sb.table("memories").select("id, owner_id, status").execute().data
    mine = [m for m in memories if m["owner_id"] == user.id]
    c1, c2, c3 = st.columns(3)
    c1.metric("My memories", len(mine))
    c2.metric("Drafts", sum(m["status"] == "draft" for m in mine))
    c3.metric("Shared with me", len(memories) - len(mine))

    if st.button("➕ Add a new memory", type="primary"):
        st.switch_page(st.session_state.pages["add"])

    st.subheader("Recent activity")
    activity = sb.table("activity").select("action, created_at").order("created_at", desc=True).limit(10).execute().data
    if not activity:
        st.info("Nothing yet. Add your first memory!")
    for a in activity:
        st.write(f"• {a['action']} — {a['created_at'][:16].replace('T', ' ')}")
