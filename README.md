# 📄 ChatPDF+

ChatPDF+ is a local, privacy-preserving PDF Question Answering system that allows users to upload one or more PDF documents and ask questions about their content. The system uses a Retrieval-Augmented Generation (RAG) approach to ensure that answers are generated strictly from the uploaded documents, reducing hallucinations commonly seen in general-purpose language models.

---

## 🚀 Features

- Upload and query multiple PDF documents
- Lightweight document retrieval mechanism
- Local LLM inference using Ollama (LLaMA 3.2)
- Offline and privacy-friendly (no cloud APIs)
- Chat-based interactive UI using Gradio
- Answers restricted to document content only

---

## 🧠 How It Works
PDF Upload
↓
Text Extraction (PyMuPDF)
↓
Text Chunking
↓
Relevant Chunk Retrieval
↓
Context Injection
↓
Local LLM (Ollama)
↓
Answer to User


The system explicitly instructs the language model to answer only from the retrieved document context.

---

## 🏗️ System Design

### PDF Text Extraction
Text is extracted from uploaded PDFs page by page using PyMuPDF (fitz).

### Text Chunking
Extracted text is split into manageable chunks to fit within the LLM context window.

### Retrieval
A keyword-based scoring method selects the most relevant chunks for a given user query.

### LLM Inference
A locally hosted LLaMA 3.2 (1B) model is accessed through Ollama to generate responses grounded in document context.

### User Interface
The application uses Gradio to provide a chat-style interface with conversation history.

---

## 🛠️ Tech Stack

- Python
- PyMuPDF (fitz)
- Gradio
- Ollama
- LLaMA 3.2 (1B)
- REST APIs
- Prompt Engineering
- Retrieval-Augmented Generation (RAG)

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Ollama installed and running

### Install Ollama model
```bash
ollama pull llama3.2:1b

### Install Python dependencies
pip install gradio pymupdf requests

### Run the application
python app.py
