import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def show():
st.header("Statistics Lab")
st.write("Interactive demonstrations of foundational statistical concepts.")


demo = st.selectbox("Choose demo", ["Sampling Distribution", "Confidence Intervals", "Distribution Comparison"])


if demo == "Sampling Distribution":
pop_mean = st.number_input("Population mean", value=0.0)
pop_sd = st.number_input("Population sd", value=1.0)
n = st.slider("Sample size (n)", 5, 500, 30)
reps = st.slider("Number of repetitions", 100, 2000, 500)


sample_means = []
for _ in range(reps):
s = np.random.normal(pop_mean, pop_sd, size=n)
sample_means.append(s.mean())
df = pd.DataFrame({"sample_mean": sample_means})
st.write(df.describe())
fig, ax = plt.subplots()
ax.hist(df['sample_mean'], bins=30)
ax.set_title("Sampling distribution of the mean")
st.pyplot(fig)


elif demo == "Confidence Intervals":
mu = st.number_input("True mean (mu)", value=0.0)
sigma = st.number_input("True sigma", value=1.0)
n = st.slider("Sample size", 5, 200, 30)
alpha = st.selectbox("Confidence level", [0.90, 0.95, 0.99])


data = np.random.normal(mu, sigma, size=n)
se = sigma / (n ** 0.5)
import scipy.stats as stats
z = stats.norm.ppf(1 - (1 - alpha) / 2)
ci_low = data.mean() - z * se
ci_high = data.mean() + z * se
st.write(f"Sample mean: {data.mean():.4f}")
st.write(f"{int(alpha*100)}% CI: [{ci_low:.4f}, {ci_high:.4f}]")


else:
st.write("Distribution comparison coming soon.")
