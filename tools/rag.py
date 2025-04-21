from typing import List, Tuple
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


def dynamic_rag_qa(query: str, all_issues: List[tuple]) -> Tuple[List[str], List[str], List[float]]:
    """Perform similarity search over the current GitHub issues without relying on saved vectorstore."""

    # Step 1: Prepare chunked documents
    texts = [f"{title}\n{body}" for title, body in all_issues]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk, metadata={"source": title})
            for title, body in all_issues
            for chunk in splitter.split_text(f"{title}\n{body}")]

    # Step 2: Embed and build vector store
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Step 3: Perform similarity search with scores
    similar_docs_with_scores = vectorstore.similarity_search_with_score(
        query, k=5)

    # Step 4: Extract fields
    context_snippets = [doc.page_content for doc,
                        _ in similar_docs_with_scores]
    sources = [doc.metadata.get("source", "Unknown")
               for doc, _ in similar_docs_with_scores]
    confidence_scores = [float(f"{score:.2f}")
                         for _, score in similar_docs_with_scores]

    return context_snippets, sources, confidence_scores
