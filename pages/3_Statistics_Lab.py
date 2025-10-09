import streamlit as st
import numpy as np
import pandas as pd

def show():
    st.header("📊 Statistics Lab")
    st.write("Explore basic statistical simulations interactively.")

    demo = st.selectbox("Choose demo", ["Sampling Distribution", "Confidence Intervals"])

    if demo == "Sampling Distribution":
        mu = st.number_input("Population mean (μ)", value=0.0)
        sigma = st.number_input("Population standard deviation (σ)", value=1.0)
        n = st.slider("Sample size (n)", 5, 500, 30)
        reps = st.slider("Number of repetitions", 100, 2000, 500)

        # Generate sample means
        sample_means = [np.random.normal(mu, sigma, n).mean() for _ in range(reps)]
        df = pd.DataFrame({"sample_mean": sample_means})
        st.dataframe(df.describe())

