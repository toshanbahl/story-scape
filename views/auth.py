"""Log in and sign up (Stage 3). Supabase Auth checks passwords; we never store them."""
import streamlit as st

from core.db import get_client


def show():
    st.title("Story-scape")
    st.write("Turn family photos and stories into four-panel comics.")
    login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

    with login_tab, st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Log in"):
            try:
                res = get_client().auth.sign_in_with_password({"email": email.strip(), "password": password})
                st.session_state.user = res.user
                st.rerun()
            except Exception:
                st.error("Wrong email or password, or your email is not confirmed yet.")

    with signup_tab, st.form("signup"):
        name = st.text_input("Your name")
        email = st.text_input("Email", key="su_email")
        password = st.text_input("Password (at least 8 characters)", type="password", key="su_pw")
        if st.form_submit_button("Create account"):
            if not name.strip() or "@" not in email or len(password) < 8:
                st.error("Please enter your name, a valid email and a password of 8+ characters.")
            else:
                try:
                    res = get_client().auth.sign_up({
                        "email": email.strip(), "password": password,
                        "options": {"data": {"display_name": name.strip()}},
                    })
                    if res.session:  # email confirmation is off in Supabase: log straight in
                        st.session_state.user = res.user
                        st.rerun()
                    st.success("Account created! Check your email to confirm, then log in.")
                except Exception as e:
                    st.error(f"Could not create account: {e}")
