import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_correlation_matrix(df, figsize=(8,6)):
    """
    Display correlation heatmap using seaborn.
    """
    corr = df.corr()
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

def plot_histogram(df, column, bins=30):
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=bins, color='skyblue', edgecolor='black')
    ax.set_title(f"Histogram of {column}")
    st.pyplot(fig)
