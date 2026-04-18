from dotenv import load_dotenv
from os import getenv
import ollama
from system_prompt import system_prompt

load_dotenv()
MODEL = getenv("MODEL_NAME_LOCAL", "gemma4:latest")

# Initializing context with the system prompt
messages = [{"role": "system", "content": system_prompt}]

def get_streaming_response(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})

    full_response = ""
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
    print("Chatbot with Streaming ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot: ", end="", flush=True)
        for kind, text in get_streaming_response(user_input):
            print(text, end="", flush=True)
        print("\n")
