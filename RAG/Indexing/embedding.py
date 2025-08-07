from sentence_transformers import SentenceTransformer
import json

# Load docs
with open("schema_metadata.txt", "r") as f:
    documents = f.read().split("\n\n")  # assumes 1 doc per section

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(documents)

# Save both docs and embeddings
with open("schema_embeddings.json", "w") as f:
    json.dump({
        "documents": documents,
        "embeddings": [emb.tolist() for emb in embeddings]
    }, f)

print("✅ Embeddings saved to 'schema_embeddings.json'")
