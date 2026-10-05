from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def carregar_documentos(pasta: str = "docs") -> list[Document]:
    docs: list[Document] = []
    for arquivo in Path(pasta).rglob("*"):
        ext = arquivo.suffix.lower()
        if ext == ".pdf":
            docs.extend(PyPDFLoader(str(arquivo)).load())
        elif ext in {".txt", ".md"}:
            docs.extend(TextLoader(str(arquivo), encoding="utf-8").load())
    return docs