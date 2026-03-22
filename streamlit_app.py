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
    temperature=0.7,
    api_key=gemini_key
)

st.set_page_config(page_title="Indian Government Scheme Finder", page_icon="🇮🇳")
st.title("🇮🇳 Indian Government Scheme Finder")
st.write("Fill in your profile and we'll find government schemes you're eligible for.")

# User Profile Form
with st.form("profile_form"):
    st.subheader("Your Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        state = st.text_input("State (e.g. Maharashtra, UP)")
    
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
        placeholder="e.g. education loan, farming support, housing scheme..."
    )
    
    submit = st.form_submit_button("🔍 Find Schemes")

# Generation Logic
if submit:
    if not name or not state:
        st.warning("Please fill Name and State.")
        st.stop()
    
    with st.spinner("Finding relevant schemes for you..."):
        
        # Build user profile query
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
        
        # Build search query for RAG
        query = f"{occupation} {category} {state} government scheme {specific_need}"
        
        # Retrieve relevant schemes
        docs = retrieve_schemes(query)
        
        # Build prompt
        prompt = build_scheme_prompt(user_profile, docs)
        
        # Generate response
        response = llm.invoke(prompt)
    
    st.success("Found relevant schemes!")
    st.markdown("### 📋 Schemes You May Be Eligible For")
    st.markdown(response.content)
    
    st.info("⚠️ Disclaimer: This tool is for informational purposes only. Please visit myscheme.gov.in or consult your local government office for official information.")