import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from rag.retriever import retrieve_schemes
from prompts.scheme_prompt import build_scheme_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = FastAPI(
    title="Indian Government Scheme Finder API",
    description="API to find government schemes based on user profile",
    version="1.0.0"
)

# Pydantic model for request body
class UserProfile(BaseModel):
    name: str
    age: int
    gender: str
    state: str
    occupation: str
    income: str
    category: str
    specific_need: Optional[str] = None

@app.post("/find-schemes")
async def find_schemes(profile: UserProfile):
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found in environment variables")

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.3,
            api_key=gemini_key
        )
        
        # Format user profile string for prompt
        specific_need_str = profile.specific_need if profile.specific_need else "General schemes"
        user_profile_str = f"""
        Name: {profile.name}
        Age: {profile.age}
        Gender: {profile.gender}
        State: {profile.state}
        Occupation: {profile.occupation}
        Annual Income: {profile.income}
        Category: {profile.category}
        Looking for: {specific_need_str}
        """

        # Generate search query
        query_need = profile.specific_need if profile.specific_need else ""
        query = f"{profile.state} state {profile.category} category {profile.occupation} {query_need} government scheme eligibility"

        # Retrieve documents
        docs = retrieve_schemes(query, state=profile.state)
        
        # Build prompt and query LLM
        prompt = build_scheme_prompt(user_profile_str, docs)
        response = llm.invoke(prompt)

        return {
            "success": True,
            "message": f"Found relevant schemes for {profile.name}",
            "schemes": response.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "AI Govt Scheme Finder API Working"}
