from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once (outside the function)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding_from_prompt(prompt: str) -> np.ndarray:
    """
    Generates embeddings for the given prompt using SentenceTransformer,
    returning a NumPy array of type float32 suitable for FAISS.
    """
    try:
        embedding = model.encode(prompt)
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {e}")

