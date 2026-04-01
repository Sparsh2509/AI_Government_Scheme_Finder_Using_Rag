import os
from dotenv import load_dotenv
from rag.retriever import retrieve_schemes
from prompts.scheme_prompt import build_scheme_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3,
    api_key=gemini_key
)

print("🇮🇳 Indian Government Scheme Finder (RAG Powered)\n")

name = input("Enter your name: ")
age = input("Enter your age: ")
gender = input("Enter gender (Male/Female/Other): ")
state = input("Enter your state: ")
occupation = input("Enter occupation (Farmer/Student/Self Employed/Salaried/Unemployed): ")
income = input("Enter annual income (Below 1 Lakh / 1-3 Lakhs / 3-5 Lakhs / Above 5 Lakhs): ")
category = input("Enter category (General/OBC/SC/ST): ")
specific_need = input("What are you looking for? (e.g. farming support, education loan): ")

user_profile = f"""
Name: {name}
Age: {age}
Gender: {gender}
State: {state}
Occupation: {occupation}
Annual Income: {income}
Category: {category}
Looking for: {specific_need}
"""

if specific_need:
    query = f"{specific_need} scheme for {occupation} or {category} category in {state}"
else:
    query = f"government scheme for {occupation} and {category} category in {state} state"

print("\nRetrieving relevant schemes...")
docs = retrieve_schemes(query, state=state)

prompt = build_scheme_prompt(user_profile, docs)

print("Generating response...\n")
response = llm.invoke(prompt)

print("=" * 50)
print("SCHEMES YOU MAY BE ELIGIBLE FOR")
print("=" * 50 + "\n")
print(response.content)
print("\n" + "=" * 50)