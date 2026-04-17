# Chatbot Architecture (Without Memory)

This project consists of a simple local chatbot interface built with **Gradio**, orchestrating **LangChain** to communicate with a local **Ollama** model server.

## Architecture Diagram

```mermaid
graph TD
    User([User]) -->|User Input| UI[Gradio Web UI]
    UI -->|String Prompt| Chatbot[Chatbot Logic: chatbot.py]
    
    subgraph "Local Environment"
        Chatbot -->|Load Env| Dotenv[.env File]
        Chatbot -->|Invoke| LangChain[LangChain Ollama Wrapper]
        
        subgraph "Ollama Service"
            LangChain -->|HTTP API Request| OllamaServer[Ollama Server]
            OllamaServer -->|Loaded in VRAM| Model[(Local LLM: Gemma/Llama)]
        end
    end
    
    Model -->|Generated Response| OllamaServer
    OllamaServer -->|HTTP Answer| LangChain
    LangChain -->|Text Result| Chatbot
    Chatbot -->|Result Output| UI
    UI -->|Bot Message| User
    
    style User fill:#66ccff,stroke:#333,stroke-width:2px
    style UI fill:#ff9900,color:#fff
    style Model fill:#00ccff,color:#fff
    style OllamaServer fill:#eeeeee,stroke:#666,stroke-dasharray: 5 5
```

## Key Components:
1.  **Gradio (UI)**: Provides a simple web interface for sending and receiving messages.
2.  **LangChain (Framework)**: Standardizes how input is passed to the LLM and processes output.
3.  **ChatOllama (Connector)**: Communicates with your locally running Ollama instance.
4.  **Ollama (Local Inference)**: Runs the actual AI model on your machine's hardware.
