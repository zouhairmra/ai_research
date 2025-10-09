import streamlit as st

def show():
    st.header("Economic Models Playground")
    st.write("Interactive simulations of classic economic models.")

    model = st.selectbox("Choose a model", ["Cobb-Douglas Production", "Solow Growth Model"])

    if model == "Cobb-Douglas Production":
        alpha = st.slider("Alpha (output elasticity of capital)", 0.0, 1.0, 0.3)
        beta = st.slider("Beta (output elasticity of labor)", 0.0, 1.0, 0.7)
        K = st.number_input("Capital (K)", value=100.0)
        L = st.number_input("Labor (L)", value=50.0)
        A = st.number_input("Total factor productivity (A)", value=1.0)
        Y = A * (K ** alpha) * (L ** beta)
        st.metric("Output (Y)", f"{Y:.2f}")
