"""
Vector Store
------------
Builds (or loads) a persistent ChromaDB vector store from the document
chunks, using the embedding model from embedder.py.
"""

import os
from langchain_chroma import Chroma
from langchain_core.documents import Document

from embedder import get_embedder

PERSIST_DIRECTORY = "chroma_db"
COLLECTION_NAME = "nutrition_knowledge_base"


def build_vector_store(chunks: list[Document]) -> Chroma:
    embedder = get_embedder()

    print(f"🔨 Building vector store with {len(chunks)} chunks... (this may take a few minutes)")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )

    print(f"✅ Vector store built and saved to '{PERSIST_DIRECTORY}/'")
    return vector_store


def load_vector_store() -> Chroma:
    if not os.path.exists(PERSIST_DIRECTORY):
        raise FileNotFoundError(
            f"No vector store found at '{PERSIST_DIRECTORY}/'. "
            "Run vector_store.py directly first to build it."
        )

    embedder = get_embedder()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedder,
        persist_directory=PERSIST_DIRECTORY,
    )
    return vector_store


if __name__ == "__main__":
    from loader import load_pdfs
    from splitter import split_documents

    docs = load_pdfs()
    chunks = split_documents(docs)
    build_vector_store(chunks)