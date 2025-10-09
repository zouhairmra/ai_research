import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def show():
    st.header("Data Hub")
    st.write("Browse built-in datasets or upload your own CSV.")

    built_in_files = [f.name for f in DATA_DIR.glob("*.csv")] if DATA_DIR.exists() else []
    choice = st.selectbox("Select dataset", ["Upload CSV"] + built_in_files)

    if choice == "Upload CSV":
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head())
            st.write(df.describe())
    else:
        path = DATA_DIR / choice
        if path.exists():
            df = pd.read_csv(path)
            st.dataframe(df.head())
            st.write(df.describe())
