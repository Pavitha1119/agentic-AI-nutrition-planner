"""
Embedder
--------
Wraps the sentence-transformers embedding model used to convert text chunks
into vector embeddings. Shared by vector_store.py and retriever.py.
"""

from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedder() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


if __name__ == "__main__":
    embedder = get_embedder()
    sample_text = "A balanced diet for diabetes should be low in refined sugar."
    vector = embedder.embed_query(sample_text)

    print(f"Embedding model loaded: {EMBEDDING_MODEL_NAME}")
    print(f"Vector length: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")