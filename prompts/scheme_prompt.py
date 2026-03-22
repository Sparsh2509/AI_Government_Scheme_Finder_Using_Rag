def build_scheme_prompt(user_profile, context):
    
    schemes_text = ""
    for doc in context:
        schemes_text += f"Scheme: {doc.metadata['scheme_name']}\n"
        schemes_text += f"Details: {doc.page_content}\n\n"
    
    return f"""
You are an expert on Indian government schemes.

User Profile:
{user_profile}

Relevant Schemes:
{schemes_text}

Instructions:
- List MAXIMUM 3 most relevant schemes
- Use EXACTLY this format for each scheme:
- NEVER use the scheme code/abbreviation as the name
- Extract the FULL scheme name from the document content
- If full name not found, describe it in simple words
-  For "How to apply": If steps are available in the document, list them. 
  Otherwise provide this clickable link: "Apply at [myscheme.gov.in](https://www.myscheme.gov.in)"

---
**Scheme Name:** [full scheme name]

**What is it:**
[explanation]

**Who can apply:**
[eligibility]

**Benefits:**
[benefits]

**How to apply:**
[steps]

---

- Each field MUST be on its own line
- Never put multiple fields on same line
- Never use abbreviations as scheme names
- Simple language only
"""