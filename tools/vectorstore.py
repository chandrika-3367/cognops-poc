import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle

# Global constants for vectorstore
VECTORSTORE_DIR = "vectorstore"
VECTORSTORE_INDEX = os.path.join(VECTORSTORE_DIR, "faiss_index")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)


def ensure_vectorstore_dir():
    if not os.path.exists(VECTORSTORE_DIR):
        os.makedirs(VECTORSTORE_DIR)


def save_vectorstore(vstore: FAISS) -> None:
    ensure_vectorstore_dir()
    vstore.save_local(VECTORSTORE_INDEX)
    with open(os.path.join(VECTORSTORE_DIR, "embeddings.pkl"), "wb") as f:
        pickle.dump(embedding_model, f)


def load_vectorstore() -> FAISS:
    with open(os.path.join(VECTORSTORE_DIR, "embeddings.pkl"), "rb") as f:
        loaded_embeddings = pickle.load(f)
    return FAISS.load_local(VECTORSTORE_INDEX, loaded_embeddings)


def embed_documents_from_texts(texts: List[str]) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk)
            for text in texts for chunk in splitter.split_text(text)]
    vstore = FAISS.from_documents(docs, embedding_model)
    save_vectorstore(vstore)
    return vstore


def search_similar_docs(query: str, k: int = 5) -> List[Document]:
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search(query, k=k)
