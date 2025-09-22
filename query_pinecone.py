import os
import pinecone
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Config: keys uit environment variabelen halen
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "cv-index"

# Check of keys wel geladen zijn
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is niet gezet. Gebruik: export PINECONE_API_KEY='...'")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is niet gezet. Gebruik: export OPENAI_API_KEY='...'")

# Init Pinecone en model
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_question(question, top_k=5):
    query_emb = embed_model.encode(question).tolist()
    results = index.query(vector=query_emb, top_k=top_k, include_metadata=True)

    if not results["matches"]:
        return "Geen relevante resultaten gevonden in de CV's."
    
    context = "\n\n".join(
        [m["metadata"]["text"] for m in results["matches"] if "text" in m["metadata"]]
    )
    
    prompt = f"""You are an assistant for screening CVs.
Answer the question using ONLY the context from the CVs below. 
If you are not sure, say you don’t know.

Context:
{context}

Question: {question}
Answer:"""
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    vraag = input("Stel je vraag over de CV's: ")
    antwoord = ask_question(vraag)
    print("\nAntwoord:", antwoord)
