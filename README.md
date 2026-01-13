# PromptForge: The Ultimate Prompt Optimizer

> [!CAUTION]
> **PRE-ALPHA VERSION**: This project is currently in a pre-alpha stage and is an active work in progress. Features, APIs, and interfaces are subject to change without notice. Use with discretion.

> [!WARNING]
> **DISCLAIMER**: Remote LLM backend providers (Anthropic, Google Gemini, Groq) have been implemented but **have not been fully tested yet**. Please report any connection or generation issues.

PromptForge is a high-end, local-first Desktop Application designed to engineer and optimize prompts using a variety of LLM backends. It leverages a "Meta-Prompting" technique to break down raw ideas into structured, high-performance prompts adhering to best practices (CRISPE, Chain-of-Thought).

## 🚀 Features

-   **Multi-Backend Support**:
    -   **Local**: LM Studio (OpenAI Compatible), Ollama, Llama.cpp (Native GGUF).
    -   **Cloud**: Anthropic (Claude), Google Gemini, Groq (Llama 3 on LPU).
-   **Advanced Prompt Engineering**: Breaks prompts into 10 structured elements:
    -   Persona, Context, Instruction, Constraints, Format, Exemplars, Tone, Delimiters, Data, Technique.
-   **Hardware Monitor**: Real-time CPU and GPU usage tracking in the sidebar.
-   **Secure Storage**: API Keys are safely stored in your OS Keychain (Windows Credential Manager / macOS Keychain).
-   **Local History**: All optimization sessions are saved locally to an SQLite database.
-   **Modern UI**: Built with CustomTkinter for a sleek, dark-mode experience.

## 🛠️ Prerequisites

-   **Python 3.10+** installed.
-   **Git** installed.
-   *(Optional)* **LM Studio** or **Ollama** running locally.
-   *(Optional)* **C++ Build Tools** (Visual Studio) if you want GPU acceleration for Llama.cpp on Windows.

## 📦 Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/ahmadzkn/prompt-forge.git
    cd prompt-forge
    ```

2.  **Run Setup Script**:
    This script creates a virtual environment and installs all dependencies.
    ```powershell
    # Windows
    python setup_env.py
    ```

    *Alternatively, manual setup:*
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

## 🎮 Usage

1.  **Launch the Application**:
    ```powershell
    .\venv\Scripts\python main.py
    ```

2.  **Configure Backend (Sidebar)**:
    -   **LLM Studio**: Ensure LM Studio is running (Server ON). Default URL: `http://localhost:1234/v1`.
    -   **Ollama**: Ensure Ollama is running. Default Host: `http://localhost:11434`.
    -   **Llama.cpp**: Select this and paste the absolute path to your `.gguf` model file.
    -   **Cloud (Anthropic/Gemini/Groq)**: Select the provider and enter your API Key. It will be saved securely.

3.  **Optimize**:
    -   Type your raw idea in the "Raw Prompt" box.
    -   Click **Optimize Prompt**.
    -   Review the "Structured Elements" and the final "Optimized Prompt".

## 🧩 Project Structure

```
prompt-forge/
├── src/
│   ├── backends/       # Provider implementations (OpenAI, Ollama, Llama.cpp, etc.)
│   ├── utils/          # Hardware monitor, Credential manager
│   ├── gui.py          # CustomTkinter UI
│   ├── optimizer.py    # Core optimization logic
│   └── database.py     # SQLite session management
├── main.py             # Entry point
├── requirements.txt    # Usage dependencies
├── setup_env.py        # Environment setup script
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📜 License

MIT License.
