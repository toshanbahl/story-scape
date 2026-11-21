"""Story-scape look and feel (Stage 4) plus accessibility rules (Stage 12).
Style: warm cream page, soft orange glow, big heavy headings, dark outlined inputs."""
import streamlit as st

ORANGE = "#E8651A"
CREAM = "#FDF8F3"
DARK = "#2C1A0E"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"], .stApp, input, textarea, button {{
    font-family: 'Inter', sans-serif; font-size: 16px; color: {DARK};
}}

/* Cream page with two soft orange glows (decoration only, behind everything) */
.stApp {{
    background:
        radial-gradient(520px 360px at 78% 18%, rgba(232,101,26,0.38), transparent 70%),
        radial-gradient(460px 380px at 5% 95%, rgba(232,101,26,0.20), transparent 70%),
        {CREAM};
    background-attachment: fixed;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ max-width: 960px; padding-top: 5rem; }}

/* Big, heavy, tight headings */
h1 {{ font-weight: 800 !important; font-size: clamp(2.4rem, 6vw, 4rem) !important;
      letter-spacing: -0.04em; line-height: 1.05 !important; }}
h2, h3 {{ font-weight: 800 !important; letter-spacing: -0.02em; }}

/* Inputs: light fill, dark 2px outline, 8px radius, 44px+ tall */
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.6) !important; border: 2px solid {DARK} !important;
    border-radius: 8px !important; min-height: 44px;
}}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{ background: transparent !important; }}
[data-testid="stTextInputRootElement"], [data-testid="stDateInputField"] {{ height: auto !important; }}
input {{ min-height: 44px !important; }}
[data-testid="stFileUploaderDropzone"] {{
    background: rgba(255,255,255,0.6); border: 2px dashed {DARK}; border-radius: 8px;
}}

/* Buttons: 44px+, 8px radius, bold. Secondary = outlined, primary = solid dark */
.stButton button, .stDownloadButton button, .stFormSubmitButton button {{
    min-height: 44px; border-radius: 8px !important; font-weight: 600;
    border: 2px solid {DARK} !important; background: transparent; color: {DARK};
    padding: 0.5rem 1.25rem;
}}
.stButton button:hover {{ background: rgba(232,101,26,0.10); color: {DARK}; }}
/* dark on cream is ~16:1 contrast; orange stays as the accent colour */
.stButton button[kind="primary"], [data-testid="stFormSubmitButton"] button {{
    background: {DARK} !important; color: {CREAM} !important; width: 100%; min-height: 52px;
}}
[data-testid="stFormSubmitButton"], .stButton:has(button[kind="primary"]) {{ width: 100%; }}
.stButton button[kind="primary"]:hover, .stFormSubmitButton button:hover {{ background: #000 !important; }}

/* Clear keyboard focus ring so keyboard users can see where they are */
button:focus-visible, input:focus-visible, textarea:focus-visible, a:focus-visible {{
    outline: 3px solid {ORANGE} !important; outline-offset: 2px;
}}

/* Cards (library tiles, forms) */
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stForm"] {{
    background: rgba(255,255,255,0.55); border: 2px solid {DARK} !important; border-radius: 8px;
}}

/* Tabs and progress bar in the accent colour */
.stTabs [aria-selected="true"] {{ color: {DARK} !important; font-weight: 800; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {DARK}; height: 3px; }}
.stProgress > div > div > div > div {{ background: {ORANGE}; }}

/* Small screens: 16px side gutters, less top space */
@media (max-width: 640px) {{
    .block-container {{ padding: 3rem 16px 2rem; }}
}}
</style>
"""


def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)
