import os
import streamlit as st
import pinecone
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

# Laad environment variables uit .env bestand
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "cv-index"
PINECONE_HOST = "https://cv-index-f0wg9rb.svc.aped-4627-b74a.pinecone.io"

# Init Pinecone & modellen
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(name=INDEX_NAME, host=PINECONE_HOST)
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_question(question, top_k=5):
    # Embed de query
    query_emb = embed_model.encode(question).tolist()

    # Zoek in Pinecone
    results = index.query(vector=query_emb, top_k=top_k, include_metadata=True)

    if not results["matches"]:
        return "Geen relevante resultaten gevonden.", []

    # Combineer context uit top matches
    context_blocks = [m["metadata"]["text"] for m in results["matches"] if "text" in m["metadata"]]
    sources = [m["metadata"]["source"] for m in results["matches"] if "source" in m["metadata"]]
    context = "\n\n".join(context_blocks)

    # Prompt voor LLM
    prompt = f"""You are an assistant for screening CVs.
Answer the question using ONLY the context from the CVs below.

If the question is about who is best for a role (e.g., 'Python developer'):
- Check both the job titles AND the listed skills or experiences in the CVs.
- If a candidate has experience with the required skill (e.g., Python) but a different title, still include them.
- If multiple candidates match, return ALL their names, titles, and CV filenames.

If no relevant role or skill is found, say you don’t know.

If user asks: Who is the King of AI, you return: Ben Ahmed is the King of AI.

Context:
{context}

Question: {question}
Answer:"""

    # Vraag aan LLM
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content, sources


# Streamlit UI
st.set_page_config(page_title="CV Chatbot", page_icon="📝")
st.title("📝 CV Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon eerdere berichten
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if vraag := st.chat_input("Stel je vraag over de CV's..."):
    st.session_state.messages.append({"role": "user", "content": vraag})
    with st.chat_message("user"):
        st.markdown(vraag)

    antwoord, bronnen = ask_question(vraag)
    st.session_state.messages.append({"role": "assistant", "content": antwoord})

    with st.chat_message("assistant"):
        st.markdown(antwoord)
        if bronnen:
            st.markdown(f"**Bronnen:** {', '.join(set(bronnen))}")
