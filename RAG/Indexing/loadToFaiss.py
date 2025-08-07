import json
import faiss
import numpy as np

# Load data
with open("schema_embeddings.json", "r") as f:
    data = json.load(f)

docs = data["documents"]
embs = np.array(data["embeddings"]).astype("float32")

# Create FAISS index
dimension = embs.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embs)

# Optional: Save FAISS index
faiss.write_index(index, "schema_faiss.index")

# Save docs mapping
with open("schema_docs_lookup.json", "w") as f:
    json.dump(docs, f)

print("✅ FAISS index created and saved as 'schema_faiss.index'")
