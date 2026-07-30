"""
Retriever
---------
Given a natural-language query, searches the persisted vector store and
returns the most relevant chunks. Called by the Disease RAG Agent.
"""

from langchain_core.documents import Document

from vector_store import load_vector_store


def retrieve_relevant_chunks(query: str, k: int = 5) -> list[Document]:
    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results


def retrieve_with_scores(query: str, k: int = 5) -> list[tuple[Document, float]]:
    vector_store = load_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    return results


def format_chunks_for_context(chunks: list[Document]) -> str:
    formatted = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.metadata.get("source_file", "unknown")
        formatted.append(f"[{i}] (Source: {source})\n{chunk.page_content}")
    return "\n\n".join(formatted)


if __name__ == "__main__":
    test_query = "What foods should a diabetic patient avoid?"

    print(f"🔍 Query: {test_query}\n")

    results = retrieve_with_scores(test_query, k=3)
    for doc, score in results:
        print(f"Score: {score:.4f} | Source: {doc.metadata.get('source_file')}")
        print(doc.page_content[:200])
        print("-" * 60)