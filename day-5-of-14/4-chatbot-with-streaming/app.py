import gradio as gr
from chatbot import get_streaming_response

def chat_interface(message, history):
    partial_message = ""
    for chunk in get_streaming_response(message):
        partial_message += chunk
        yield partial_message

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Caramel AI - Your Friendly AI Teacher (Streaming)",
    description="Ask me about Artificial Intelligence!"
)

if __name__ == "__main__":
    demo.launch()