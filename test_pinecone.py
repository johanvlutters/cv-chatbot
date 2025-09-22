import pinecone

PINECONE_API_KEY = "pcsk_pcS1o_Tk7SB7LVK28PUqwbpsciffjoUMXadk2sbrLVaEe32C6WjxQ1VoE5qCN2ZQneaHz"  # vervang met jouw key
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(
    "cv-index",
    host="https://cv-index-f0wg9rb.svc.aped-4627-b74a.pinecone.io"
)

print(index.describe_index_stats())
