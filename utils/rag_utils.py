# utils/rag_utils.py
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_store(docs):
    """
    Build a FAISS vector store from a list of plain text documents.
    Uses a small/faster HuggingFace sentence-transformer (CPU).
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
        model_kwargs={"device": "cpu"}
    )

    texts = [d if isinstance(d, str) else d.page_content for d in docs]
    vector_store = FAISS.from_texts(texts, embedding=embeddings)
    return vector_store


def build_vector_store(path: str = "vector_store"):
    """
    Load the vector store from disk if present; otherwise build it and save it.
    Returns a FAISS vector store instance.
    """
    if os.path.exists(path):
        # reload using the same embedding object
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
            model_kwargs={"device": "cpu"}
        )
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    else:
        sample_docs = [
            "NeoStats is an AI company focusing on analytics.",
            "RAG stands for Retrieval-Augmented Generation.",
            "Groq models are fast and optimized for inference."
        ]
        vs = create_vector_store(sample_docs)
        vs.save_local(path)
        return vs


def retrieve_answer(query, vector_store, llm):
    docs = vector_store.similarity_search(query, k=3)
    # docs are Document objects; join their content
    context = "\n".join([d.page_content for d in docs])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = llm.invoke(prompt)
    return response.content
