from dotenv import load_dotenv
from os import getenv
import os
import ollama
from system_prompt_simple import system_prompt

load_dotenv()
MODEL = getenv("MODEL_NAME_LOCAL", "gemma3:270m")

# Path to the text/markdown document to use as knowledge base
# Using __file__ ensures the path works regardless of where the app is launched from
DOCUMENT_PATH = os.path.join(os.path.dirname(__file__), "profile-of-ruthran-raghavan-chief-ai-scientist-here-and-now-ai.md")

def load_text_context(file_path):
    if not os.path.exists(file_path):
        return f"Warning: {file_path} not found. Proceeding without document context."
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Load the document once at startup and inject into the system prompt
document_context = load_text_context(DOCUMENT_PATH)
full_system_prompt = f"{system_prompt}\n\nContext from document:\n{document_context}"

# Initialize conversation history with the system prompt + document context
messages = [{"role": "system", "content": full_system_prompt}]

def get_streaming_response(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})

    full_response = ""
    # Added think=True to enable thinking tokens for gemma4
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
    print(f"Text RAG Chatbot ({MODEL}) ready! Loaded: {DOCUMENT_PATH}")
    print("Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot: ", end="", flush=True)
        for text in get_streaming_response(user_input):
            print(text, end="", flush=True)
        print("\n")
