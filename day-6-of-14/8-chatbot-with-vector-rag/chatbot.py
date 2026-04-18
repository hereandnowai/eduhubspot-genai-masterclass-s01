from dotenv import load_dotenv
from os import getenv
import os
import ollama
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from system_prompt_simple import system_prompt

load_dotenv()
MODEL = getenv("MODEL_NAME_LOCAL", "gemma4:e2b")
EMBED_MODEL = getenv("EMBED_MODEL", "embeddinggemma:latest")
DOCUMENT_PATH = os.path.join(os.path.dirname(__file__), "mcp.pdf")

# --- Step 1: Set up ChromaDB vector store ---
collection = chromadb.Client().create_collection(name="knowledge_base")
all_chunks: list[str] = []  # kept in memory for keyword search

def get_embedding(text):
    return ollama.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]

# --- Step 2: Load PDF, split into chunks, embed and store ---
def build_vector_store():
    print(f"Indexing: {DOCUMENT_PATH}...")
    docs = PyPDFLoader(DOCUMENT_PATH).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
    for i, chunk in enumerate(chunks):
        all_chunks.append(chunk.page_content)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[get_embedding(chunk.page_content)],
            documents=[chunk.page_content]
        )
    print(f"Indexed {len(chunks)} chunks.")

# --- Step 3: Retrieve relevant chunks (semantic + keyword) ---
def retrieve_context(question, top_k=15):
    # Semantic search via ChromaDB
    results = collection.query(query_embeddings=[get_embedding(question)], n_results=top_k)
    semantic = (results["documents"] or [[]])[0]
    semantic_set = set(semantic)

    # Keyword search — score every chunk by how many question words it contains
    stop = {"who", "what", "when", "where", "how", "did", "does", "the", "and", "for", "was", "are", "with", "into", "that"}
    keywords = [w for w in question.lower().split() if w not in stop]
    scored = sorted(all_chunks, key=lambda c: sum(1 for kw in keywords if kw in c.lower()), reverse=True)
    keyword_hits = [c for c in scored[:10] if c not in semantic_set and any(kw in c.lower() for kw in keywords)]

    return "\n\n".join(semantic + keyword_hits)

# --- Step 4: Stream a response using retrieved context ---
def get_streaming_response(user_input):
    context = retrieve_context(user_input)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_input}"}
    ]
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True, think=True):
        if chunk["message"].get("thinking"):
            yield ("thinking", chunk["message"]["thinking"])
        if chunk["message"].get("content"):
            yield ("response", chunk["message"]["content"])

build_vector_store()

if __name__ == "__main__":
    print(f"Vector RAG Chatbot ({MODEL}) ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        for kind, text in get_streaming_response(user_input):
            print(text, end="", flush=True)
        print("\n")
