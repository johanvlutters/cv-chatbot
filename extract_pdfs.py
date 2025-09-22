import os
import pdfplumber

def load_pdfs(folder="cvs"):
    documents = []
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            text = ""
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            documents.append({"text": text, "source": filename})
    return documents

if __name__ == "__main__":
    documents = load_pdfs("cvs")
    print(f"{len(documents)} CV's gevonden")
    for d in documents[:2]:
        print("----", d["source"], "----")
        print(d["text"][:300], "...\n")
