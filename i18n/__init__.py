"""Bilingual i18n system - flat dict with dotted keys."""

import streamlit as st
from . import fr, en

_TRANSLATIONS = {
    "fr": fr.STRINGS,
    "en": en.STRINGS,
}


def get_lang() -> str:
    """Return current language from session state, default 'fr'."""
    return st.session_state.get("lang", "fr")


def t(key: str) -> str:
    """Translate a dotted key. Returns key itself if missing."""
    lang = get_lang()
    return _TRANSLATIONS.get(lang, _TRANSLATIONS["fr"]).get(key, key)
