import os
os.system("pip install exa-py cerebras-cloud-sdk")
import streamlit as st
from duckduckgo_search import DDGS
from cerebras.cloud.sdk import Cerebras

# API keys (store securely in Streamlit Cloud later)
EXA_API_KEY = st.secrets["EXA_API_KEY"]
CEREBRAS_API_KEY = st.secrets["CEREBRAS_API_KEY"]

# Initialize clients
exa = Exa(api_key=EXA_API_KEY)
client = Cerebras(api_key=CEREBRAS_API_KEY)

# Define search function
def search_web(query, num=5):
    """Web search using DuckDuckGo (fallback for Exa)"""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num):
            results.append({
                "title": r["title"],
                "content": r["body"]
            })
    return results

# Define AI analysis function
def ask_ai(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-4-scout-17b-16e-instruct",
        max_tokens=600,
        temperature=0.2
    )
    return chat_completion.choices[0].message.content

# Define research workflow
def research_topic(query):
    results = search_web(query, 5)
    sources = []
    for result in results:
        if result.text and len(result.text) > 200:
            sources.append({"title": result.title, "content": result.text})
    if not sources:
        return "No sources found."

    context = f"Research query: {query}\n\nSources:\n"
    for i, s in enumerate(sources[:4], 1):
        context += f"{i}. {s['title']}: {s['content'][:400]}...\n\n"

    prompt = f"""{context}
    Based on these sources, provide:
    SUMMARY: [2-3 sentences]
    INSIGHTS: - [3 bullet points]
    """
    return ask_ai(prompt)

# Streamlit UI
st.title("🔍 AI Research Assistant")
st.write("Enter a topic and let AI summarize the latest web knowledge for you.")

query = st.text_input("Research Topic", "")
if st.button("Run Research"):
    if query:
        with st.spinner("Running research..."):
            result = research_topic(query)
        st.success("Research complete!")
        st.write(result)
    else:
        st.warning("Please enter a topic.")
