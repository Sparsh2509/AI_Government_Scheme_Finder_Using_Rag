# 🇮🇳 AI Government Scheme Finder (Powered by RAG)

An advanced AI-powered application that helps Indian citizens discover government schemes they are eligible for. The system uses **Retrieval-Augmented Generation (RAG)** to semantically search through a massive database of government schemes and utilizes a Large Language Model to perfectly match schemes to a user's demographic profile and specific needs.

## 🚀 Key Features
- **Semantic RAG Search:** Bypasses keyword constraints to find highly relevant schemes based on the user's situation.
- **Dynamic Prioritization:** Capable of prioritizing precise user queries (e.g., "Housing Scheme") while still factoring in demographic filters (Income, Occupation, Category).
- **Generative Summaries:** Uses Google's Gemini LLM to instantly extract and infer *Benefits*, *Eligibility*, and step-by-step *Application Processes*.
- **Multi-Interface:** Comes with a **Streamlit Web UI**, a **FastAPI Backend Service**, and a **Command-Line Interface**.

---

## 🛠️ Technology Stack
- **Frameworks:** Streamlit (Frontend UI), FastAPI (Backend API)
- **AI & RAG:** LangChain, Google Gemini 2.5 Flash-Lite (LLM)
- **Vector Database:** Qdrant (Cloud)
- **Embeddings:** HuggingFace Serverless Inference (`sentence-transformers/all-MiniLM-L6-v2`)

---

## 📂 Project Structure
- `streamlit_app.py`: The visual frontend built in Streamlit.
- `main.py`: The robust FastAPI server providing API endpoints.
- `app.py`: A simple CLI script for quick terminal interactions.
- `rag/retriever.py`: Search logic integrating HuggingFace Embeddings and Qdrant.
- `prompts/scheme_prompt.py`: The highly tuned LangChain prompt for Gemini LLM.

---

## ⚙️ Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sparsh2509/AI_Government-_Scheme_Finder_Using_Rag.git
   cd AI_Government-_Scheme_Finder_Using_Rag
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add the following keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_URL=your_qdrant_cloud_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   HF_TOKEN=your_huggingface_inference_token
   ```

4. **Run the Application (Choose one):**

   *Option A: Streamlit UI (Browser)*
   ```bash
   streamlit run streamlit_app.py
   ```

   *Option B: FastAPI Server (API)*
   ```bash
   uvicorn main:app --reload
   ```

   *Option C: Terminal CLI*
   ```bash
   python app.py
   ```

---

## 📡 API Documentation

If running the FastAPI server (`main.py`), you can test the logic programmatically by sending requests to the API.

### `POST /find-schemes`
**Request Body (JSON):**
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

**Successful Response:**
```json
{
  "success": true,
  "message": "Found relevant schemes for Ramesh Kumar",
  "schemes": "---\n**Scheme Name:** Paramparagat Krishi Vikas Yojana (PKVY)...\n**What is it:**...\n"
}
```

---
*Built with ❤️ for Indian Citizens.*
