import matplotlib.pyplot as plt
import streamlit as st
def reg_scatter_plot(df, y, x):
fig, ax = plt.subplots()
ax.scatter(df[x], df[y])
ax.set_xlabel(x)
ax.set_ylabel(y)
ax.set_title(f"Scatter: {y} vs {x}")
st.pyplot(fig)
