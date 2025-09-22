import pinecone
from sentence_transformers import SentenceTransformer
import pdfplumber
import os

# Config
PINECONE_API_KEY = "pcsk_6cyHFj_6JESus8R1TWetFmH5aHVgwftJ8nFLHsffwvjTFHWgrns4rqC3yWweTajERGcDy9"
INDEX_NAME = "cv-index"

# Init Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Embedding model
print("Model laden (kan 1 minuut duren bij eerste keer)...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# PDF map
PDF_DIR = "CVS"

def load_pdfs(pdf_dir):
    docs = []
    for fname in os.listdir(pdf_dir):
        if fname.endswith(".pdf"):
            path = os.path.join(pdf_dir, fname)
            with pdfplumber.open(path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
            docs.append({"source": fname, "text": text})
    return docs

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Laad alle documenten
documents = load_pdfs(PDF_DIR)

records = []
for doc in documents:
    chunks = chunk_text(doc["text"], chunk_size=400, overlap=50)
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        records.append({
            "id": f"{doc['source']}_chunk{i}",
            "values": embedding,
            "metadata": {"source": doc["source"], "text": chunk}
        })

# Upload naar Pinecone
if records:
    index.upsert(vectors=records)
    print(f"{len(records)} vectors succesvol geüpload naar Pinecone index '{INDEX_NAME}'")
else:
    print("Geen tekst gevonden in de PDF's!")
