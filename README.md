# AI Freelance Portfolio

Python projects demonstrating AI integration using the Gemini API.

## Projects

### 1. Customer Review Analyzer (`api_test.py`)
Analyzes customer reviews using Gemini API. Returns sentiment, score, and summary in JSON format for each review, then generates an overall report.

**Concepts:** JSON parsing, batch API calls, structured output

### 2. Customer Support Chatbot
A rule-based support bot for a fictional electronics store (TechStore). Uses system prompts to enforce business rules — returns policy, shipping info, warranty terms.

**Concepts:** System prompts, conversation history, temperature control

### 3. Document Q&A Assistant (`Docapp.py`)
Upload any `.txt` file and ask questions about it. Uses a basic RAG approach — splits the document into sections, finds relevant parts, and feeds only those to the model.

**Concepts:** File handling, basic RAG, Streamlit UI

## Tech Stack
- Python 3.14
- Google Gemini API 
- Streamlit
- google-genai SDK

## Setup
1. Clone the repo
2. Install dependencies: `pip install google-genai streamlit`
3. Add your Gemini API key where indicated in the code
4. Run the Streamlit app: `python -m streamlit run Docapp.py`