import streamlit as st
import pandas as pd
import numpy as np

def show():
    st.header("Econometrics Studio (Simplified)")
    st.write("Upload a CSV dataset, select dependent and independent variables, and compute basic regression manually.")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())
        cols = df.columns.tolist()
        y_col = st.selectbox("Dependent variable (Y)", cols)
        x_cols = st.multiselect("Independent variables (X)", [c for c in cols if c != y_col])

        if st.button("Run Simple Regression") and len(x_cols) > 0:
            X = df[x_cols].values
            y = df[y_col].values.reshape(-1,1)
            # Add intercept manually
            X = np.hstack([np.ones((X.shape[0],1)), X])
            beta = np.linalg.pinv(X.T @ X) @ X.T @ y
            st.write("Regression Coefficients:")
            st.write({"Intercept": float(beta[0]), **{x_cols[i]: float(beta[i+1]) for i in range(len(x_cols))}})
