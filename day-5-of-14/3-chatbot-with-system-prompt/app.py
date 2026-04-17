import gradio as gr
from chatbot import get_response

def chat_interface(message, history):
    return get_response(message)

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Caramel AI - Your Friendly AI Teacher",
    description="Ask me about Artificial Intelligence! I have been programmed to respond like a friendly AI teacher."
)

if __name__ == "__main__":
    demo.launch()
