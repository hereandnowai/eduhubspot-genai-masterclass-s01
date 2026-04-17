import gradio as gr
from chatbot import get_response

def chat_interface(message, history):
    return get_response(message)

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Chatbot with Memory",
    description="I remember what you said earlier in this session!"
)

if __name__ == "__main__":
    demo.launch()
