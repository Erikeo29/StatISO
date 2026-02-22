"""StatISO -- main entry point.

Run with:  streamlit run app/Home.py
"""

import os
import sys
from pathlib import Path

# Add project root to path so core/, i18n/, data/ are importable
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from data.handler import DataHandler
from data.report import ReportGenerator
from i18n import get_lang, t

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="StatISO",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

_cfg_path = os.path.join(str(_PROJECT_ROOT), "config.yaml")
with open(_cfg_path) as _f:
    _auth_config = yaml.load(_f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    _auth_config["credentials"],
    _auth_config["cookie"]["name"],
    _auth_config["cookie"]["key"],
    _auth_config["cookie"]["expiry_days"],
)

authenticator.login()

if not st.session_state.get("authentication_status"):
    if st.session_state.get("authentication_status") is False:
        st.error("Identifiants incorrects / Invalid credentials")
    else:
        st.info("Entrez vos identifiants / Enter your credentials")
    st.stop()

# Save config (updates failed_login_attempts, logged_in status)
try:
    with open(_cfg_path, "w") as _f:
        yaml.dump(_auth_config, _f, default_flow_style=False)
except OSError:
    pass

# ---------------------------------------------------------------------------
# Sidebar -- language selector
# ---------------------------------------------------------------------------

with st.sidebar:
    authenticator.logout(location="sidebar")
    lang = st.selectbox(
        t("sidebar.language"),
        options=["fr", "en"],
        index=0 if get_lang() == "fr" else 1,
        format_func=lambda x: "Fran\u00e7ais" if x == "fr" else "English",
    )
    st.session_state["lang"] = lang

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Sidebar -- data loading
    # -----------------------------------------------------------------------

    st.subheader(t("sidebar.data_source"))

    uploaded_file = st.file_uploader(
        t("sidebar.upload_file"),
        type=["csv", "xlsx", "xls"],
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name
        columns = DataHandler.get_columns(file_bytes, filename)

        col_choice = None
        if len(columns) > 1:
            col_choice = st.selectbox(t("sidebar.column_select"), columns)

        try:
            data = DataHandler.load_file(file_bytes, filename, col_choice)
            st.session_state["data"] = data
            st.success(t("sidebar.data_loaded").format(n=len(data)))
        except Exception as exc:
            st.error(f"{t('common.error')}: {exc}")

    # Sample data button
    if st.button(t("sidebar.use_sample")):
        sample_path = (
            Path(__file__).resolve().parent.parent / "data" / "sample_data.csv"
        )
        df = pd.read_csv(sample_path)
        st.session_state["data"] = df.iloc[:, 0].dropna().values.astype(float)
        st.success(t("sidebar.sample_loaded"))

    # Manual input
    with st.expander(t("sidebar.manual_input")):
        manual_text = st.text_area(
            t("sidebar.manual_input"),
            placeholder=t("sidebar.manual_placeholder"),
            height=120,
            label_visibility="collapsed",
        )
        if st.button(t("sidebar.validate")):
            try:
                data = DataHandler.parse_manual_input(manual_text)
                st.session_state["data"] = data
                st.success(t("sidebar.data_loaded").format(n=len(data)))
            except Exception as exc:
                st.error(f"{t('common.error')}: {exc}")

    # Current data status
    st.markdown("---")
    if "data" in st.session_state and st.session_state["data"] is not None:
        data = st.session_state["data"]
        st.caption(t("sidebar.data_loaded").format(n=len(data)))
    else:
        st.caption(t("sidebar.no_data"))

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------

st.title(t("app.title"))
st.subheader(t("app.subtitle"))

if "data" in st.session_state and st.session_state["data"] is not None:
    data = st.session_state["data"]

    # -- Descriptive statistics row 1 --
    cols = st.columns(4)
    cols[0].metric(t("stats.n"), len(data))
    cols[1].metric(t("stats.mean"), f"{np.mean(data):.4f}")
    cols[2].metric(t("stats.std"), f"{np.std(data, ddof=1):.4f}")
    cols[3].metric(t("stats.median"), f"{np.median(data):.4f}")

    # -- Descriptive statistics row 2 --
    cols2 = st.columns(4)
    cols2[0].metric(t("stats.min"), f"{np.min(data):.4f}")
    cols2[1].metric(t("stats.max"), f"{np.max(data):.4f}")
    cols2[2].metric(t("stats.q1"), f"{np.percentile(data, 25):.4f}")
    cols2[3].metric(t("stats.q3"), f"{np.percentile(data, 75):.4f}")

    # -- Quick distribution plot --
    fig = ReportGenerator.distribution_plot(
        data,
        np.mean(data),
        np.std(data, ddof=1),
        title=t("common.distribution_plot"),
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info(t("common.no_data"))
