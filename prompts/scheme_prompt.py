def build_scheme_prompt(user_profile, context):
    
    schemes_text = ""
    for doc in context:
        schemes_text += f"Scheme: {doc.metadata['scheme_name']}\n"
        schemes_text += f"Details: {doc.page_content}\n\n"
    
    return f"""
You are an expert on Indian government schemes.

Based on the user profile below, identify relevant government schemes from the context provided.
Explain each scheme in simple, clear English.

User Profile:
{user_profile}

Relevant Schemes from Database:
{schemes_text}

Instructions:
- List only schemes relevant to the user profile
- For each scheme explain: What it is, Who is eligible, What are the benefits, How to apply
- Use simple language, avoid government jargon
- If no schemes match, say "No matching schemes found for your profile"
- Add this disclaimer at the end: "Please visit myscheme.gov.in or consult your local government office for official information."

Response:
"""