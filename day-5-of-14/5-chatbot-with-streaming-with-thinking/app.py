import gradio as gr
from chatbot import get_streaming_response

def chat_interface(message, history):
    thinking_text = ""
    response_text = ""

    for kind, text in get_streaming_response(message):
        if kind == "thinking":
            thinking_text += text
            # Show the live thinking process in a collapsible block
            display = f"<details open><summary>💭 Thinking...</summary>\n\n{thinking_text}\n\n</details>"
            yield display
        elif kind == "response":
            response_text += text
            # Once responding, show thinking collapsed + the growing answer
            display = f"<details><summary>💭 Thinking (done)</summary>\n\n{thinking_text}\n\n</details>\n\n{response_text}"
            yield display

demo = gr.ChatInterface(
    fn=chat_interface,
    title="Caramel AI - Your Friendly AI Teacher (Streaming)",
    description="Ask me about Artificial Intelligence! I'll show you my thinking process."
)

if __name__ == "__main__":
    demo.launch()
