# PromptForge ⚡
**The Ultimate Local-First Prompt Optimizer**

PromptForge is a high-end, secure, and local desktop application designed to turn raw ideas into prompt engineering masterpieces. Built with Python and CustomTkinter, it leverages **LM Studio** (and other local LLMs) to analyze, restructure, and optimize your prompts using valid frameworks like CRISPE and Chain-of-Thought.

![PromptForge UI](docs/screenshot.png) *(Add a screenshot here)*

## 🚀 Features
- **Local Intelligence**: Uses your local GPU (via LM Studio) for 100% privacy.
- **Meta-Prompt Engine**: Automatically decomposes prompts into key elements (Persona, Context, Constraints, etc.).
- **Structured Output**: View and edit each component of the prompt individually.
- **Persistent History**: Everything is saved to a local SQLite database.
- **Modern UI**: Sleek dark mode interface built with CustomTkinter.

## 🛠️ Prerequisites
- **Python 3.10+**
- **LM Studio**: Running locally (default: `http://localhost:1234`).
  - *Note: Ensure you have a model loaded in LM Studio and the Server is turned ON.*

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PromptForge.git
   cd PromptForge
   ```

2. **Run the Setup Script**
   This handles virtual environment creation and dependency installation automatically.
   ```bash
   python setup_env.py
   ```

## 🖥️ Usage

1. **Launch the App**
   ```bash
   # Windows
   venv\Scripts\python main.py
   
   # Linux/Mac
   ./venv/bin/python main.py
   ```

2. **Optimize**
   - Paste your raw prompt.
   - Click **Optimize**.
   - Watch as your prompt is reverse-engineered and polished.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
