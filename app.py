"""Story-scape entry point: theme, login gate and the top navbar."""
import streamlit as st

from core.db import get_client
from core.theme import apply_theme
from views import add_memory, auth, home, library, memory

st.set_page_config(page_title="Story-scape", page_icon="📖", layout="wide")
apply_theme()


def logout():
    get_client().auth.sign_out()
    st.session_state.clear()  # forget the user, drafts and the old client
    st.rerun()


# Not logged in: only the login/sign-up page exists
if "user" not in st.session_state:
    st.navigation([st.Page(auth.show, title="Log in", url_path="login")], position="hidden").run()
    st.stop()

# Logged in: the navbar across the top
# Kept in session_state so any page can jump to another with st.switch_page
st.session_state.pages = {
    "home": st.Page(home.show, title="Home", icon="🏠", url_path="home", default=True),
    "add": st.Page(add_memory.show, title="Add Memory", icon="➕", url_path="add"),
    "library": st.Page(library.show, title="Library", icon="📚", url_path="library"),
    "memory": st.Page(memory.show, title="Memory", icon="🖼️", url_path="memory"),
    "logout": st.Page(logout, title="Log out", icon="🚪", url_path="logout"),
}
st.navigation(list(st.session_state.pages.values()), position="top").run()
