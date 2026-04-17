from dotenv import load_dotenv
from os import getenv
import ollama
from system_prompt import system_prompt

load_dotenv()
MODEL = getenv("MODEL_NAME_LOCAL", "gemma3:270m")

# Initializing context with the system prompt
messages = [{"role": "system", "content": system_prompt}]

def get_streaming_response(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})

    full_response = ""
    # Removed think=True as it is not supported by models like gemma3:270m
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True):
        content = chunk["message"].get("content", "")
        if content:
            full_response += content
            yield content

    messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    print(f"Chatbot ({MODEL}) ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot: ", end="", flush=True)
        for text in get_streaming_response(user_input):
            print(text, end="", flush=True)
        print("\n")
