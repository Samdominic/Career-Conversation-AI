Sure! Here's a clean and complete `README.md` file for your project, assuming it's called **Career Conversation AI** and uses Gradio, local OpenAI-compatible models, and Pushover notifications:

---

````markdown
# Career Conversation AI

An interactive AI assistant powered by LLaMA and Gradio that can respond using a personal profile PDF, answer general questions, and trigger real-time notifications via Pushover. Designed to be self-hosted using an OpenAI-compatible local model endpoint (e.g., Ollama).

## 🚀 Features

- 🧠 AI assistant that answers questions using uploaded profile PDF
- 📄 Tool-calling support to:
  - Log unanswered questions
  - Log user contact details
- 📢 Real-time notifications via [Pushover](https://pushover.net/)
- 📎 PDF extraction using `pypdf`
- 💬 Web UI using [Gradio ChatInterface](https://www.gradio.app/guides/creating-a-chatbot)

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Samdominic/Career-Conversation-AI.git
cd Career-Conversation-AI
````

### 2. Install Dependencies

Make sure you have Python 3.10+ and `uv` or `pip`:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

> If using `pip` instead:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Environment Variables

Create a `.env` file:

```env
PUSHOVER_TOKEN=your_pushover_api_token
PUSHOVER_USER=your_pushover_user_key
```

> 🔒 This file is ignored from Git via `.gitignore`.

---

### 4. Add Your PDF Profile

Place your profile PDF in the `assets/` folder and rename it to `Profile.pdf`:

```
assets/Profile.pdf
```

---

### 5. Run the App

```bash
python main.py
```

This will launch the Gradio web interface in your browser.

---

## 🧪 Tool Functions

The assistant can invoke tools to:

* Log unanswered questions (`log_unanswered_question`)
* Log user contact info (`log_user_details`)

These are handled by your local Python code and trigger notifications using Pushover.

---

## 🤖 Model Endpoint

This app uses a local OpenAI-compatible endpoint, such as:

* [Ollama](https://ollama.com/)
* [LM Studio](https://lmstudio.ai/)
* [OpenRouter](https://openrouter.ai/) (if deployed)

Configured in code:

```python
OpenAI(base_url="http://localhost:11434/v1", api_key="anything")
```

> Adjust as needed based on your backend.

---

## 📦 Dependencies

* [`openai`](https://pypi.org/project/openai/)
* [`pypdf`](https://pypi.org/project/pypdf/)
* [`gradio`](https://gradio.app/)
* [`python-dotenv`](https://pypi.org/project/python-dotenv/)
* [`requests`](https://pypi.org/project/requests/)

Install manually if needed:

```bash
uv pip install openai gradio pypdf python-dotenv requests
```

---

## 📄 License

MIT License

---

## ✍️ Author

Built by [@Samdominic](https://github.com/Samdominic)
