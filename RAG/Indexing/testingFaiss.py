import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

# Load index
index = faiss.read_index("schema_faiss.index")

# Load docs
with open("schema_docs_lookup.json", "r") as f:
    docs = json.load(f)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

query = "Which table has a column with date and nullable field?"
query_emb = model.encode([query]).astype("float32")

# Search
D, I = index.search(query_emb, k=3)
print("Top results:\n")
for i in I[0]:
    print(docs[i], "\n---\n")
