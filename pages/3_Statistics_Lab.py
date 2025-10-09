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

        try:
            # Lazy import inside try block
            import matplotlib
            matplotlib.use("Agg")  # Safe backend for Streamlit Cloud
            import matplotlib.pyplot as plt

            # Create the figure
            fig, ax = plt.subplots()
            ax.hist(df['sample_mean'], bins=30, color='skyblue', edgecolor='black')
            ax.set_title("Sampling Distribution of the Mean")
            ax.set_xlabel("Sample Mean")
            ax.set_ylabel("Frequency")

            st.pyplot(fig)

        except ModuleNotFoundError:
            st.error(
                "⚠️ Matplotlib is not installed on this environment. "
                "Please ensure `matplotlib` is listed in your requirements.txt and redeploy the app."
            )
        except Exception as e:
            st.error(f"Unexpected error during plotting: {e}")

    elif demo == "Confidence Intervals":
        st.info("Confidence Interval simulation will be added soon.")
