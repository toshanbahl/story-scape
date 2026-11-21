"""Story-scape look and feel (Stage 4) plus accessibility rules (Stage 12)."""
import streamlit as st

ORANGE = "#E8651A"
CREAM = "#FDF8F3"
DARK = "#2C1A0E"

CSS = f"""
<style>
html, body, [class*="css"] {{ font-size: 16px; color: {DARK}; }}
.stApp {{ background: {CREAM}; }}

/* 44px minimum touch targets, 8px radius on everything clickable */
.stButton button, .stDownloadButton button, .stFormSubmitButton button,
input, textarea, [data-baseweb="select"] > div {{
    min-height: 44px; border-radius: 8px !important;
}}
.stButton button[kind="primary"], .stFormSubmitButton button {{
    /* dark text on orange: about 5:1 contrast (white would only be about 3.3:1, failing WCAG AA) */
    background: {ORANGE}; color: {DARK}; border: none; font-weight: 600;
}}

/* Clear keyboard focus ring so keyboard users can see where they are */
button:focus-visible, input:focus-visible, textarea:focus-visible, a:focus-visible {{
    outline: 3px solid {DARK} !important; outline-offset: 2px;
}}

/* Memory cards in the library */
.card {{ background: #fff; border-radius: 8px; padding: 12px; border: 1px solid #eadfd4; }}

/* Small screens: let columns stack and keep side gutters */
@media (max-width: 640px) {{
    .block-container {{ padding-left: 16px; padding-right: 16px; }}
}}
</style>
"""


def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)
