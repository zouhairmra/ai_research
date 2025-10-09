# Minimal interactive economic models playground
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def show():
st.header("Economic Models Playground")
st.write("Interactive simulations of classic economic models.")


model = st.selectbox("Choose a model", ["Cobb-Douglas Production", "Solow Growth Model", "Market Equilibrium"])


if model == "Cobb-Douglas Production":
alpha = st.slider("Alpha (output elasticity of capital)", 0.0, 1.0, 0.3)
beta = st.slider("Beta (output elasticity of labor)", 0.0, 1.0, 0.7)
K = st.number_input("Capital (K)", value=100.0)
L = st.number_input("Labor (L)", value=50.0)
A = st.number_input("Total factor productivity (A)", value=1.0)


Y = A * (K ** alpha) * (L ** beta)
st.metric("Output (Y)", f"{Y:.2f}")


st.write("### Explanation")
st.latex(r"Y = A K^{\alpha} L^{\beta}")
st.write("Change K or L or elasticities to observe marginal effects.")


elif model == "Solow Growth Model":
s = st.slider("Savings rate (s)", 0.0, 1.0, 0.2)
n = st.number_input("Population growth rate (n)", value=0.01)
delta = st.number_input("Depreciation (delta)", value=0.05)
alpha = st.slider("Alpha", 0.1, 0.9, 0.33)


k_ss = ((s) / (n + delta)) ** (1 / (1 - alpha))
st.metric("Steady-state capital per worker (k*)", f"{k_ss:.2f}")
st.write("Adjust parameters to see how the steady state moves.")


else:
st.write("Market Equilibrium simulator coming soon — placeholder.")
