import fitz
import gradio as gr
import requests
import textwrap

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"
CHUNK_SIZE = 1200


# ------------------ PDF TEXT ------------------
def extract_pdf_text(files):
    text = ""
    for f in files:
        doc = fitz.open(f.name)
        for page in doc:
            text += page.get_text()
    return text


# ------------------ CHUNKING ------------------
def chunk_text(text):
    return textwrap.wrap(text, CHUNK_SIZE)


# ------------------ RETRIEVER ------------------
def retrieve_chunks(chunks, query, top_k=3):
    scores = []
    for c in chunks:
        score = sum(word in c.lower() for word in query.lower().split())
        scores.append((score, c))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in scores[:top_k]]


# ------------------ OLLAMA CALL ------------------
def ask_ollama(system, user):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)
    data = r.json()

    if "message" not in data:
        return f"Ollama Error: {data.get('error', 'Unknown error')}"

    return data["message"]["content"]


# ------------------ CHAT LOGIC ------------------
def chat(user_question, history, pdf_files, stored_chunks):
    if not pdf_files:
        return history, history, stored_chunks  # Keep same format

    if stored_chunks is None:
        text = extract_pdf_text(pdf_files)
        stored_chunks = chunk_text(text)

    relevant = retrieve_chunks(stored_chunks, user_question)
    context = "\n\n---\n\n".join(relevant)

    system_prompt = (
        "You are a PDF assistant. Answer ONLY from the text below.\n\n"
        f"{context}"
    )

    answer = ask_ollama(system_prompt, user_question)

    # --- Correct format for Gradio Chatbot ---
    if history is None:
        history = []

    history.append({"role": "user", "content": user_question})
    history.append({"role": "assistant", "content": answer})

    # Gradio Chatbot expects same history for output
    return history, history, stored_chunks


# ------------------ UI ------------------
with gr.Blocks(title="ChatPDF+") as ui:
    gr.Markdown(
        "<h1 style='text-align: center;'>📄 ChatPDF+</h1>",
        elem_id="main_heading"
    )
 
    with gr.Row():
        # Sidebar for chat history
        with gr.Column(scale=5, min_width=250, visible=True) as sidebar:
            gr.Markdown("##  Chat History")
            chatbot = gr.Chatbot(label="🤖 PDF Assistant", height=500, elem_classes="scrollable-chat")

        # Main column for inputs
        with gr.Column(scale=5):
            gr.Markdown("")
            gr.Markdown("## Upload PDFs and ask your questions below ✨")
            
            pdf_files = gr.File(file_count="multiple", file_types=[".pdf"], label="📎 Upload PDF(s)")
            question = gr.Textbox(label="💬 Ask something", placeholder="Type your question here... ✍️")

            with gr.Row():
                analyze_btn = gr.Button(" Analyze")
                clear_btn = gr.Button(" Clear Chat")


    stored_chunks = gr.State()

    # --- Button actions ---
    question.submit(chat, inputs=[question, chatbot, pdf_files, stored_chunks], outputs=[chatbot, chatbot, stored_chunks])
    analyze_btn.click(chat, inputs=[question, chatbot, pdf_files, stored_chunks], outputs=[chatbot, chatbot, stored_chunks])
    clear_btn.click(lambda: ("", [], None), inputs=[], outputs=[question, chatbot, stored_chunks])
    
# --- Custom CSS for scrollable chat ---
css = """
.scrollable-chat .overflow-y-auto {
    max-height: 500px;
    overflow-y: auto;
}
"""
ui.launch(css=css)





