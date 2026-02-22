"""Shared UI helpers for all pages (CSS, nav buttons, sidebar footer)."""

import os
from pathlib import Path

import streamlit as st

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_CSS_PATH = os.path.join(str(_PROJECT_ROOT), "assets", "style.css")


def inject_custom_css() -> None:
    """Inject custom CSS + floating nav buttons. Call once per page."""
    try:
        with open(_CSS_PATH, encoding="utf-8") as f:
            css_content = f.read()
    except FileNotFoundError:
        css_content = ""

    nav_buttons_html = (
        '<a href="#top" class="nav-button back-to-top"'
        ' title="Retour en haut / Back to top">&#9650;</a>'
        '<a href="#bottom" class="nav-button scroll-to-bottom"'
        ' title="Aller en bas / Go to bottom">&#9660;</a>'
        '<div id="top"></div>'
    )
    st.markdown(f"<style>{css_content}</style>{nav_buttons_html}", unsafe_allow_html=True)


def inject_bottom_anchor() -> None:
    """Add bottom anchor for scroll-to-bottom nav button. Call at end of page."""
    st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)
