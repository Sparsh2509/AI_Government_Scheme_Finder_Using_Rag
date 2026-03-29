import os
import streamlit as st
from dotenv import load_dotenv
from rag.retriever import retrieve_schemes
from prompts.scheme_prompt import build_scheme_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not gemini_key:
    st.error("GEMINI_API_KEY not found")
    st.stop()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3,
    api_key=gemini_key
)

st.set_page_config(
    page_title="Indian Government Scheme Finder",
    page_icon="🇮🇳",
    layout="wide"
)

# Header
st.title("🇮🇳 Indian Government Scheme Finder")
st.write("Fill in your profile and we'll find government schemes you're eligible for.")
st.markdown("---")

# User Profile Form
with st.form("profile_form"):
    st.subheader("👤 Your Profile")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Your Name", placeholder="e.g. Ramesh Kumar")
        age = st.number_input("Age", min_value=1, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        state = st.text_input("State", placeholder="e.g. Maharashtra, Uttar Pradesh")

    with col2:
        occupation = st.selectbox("Occupation", [
            "Farmer", "Student", "Self Employed",
            "Salaried", "Unemployed", "Business Owner"
        ])
        income = st.selectbox("Annual Income", [
            "Below 1 Lakh", "1-3 Lakhs",
            "3-5 Lakhs", "Above 5 Lakhs"
        ])
        category = st.selectbox("Category", [
            "General", "OBC", "SC", "ST"
        ])

    specific_need = st.text_area(
        "What are you looking for? (optional)",
        placeholder="e.g. education loan, farming support, housing scheme, business loan..."
    )

    submit = st.form_submit_button("🔍 Find Schemes", use_container_width=True)

# Generation Logic
if submit:
    if not name or not state:
        st.warning("⚠️ Please fill Name and State.")
        st.stop()

    with st.spinner("🔍 Searching through 2000+ government schemes for you..."):

        user_profile = f"""
        Name: {name}
        Age: {age}
        Gender: {gender}
        State: {state}
        Occupation: {occupation}
        Annual Income: {income}
        Category: {category}
        Looking for: {specific_need if specific_need else 'General schemes'}
        """

        query = f"government scheme for {occupation} {category} category {state} state {specific_need}"

        docs = retrieve_schemes(query)
        prompt = build_scheme_prompt(user_profile, docs)
        response = llm.invoke(prompt)

    st.markdown("---")
    st.success(f"✅ Found relevant schemes for **{name}**!")
    st.markdown("### 📋 Schemes You May Be Eligible For")
    st.markdown(response.content)
    st.markdown("---")

    # Disclaimer
    st.info("⚠️ **Disclaimer:** This tool is for informational purposes only. Data sourced from myscheme.gov.in. Always verify eligibility and apply at [myscheme.gov.in](https://www.myscheme.gov.in) or consult your local government office.")

    # Quick link
    st.markdown("🔗 **Apply directly:** [myscheme.gov.in](https://www.myscheme.gov.in)")