import streamlit as st
import pandas as pd
import statsmodels.api as sm

def show():
    st.header("Econometrics Studio")
    st.write("Upload a CSV dataset, select dependent and independent variables, and run OLS regression.")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())
        cols = df.columns.tolist()
        y = st.selectbox("Dependent variable (Y)", cols)
        x = st.multiselect("Independent variables (X)", [c for c in cols if c != y])
        if st.button("Run OLS") and len(x) > 0:
            X = sm.add_constant(df[x])
            model = sm.OLS(df[y], X).fit()
            st.write(model.summary())
