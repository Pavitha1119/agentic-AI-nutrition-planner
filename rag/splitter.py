"""
Splitter
--------
Takes the Document list from loader.py and splits each page into smaller,
overlapping chunks suitable for embedding and retrieval.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    print(f" Split {len(documents)} pages into {len(chunks)} chunks")
    return chunks


if __name__ == "__main__":
    from loader import load_pdfs

    docs = load_pdfs()
    chunks = split_documents(docs)

    if chunks:
        print("\n--- Preview of first chunk ---")
        print("Source:", chunks[0].metadata.get("source_file"))
        print("Chunk length:", len(chunks[0].page_content))
        print("Content:\n", chunks[0].page_content)