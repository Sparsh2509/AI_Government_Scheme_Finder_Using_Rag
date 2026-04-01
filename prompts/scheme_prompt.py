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
- PRIORITIZE schemes that match the user's state from their profile
- If a scheme is from a different state, clearly mention it
- NEVER use abbreviations as scheme names
- Extract the FULL scheme name from the document content
- For "How to apply": If steps are available list them as numbered steps.
  If not available, generate logical application steps based on the scheme type.
  Never give "visit website" as the only step.
- For "Benefits": If exact benefits are not explicitly detailed in the text, use your general knowledge of Indian government schemes to logically explain what the benefits are. Do not say "not explicitly detailed" or similar phrases.
- Use EXACTLY this format:

---
**Scheme Name:** [full scheme name]

**What is it:**
[explanation]

**Who can apply:**
[eligibility]

**Benefits:**
[benefits]

**How to apply:**
1. [step 1]
2. [step 2]
3. [step 3]

---

- Each field MUST be on its own line
- Simple language only
"""