import streamlit as st
import pandas as pd
import os


DATA_DIR = Path(__file__).parent.parent / "data"




def show():
st.header("Data Hub")
st.write("Browse built-in datasets or upload your own.")


built_ins = [p.name for p in (DATA_DIR).glob("*.csv")] if DATA_DIR.exists() else []
choice = st.selectbox("Choose dataset", ["Upload a file"] + built_ins)


if choice == "Upload a file":
uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded is not None:
df = pd.read_csv(uploaded)
st.dataframe(df.head())
else:
path = DATA_DIR / choice
if path.exists():
df = pd.read_csv(path)
st.dataframe(df.head())
else:
st.info("No built-in datasets found. Add CSVs to the /data folder.")
