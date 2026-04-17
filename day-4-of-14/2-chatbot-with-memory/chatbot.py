from dotenv import load_dotenv
from os import getenv
from langchain_ollama import ChatOllama

load_dotenv()
llm = ChatOllama(model=getenv("MODEL_NAME_LOCAL", "gemma4:latest"))

context = ""

def get_response(user_input):
    global context
    context += f"User: {user_input}\n"
    response = llm.invoke(context)
    context += f"Assistant: {response.content}\n"
    return response.content

if __name__ == "__main__":
    print("Chatbot with Memory ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print(f"Bot: {get_response(user_input)}\n")
