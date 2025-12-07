# 📘 **Smart-QA — Text Summarization, Extraction & Question-Answering CLI**

Smart-QA is a command-line tool for interacting with Google’s Gemini API to:

* **Summarize text**
* **Extract factual entities as structured JSON**
* **Ask questions strictly based on a given text** (no hallucination allowed)

It supports file input (`.txt`, `.md`, `.docx`, `.pdf`), multi-line stdin input, and automatic output saving.

Smart-QA is built with:

* Python 3.11+
* `google-genai`
* A custom retry system with exponential backoff
* Helpful custom exceptions
* Simple CLI built with `argparse`

---

# 🚀 **Features**

### 🔹 Summarization

Produces a concise, high-quality summary following strict rules (no external info, no hallucination).

### 🔹 Entity Extraction

Extracts only **explicit facts** in JSON form — zero inference allowed.

### 🔹 Question Answering

Creates a persistent Gemini chat session configured to answer **only from provided text**, responding *“I don’t know”* when information is not found.

### 🔹 File Support

Reads:

* `.txt`
* `.md`
* `.docx`
* `.pdf`

### 🔹 Automatic Retry Logic

Handles:

* Rate limits (`429`)
* Server errors (`5xx`)
* Connection errors

Uses exponential backoff.

### 🔹 Output Saving

Save:

* Summaries → `output.txt`
* Extracted JSON → `output.json`

---

# 📦 **Project Structure**

```
smart_qa/
│
├── client.py               # Gemini client + retry logic
├── helper.py               # File reading & saving utilities
├── custom_exceptions.py    # App-specific exceptions
│
├── main.py                 # CLI entrypoint
│
├── configs/
│   └── logging.py          # Logging configuration
│
└── tests/                  # (Optional) test suite
```

---

# 🔧 **Installation**

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/smart-qa-project.git
cd smart-qa
```

### 2. Install dependencies

```bash
poetry install
```

### 4. Set up environment variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

# 🖥️ **Usage (CLI)**

Run the CLI:

```bash
poetry run python main.py
```

Then choose one of the modes:

```
What would you like to do? [summarize | ask | extract] or [quit]:
```

Arguments:

| Flag            | Description                       |
| --------------- | --------------------------------- |
| `--file PATH`   | Read input from a file            |
| `--save PATH`   | Directory to save output          |
| `--clear-cache` | Clear cached results              |

---

# 🛠️ **Internal Components**

## **`LLMClient`**

Methods:

| Method                   | Description                              |
| ------------------------ | ---------------------------------------- |
| `summarize(text)`        | Summarizes text using Gemini             |
| `extract_entities(text)` | Returns JSON dict of explicit facts      |
| `create_chat(text)`      | Builds a Gemini chat session             |
| `ask(question, chat)`    | Asks a question via a persistent session |
| `_make_request`          | Low-level request with retry logic       |


---

# 🧪 **Testing**

If you add a test suite:

```bash
poetry run pytest
```
---

# 📄 **License**

MIT License © 2025
