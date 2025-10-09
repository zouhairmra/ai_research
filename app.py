import streamlit as st
import importlib

st.set_page_config(page_title="EconLab — Interactive Economics Lab", layout='wide')

PAGES = {
    "1. Economic Models": "pages.1_Economic_Models",
    "2. Econometrics Studio": "pages.2_Econometrics_Studio",
    "3. Statistics Lab": "pages.3_Statistics_Lab",
    "4. Data Hub": "pages.4_Data_Hub",
    "5. Report Generator": "pages.5_Report_Generator",
    "6. AI Assistant": "pages.6_AI_Assistant"
}

st.markdown("# EconLab — Where Economic Theory Meets Data")
st.markdown("***")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

module_name = PAGES[selection]
page = importlib.import_module(module_name)
page.show()

st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("© 2025 EconLab — Built by Mohamed Mrabet")
with col2:
    st.markdown("[GitHub](https://github.com/your-username) | [Contact](mailto:your-email@example.com)")
