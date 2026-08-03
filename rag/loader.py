

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

KNOWLEDGE_BASE_DIR = "knowledge_base"


def load_pdfs(folder_path: str = KNOWLEDGE_BASE_DIR) -> list[Document]:
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Knowledge base folder not found: {folder_path}")

    all_documents: list[Document] = []
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f" No PDF files found in '{folder_path}'.")
        return all_documents

    for filename in pdf_files:
        file_path = os.path.join(folder_path, filename)
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()

            for page in pages:
                page.metadata["source_file"] = filename

            all_documents.extend(pages)
            print(f" Loaded {len(pages)} pages from {filename}")

        except Exception as e:
            print(f" Failed to load {filename}: {e}")

    print(f" Total pages loaded: {len(all_documents)}")
    return all_documents


if __name__ == "__main__":
    docs = load_pdfs()
    if docs:
        print("\n--- Preview of first document ---")
        print("Source:", docs[0].metadata.get("source_file"))
        print("Page content (first 300 chars):\n", docs[0].page_content[:300])