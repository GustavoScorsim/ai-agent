import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.agent.helpers import get_embeddings
from app.rag.loaders import carregar_documentos

CHROMA_DIR = "chroma_db"
COLLECTION = "documentos"


def ingerir(pasta: str = "docs") -> None:
    docs = carregar_documentos(pasta)
    if not docs:
        print(f"Nenhum documento encontrado em '{pasta}'.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    if Path(CHROMA_DIR).exists():
        shutil.rmtree(CHROMA_DIR)  # recria o índice do zero

    Chroma.from_documents(
        chunks,
        get_embeddings(),
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
    )
    print(f"{len(docs)} documento(s) -> {len(chunks)} chunks indexados em '{CHROMA_DIR}'.")


if __name__ == "__main__":
    ingerir()