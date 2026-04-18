from dotenv import load_dotenv
from os import getenv
import os
import ollama
from langchain_community.document_loaders import PyPDFLoader
from system_prompt_simple import system_prompt

load_dotenv()
MODEL = getenv("MODEL_NAME_LOCAL", "gemma3:270m")

# Path to the PDF document to use as knowledge base
# Using __file__ ensures the path works regardless of where the app is launched from
PDF_PATH = os.path.join(os.path.dirname(__file__), "profile-of-ruthran-raghavan-chief-ai-scientist-here-and-now-ai.pdf")

def load_pdf_context(pdf_path):
    if not os.path.exists(pdf_path):
        return f"Warning: {pdf_path} not found. Proceeding without document context."
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    return " ".join([page.page_content for page in pages])

# Load the PDF once at startup and inject into the system prompt
pdf_context = load_pdf_context(PDF_PATH)
full_system_prompt = f"{system_prompt}\n\nContext from PDF:\n{pdf_context}"

# Initialize conversation history with the system prompt + PDF context
messages = [{"role": "system", "content": full_system_prompt}]

def get_streaming_response(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})

    full_response = ""
    # Enabled thinking tokens for RAG with gemma4
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True, think=True):
        thinking = chunk["message"].get("thinking", "")
        content = chunk["message"].get("content", "")
        
        if thinking:
            yield ("thinking", thinking)
        if content:
            full_response += content
            yield ("response", content)

    messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    print(f"PDF RAG Chatbot ({MODEL}) ready! Loaded: {PDF_PATH}")
    print("Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot: ", end="", flush=True)
        for text in get_streaming_response(user_input):
            print(text, end="", flush=True)
        print("\n")
