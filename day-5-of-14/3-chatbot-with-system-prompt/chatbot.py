from dotenv import load_dotenv
from os import getenv
from langchain_ollama import ChatOllama
from system_prompt import system_prompt
# from observability import measure_performance

load_dotenv()
llm = ChatOllama(
    model=getenv("MODEL_NAME_LOCAL", "gemma4:latest"),
    num_ctx=4096,
    temperature=0.0,
    )

# Initializing context with the system prompt
context = f"System: {system_prompt}\n"

# @measure_performance
def get_response(user_input):
    global context
    context += f"User: {user_input}\n"
    response = llm.invoke(context)
    context += f"Assistant: {response.content}\n"
    return response.content

if __name__ == "__main__":
    print("Chatbot with System Prompt ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print(f"Bot: {get_response(user_input)}\n")