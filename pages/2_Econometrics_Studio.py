import streamlit as st
import pandas as pd
import statsmodels.api as sm
from utils.plot_utils import reg_scatter_plot




def show():
st.header("Econometrics Studio")
st.write("Upload a CSV dataset, select dependent and independent variables, and run OLS regression.")


uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded is not None:
df = pd.read_csv(uploaded)
st.write("Preview of dataset:")
st.dataframe(df.head())


cols = df.columns.tolist()
y = st.selectbox("Choose dependent variable (Y)", cols)
x = st.multiselect("Choose independent variables (X)", [c for c in cols if c != y])


if st.button("Run OLS") and len(x) > 0:
X = df[x]
X = sm.add_constant(X)
model = sm.OLS(df[y], X, missing='drop').fit()
st.write(model.summary())


# simple scatter for first regressor
reg_scatter_plot(df, y, x[0])


else:
st.info("Upload a CSV to begin. Example datasets can be placed in /data and uploaded here.")
