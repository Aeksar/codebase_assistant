from qdrant_client import QdrantClient, models
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.vectorstores.base import VectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4

from config import cfg, logger

def get_store(collection_name: str) -> VectorStore:
    qdrant = QdrantClient(url=cfg.QDRANT_URL)
    embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS_MODEL)
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config={
                "size": 768,
                "distance": models.Distance.COSINE
            }
    )
    return QdrantVectorStore(
        client=qdrant,
        embedding=embeddings,
        collection_name=collection_name
    )


def load_to_store(vectorstore: VectorStore, contents: list[str]):
    logger.info("Load data to store")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " "]
    )
    texts = []
    metadatas = []
    ids = []

    for content in contents:
        chunks = splitter.split_text(content)
        doc_id = str(uuid4())
        for j, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append({"source": f"doc_{doc_id}", "chunk": j})
            ids.append(uuid4().hex)
    vectorstore.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids,
    )
