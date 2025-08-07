# import numpy as np
# import faiss
# import json
# import os

# # Constants for file paths
# FAISS_INDEX_PATH = "/Users/raghavsharma/Desktop/aiPoweredAssistant/RAG/Indexing/schema_faiss.index"
# METADATA_LOOKUP_PATH = "/Users/raghavsharma/Desktop/aiPoweredAssistant/RAG/Indexing/schema_docs_lookup.json"

# # Load FAISS index
# index = faiss.read_index(FAISS_INDEX_PATH)

# # Load metadata lookup
# with open(METADATA_LOOKUP_PATH, 'r', encoding='utf-8') as f:
#     metadata_lookup = json.load(f)  # expected format: {"0": {...}, "1": {...}, ...}

# def search_top_embedding_with_metadata(generated_embedding: np.ndarray) -> dict:
#     """
#     Searches the FAISS index using the given embedding and returns the metadata for the closest match.

#     Args:
#         generated_embedding (np.ndarray): The embedding to search with (must be float32).

#     Returns:
#         dict: Metadata of the closest matching document.
#     """
#     if not isinstance(generated_embedding, np.ndarray):
#         generated_embedding = np.array(generated_embedding, dtype=np.float32)
#     else:
#         generated_embedding = generated_embedding.astype(np.float32)

#     if index is None:
#         raise ValueError("FAISS index is not initialized.")

#     # Perform the search
#     k = 1
#     distances, indices = index.search(generated_embedding.reshape(1, -1), k)

#     # Process results
#     if len(indices) > 0 and indices[0][0] != -1:
#         top_index = int(indices[0][0])
#         metadata = metadata_lookup.get(str(top_index))
#         if metadata:
#             return metadata
#         else:
#             return {"error": f"No metadata found for index {top_index}"}
    
#     return {"error": "No matching embedding found."}



import numpy as np
import faiss
import json
import os

# Constants for file paths
FAISS_INDEX_PATH = "/Users/raghavsharma/Desktop/aiPoweredAssistant/RAG/Indexing/schema_faiss.index"
METADATA_LOOKUP_PATH = "/Users/raghavsharma/Desktop/aiPoweredAssistant/RAG/Indexing/schema_docs_lookup.json"

# Load FAISS index
index = faiss.read_index(FAISS_INDEX_PATH)

# Load metadata lookup
with open(METADATA_LOOKUP_PATH, 'r', encoding='utf-8') as f:
    metadata_lookup = json.load(f)  # expected format: {"0": {...}, "1": {...}, ...}

def search_top_embedding_with_metadata(generated_embedding: np.ndarray) -> dict:
    if not isinstance(generated_embedding, np.ndarray):
        generated_embedding = np.array(generated_embedding, dtype=np.float32)
    else:
        generated_embedding = generated_embedding.astype(np.float32)

    if index is None:
        raise ValueError("FAISS index is not initialized.")

    k = 1
    distances, indices = index.search(generated_embedding.reshape(1, -1), k)

    if len(indices) > 0 and indices[0][0] != -1:
        top_index = int(indices[0][0])
        try:
            metadata = metadata_lookup[top_index]  # ✅ Use list indexing
            return {"context": metadata}
        except IndexError:
            return {"error": f"Index {top_index} out of range in metadata list."}

    return {"error": "No matching embedding found."}