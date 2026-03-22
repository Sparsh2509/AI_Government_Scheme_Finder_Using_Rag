def build_scheme_prompt(user_profile, context):
    
    schemes_text = ""
    for doc in context:
        schemes_text += f"Scheme: {doc.metadata['scheme_name']}\n"
        schemes_text += f"Details: {doc.page_content}\n\n"
    
    return f"""
You are an expert on Indian government schemes.

Based on the user profile below, identify relevant government schemes.

User Profile:
{user_profile}

Relevant Schemes:
{schemes_text}

Instructions:
- List MAXIMUM 3 most relevant schemes
- Use EXACTLY this format for each scheme:

### 1. [Scheme Name]
**What is it:** [one line explanation]
**Who can apply:** [eligibility in simple words]
**Benefits:** [what you get]
**How to apply:** [steps]

- Use simple language
- If no schemes match say "No matching schemes found"
"""