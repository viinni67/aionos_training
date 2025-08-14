**🚀 RAG-Powered Chatbot with Streamlit + FastAPI (Groq API + GPT-OSS-120B)**
📌 **Overview**
This project is a Retrieval-Augmented Generation (RAG) based chatbot with:

Frontend: Built with Streamlit for an interactive and lightweight chat interface.

Backend: Powered by FastAPI for handling requests, orchestrating responses, and managing retrieval logic.

LLM Engine: Uses the Groq API with the model openai/gpt-oss-120b for high-quality, low-latency responses.

Vector Database: ChromaDB for context retrieval, pre-trained on Google Colab and loaded into the backend for fast querying.

This architecture enables context-aware, domain-specific responses while maintaining guardrails for safety and relevance.

[ User ]  
   ⬇ (Query)  
[ Streamlit Frontend ] —(API Call)→ [ FastAPI Backend ]  
   ⬇                                   ⬇  
[ Chroma Vector DB ] ←— Retriever — [ Groq API (GPT-OSS-120B) ]  


**Prompt Engineering & Guardrails**

We implemented prompt engineering to ensure the chatbot remains safe, accurate, and on-topic.

Approach:

Context Injection – The retrieved knowledge chunks from Chroma are inserted into the prompt as context.

Instruction Layer – A fixed system prompt ensures the model answers only from provided context.

Guardrails – Added conditional logic to handle:

Irrelevant Queries – Respond politely when context doesn’t match user query.

Harmful Queries – Refuse unsafe or unethical requests.

Fallback Behavior – If no relevant context is found, the model responds with a helpful fallback message rather than hallucinating.

Example System Prompt:






🗂** Vector Database with Chroma**

We use Chroma as our vector store for efficient semantic search.

Workflow:

Data Preparation – Documents are cleaned and chunked in Google Colab.

Embedding Generation – Pre-trained embeddings are created and stored in Chroma.

Persistence – The Chroma DB is saved locally after training.

Loading into Backend – On FastAPI startup, the persisted Chroma DB is loaded into memory for retrieval.

This allows the chatbot to instantly fetch top-K relevant chunks for each query.





**Installation & Setup**
front end set up 

cd frontend
pip install -r requirements.txt
streamlit run app.py


Backend setup 
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

env variables 
GROQ_API_KEY=your_api_key_here
MODEL_NAME=openai/gpt-oss-120b
