# 🇮🇳 AI Government Scheme Finder using RAG

An AI-powered Government Scheme Finder built using **Retrieval-Augmented Generation (RAG)**.  
By combining semantic scheme retrieval via Qdrant & Hugging Face embeddings with the reasoning power of Google Gemini, this system finds and explains highly relevant, context-aware government schemes tailored to any specific demographic profile, income, and personal needs.

Live UI Demo: [https://aigovernmentschemefinderusingrag-tfhncfcuspjwp3zztmgwzf.streamlit.app/](https://aigovernmentschemefinderusingrag-tfhncfcuspjwp3zztmgwzf.streamlit.app/) 

Live REST API: [https://ai-government-scheme-finder-using-rag.onrender.com](https://ai-government-scheme-finder-using-rag.onrender.com)

---

## 🚀 Features

- Discover relevant government schemes across India (Housing, Education, Agriculture, etc.)
- Context-aware retrieval using RAG
- Semantic scheme matching using Qdrant Cloud Vector Database (zero local storage footprint)
- HuggingFace Serverless embeddings (all-MiniLM-L6-v2)
- Gemini 2.5 Flash Lite for generation and inferring benefits
- Interactive Streamlit Web UI
- Deployed on Streamlit Cloud & Render

---

## 🏗 Architecture

User Input Profile & Needs  
↓  
Generate Semantic Query dynamically  
↓  
HuggingFace Embeddings API  
↓  
Qdrant Vector Database Search  
↓  
Retrieve Top-K Relevant Schemes  
↓  
Inject Context into Prompt  
↓  
Gemini LLM Generates Final Eligibility Report  

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- HuggingFace Endpoints
- Qdrant Cloud Vector Database (Fully managed, no local storage required)
- Google Gemini API
- dotenv
- FastAPI (REST API)
- Uvicorn

---

## 📂 Project Structure

```
AI_Government-_Scheme_Finder_Using_Rag/
│
├── streamlit_app.py            # Streamlit UI for finding schemes using Gemini API
├── app.py                      # CLI-based scheme finding interface
├── main.py                     # FastAPI REST endpoint exposing the RAG pipeline
│
├── rag/
│   ├── build_vectorstore.py    # Embeds scheme documents and builds Qdrant vector index
│   ├── retriever.py            # Retrieves top relevant schemes using semantic search
│
├── prompts/
│   ├── scheme_prompt.py        # Instructs Gemini LLM to format benefits, eligibility, and steps
│
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## ⚙ How It Works

1. User enters:
   - Name, Age, Gender
   - State & Category (General/OBC/SC/ST)
   - Occupation & Annual Income
   - Specific Need (e.g. "Housing Scheme", "Education Loan")

2. System:
   - Evaluates if the user entered a specific need to prioritize the semantic query.
   - Converts query into embeddings via Hugging Face Inference API.
   - Retrieves similar official government schemes from Qdrant.
   - Injects the official scheme details into a structured prompt.
   - Gemini evaluates eligibility, extracts steps, and logically infers missing benefits.

This ensures hyper-accurate and highly personalized results compared to simple keyword matching on government portals.

---

## 📥 Sample Request

Below is an example user input provided through the UI:

```
Name: Sparsh
Age: 25
Gender: Male
State: Delhi
Occupation: Student
Annual Income: Below 1 Lakh
Category: General
Specific Need: Housing Scheme
```

---

## 📤 Sample Response

```markdown
✅ Found relevant schemes for Sparsh!

### Schemes You May Be Eligible For

---
**Scheme Name:** Delhi Mukhyamantri Awas Yojana

**What is it:**
This scheme aims to provide affordable housing and rehabilitation for residents belonging to lower-income groups residing in the state of Delhi.

**Who can apply:**
- Must be a permanent resident of Delhi.
- Total family income must be classified under Economically Weaker Sections (EWS).

**Benefits:**
The scheme provides financial assistance for the construction or acquisition of a house, ensuring secure and permanent housing for eligible students and families.

**How to apply:**
1. Visit the nearest Delhi Urban Shelter Improvement Board (DUSIB) office.
2. Collect and fill out the housing application form.
3. Submit the required income certificates, Aadhaar card, and residence proof.
---
```

---

## 🔌 REST API

A FastAPI layer was built to expose the RAG pipeline as a REST endpoint.

### Live API Endpoint (Render)
You can test the API directly via POST request at:
`https://ai-government-scheme-finder-using-rag.onrender.com/find-schemes`

### Run API Locally
```bash
uvicorn main:app --reload
```

### Endpoint

`POST /find-schemes`

### Request Body
```json
{
  "name": "Ramesh Kumar",
  "age": 25,
  "gender": "Male",
  "state": "Maharashtra",
  "occupation": "Farmer",
  "income": "Below 1 Lakh",
  "category": "OBC",
  "specific_need": "farming support"
}
```

### Response
```json
{
  "success": true,
  "message": "Found relevant schemes for Ramesh Kumar",
  "schemes": "---\n**Scheme Name:** Paramparagat Krishi Vikas Yojana (PKVY)\n\n**What is it:**\nThis scheme promotes organic farming...\n"
}
```

---

## 🔎 What Makes This Response Context-Aware?

- The system searches the Qdrant vector database prioritizing matching logic for both the user demographic context (State, Category) and exact contextual needs (Occupation, specific need).
- If the official scheme text in the DB lacks explicit explanations of the benefits, Gemini 2.5 uses its internalized knowledge of Indian Government schemes to thoughtfully infer and expand on the benefits section for the user.

---

## 🧪 Run Locally

### Clone Repository

```bash
git clone https://github.com/Sparsh2509/AI_Government-_Scheme_Finder_Using_Rag.git
cd AI_Government-_Scheme_Finder_Using_Rag
```

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root of project and add API keys. We use the Hugging Face Serverless Inference API to handle embeddings with zero local memory cost, and Qdrant Cloud.

```env
GEMINI_API_KEY="google_gemini_token"
HF_TOKEN="huggingface_token"
QDRANT_URL="qdrant_cloud_cluster_url"
QDRANT_API_KEY="qdrant_api_key"
```
> **Important:** Your Hugging Face token must have the **"Make calls to the serverless Inference API"** permission enabled.


### Run Streamlit App

```bash
streamlit run streamlit_app.py
```
