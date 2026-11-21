"""Supabase connection and small database helpers."""
import os

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_secret(name):
    """Read a key from .env locally, or from Streamlit Cloud secrets when deployed."""
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets[name]
    except (KeyError, FileNotFoundError):
        return None


def get_client():
    """One Supabase client per browser session, so each user's login stays separate."""
    if "sb" not in st.session_state:
        st.session_state.sb = create_client(get_secret("SUPABASE_URL"), get_secret("SUPABASE_ANON_KEY"))
    return st.session_state.sb


def current_user():
    """The logged-in user, or None."""
    return st.session_state.get("user")


def log_activity(action, memory_id=None):
    """Write one line to the activity table. Failure here should never break the app."""
    try:
        get_client().table("activity").insert(
            {"user_id": current_user().id, "memory_id": memory_id, "action": action}
        ).execute()
    except Exception:
        pass


def signed_url(path):
    """A temporary (1 hour) link to a private file in the photos bucket."""
    res = get_client().storage.from_("photos").create_signed_url(path, 3600)
    return res.get("signedURL") or res.get("signedUrl")
