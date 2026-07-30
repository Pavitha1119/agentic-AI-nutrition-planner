"""
Disease RAG Agent
------------------
Given a user's medical condition(s), retrieves relevant guideline chunks
from the knowledge base and asks the LLM to summarize actionable dietary
advice — grounded in the retrieved sources.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rag"))
from retriever import retrieve_relevant_chunks, format_chunks_for_context

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

DISEASE_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Disease Guideline Agent for a nutrition planning system.

You are given:
1. A user's medical condition(s)
2. Relevant excerpts retrieved from trusted nutrition guideline documents

Your job: summarize clear, practical dietary DOs and DON'Ts for this user,
based ONLY on the provided context. Do not invent facts not present in the
context. If the context is insufficient, say so honestly.

Keep the response concise — a short list of dos and don'ts, not an essay."""),
    ("human", """Medical condition(s): {diseases}

Retrieved guideline excerpts:
{context}

Summarize the key dietary dos and don'ts for this condition.""")
])


def get_disease_guidance(diseases: list[str], k: int = 5) -> dict:
    diseases = [d for d in diseases if d and d != "None"]
    if not diseases:
        return {"guidance": "No medical conditions specified.", "sources": []}

    all_chunks = []
    for disease in diseases:
        query = f"dietary guidelines and food recommendations for {disease}"
        chunks = retrieve_relevant_chunks(query, k=k)
        all_chunks.extend(chunks)

    context = format_chunks_for_context(all_chunks)
    sources = sorted(set(c.metadata.get("source_file", "unknown") for c in all_chunks))

    chain = DISEASE_AGENT_PROMPT | llm
    response = chain.invoke({
        "diseases": ", ".join(diseases),
        "context": context,
    })

    return {
        "guidance": response.content,
        "sources": sources,
    }


if __name__ == "__main__":
    result = get_disease_guidance(["Diabetes"])
    print("=== Dietary Guidance ===")
    print(result["guidance"])
    print("\n=== Sources ===")
    for src in result["sources"]:
        print("-", src)