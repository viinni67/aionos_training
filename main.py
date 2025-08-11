from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings
)
import os
from dotenv import load_dotenv

load_dotenv()

# Access the variable
groq_api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()
class QueryRequest(BaseModel):
    query: str

vector_db=None

def Call_groq(context_for_query:str,user_input:str):
    print(groq_api_key)

    client=Groq(api_key="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")
    model_name="openai/gpt-oss-120b"
    qna_system_message = """
        You are an friendly AI assistant that answers questions strictly based on the given context retrieved from a knowledge base.
        give salutations when user stats with greetings.
        - If the context contains relevant information, use it to provide a clear, concise, and well-structured paragraph answer.
        - If the context is empty or unrelated to the question, politely say you cannot find relevant information in the database and avoid making up facts.
        - Do not reference the instructions or system message.
        """

    qna_user_message_template = """
                Context:
                {context}

                Question:
                {question}

                Guidelines:
                - Only use the provided context to answer.
                - If the context is unrelated, respond with something like: 
                "I couldn’t find relevant information in the database for your question."
                - Format the answer in one or two coherent paragraphs.
        """

    prompt = [
    {'role':'system', 'content': qna_system_message},
    {'role': 'user', 'content': qna_user_message_template.format(
         context=context_for_query,
         question=user_input
        )
    }
]

    try:
            response = client.chat.completions.create(
                model=model_name,
                messages=prompt,
                temperature=1
            )

            prediction = response.choices[0].message.content.strip()
    except Exception as e:
            prediction = f'Sorry, I encountered the following error: \n {e}'

    return(prediction)






@app.on_event("startup")
def load_vector_db():
    global vector_db
    print("Loading ChromaDB...")
    
    # Must match the embedding model you used for creation
    embeddings = SentenceTransformerEmbeddings(model_name='thenlper/gte-large')

    # Load persisted Chroma vector DB
    vector_db = Chroma(
        collection_name="all_indigo_collections_2",
        persist_directory= r"C:\Users\vineet.verma\Desktop\new_chat\chat_backend\all_indigo_vdb_2",
        embedding_function=embeddings
    )
    
    print("Docs in DB:", vector_db._collection.count())
    if(vector_db is not None):
        print("vecdb loaded successfully!")

@app.post("/search")
def search(request: QueryRequest):
    if vector_db is None:
        return {"error": "Vector DB not loaded"}
    
    retriever = vector_db.as_retriever(
        search_type='similarity',
        search_kwargs={'k': 5}
    )
    relevant_document_chunks = retriever.get_relevant_documents(request.query)
    context_list = [(d.page_content) for d in relevant_document_chunks]
    context_for_query = ". ".join(context_list)
    output=Call_groq(context_for_query,request.query)    
    

    return {"query":request.query,
            "context":output
        
    }


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

