import streamlit as st
import numpy as np
import pandas as pd

def show():
    st.header("Statistics Lab")
    st.write("Interactive statistical demos.")

    demo = st.selectbox("Choose demo", ["Sampling Distribution", "Confidence Intervals"])

    if demo == "Sampling Distribution":
        mu = st.number_input("Population mean", value=0.0)
        sigma = st.number_input("Population sd", value=1.0)
        n = st.slider("Sample size", 5, 500, 30)
        reps = st.slider("Repetitions", 100, 2000, 500)

        sample_means = [np.random.normal(mu, sigma, n).mean() for _ in range(reps)]
        df = pd.DataFrame({"sample_mean": sample_means})
        st.write(df.describe())

        # Lazy import only here
        import matplotlib
        matplotlib.use("Agg")  # <- critical fix for Streamlit Cloud
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.hist(df['sample_mean'], bins=30, color='skyblue', edgecolor='black')
        ax.set_title("Sampling Distribution of the Mean")
        st.pyplot(fig)
