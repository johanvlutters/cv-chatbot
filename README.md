# CV Chatbot

This project is a simple chatbot that allows you to query information from a collection of CVs (PDFs).  
The CVs are processed into embeddings, stored in a Pinecone index, and queried via an LLM (OpenAI GPT models).  
The project also includes a clean chat interface built with Streamlit.  

---

## Features
- Upload and process CVs (PDF format).
- Store and search CV embeddings with Pinecone.
- Ask questions about the CVs in natural language.
- Simple Streamlit web interface with Q&A display.
- Answers are based **only** on the information found in the CVs.

---

## Tech Stack
- [Python 3.9+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) for the chat UI
- [Pinecone](https://www.pinecone.io/) for vector storage
- [SentenceTransformers](https://www.sbert.net/) for embeddings
- [OpenAI API](https://platform.openai.com/) for LLM answers
- [pdfplumber](https://github.com/jsvine/pdfplumber) for extracting text from PDFs

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/johanvlutters/cv-chatbot.git
cd cv-chatbot

2. Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

2. Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

3. 3. Install dependencies
pip install -r requirements.txt

4. Set environment variables
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here

5. Prepare Pinecone Index
Make sure you have a Pinecone index created (default name in code is cv-index).
5. Prepare Pinecone Index

Make sure you have a Pinecone index created (default name in code is cv-index).

Usage
Upload CVs to Pinecone
python upload_to_pinecone.py

Query CVs from the terminal
python query_pinecone.py

Run the Chat Interface
streamlit run app.py


Then open the provided URL (usually http://localhost:8501) in your browser.

File Structure
cv-chatbot/
│── app.py                 # Streamlit app (chat interface)
│── extract_pdfs.py        # PDF text extraction helper
│── upload_to_pinecone.py  # Uploads CVs to Pinecone
│── query_pinecone.py      # Query Pinecone via terminal
│── cvs/                   # Folder containing CV PDFs
│── .gitignore
│── requirements.txt
│── README.md

Roadmap / Improvements
- Support uploading CVs dynamically via the UI.
- Show source CV(s) alongside the answers.
- Add authentication for the app.
- Optimize embedding and search performance.

License

This project is open source and available under the MIT License.