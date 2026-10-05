from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.tools import tool

from app.agent.helpers import get_embeddings
from app.rag.ingest import CHROMA_DIR, COLLECTION


@lru_cache(maxsize=1)
def get_retriever(k: int = 4):
    store = Chroma(
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
    )
    return store.as_retriever(search_kwargs={"k": k})


@tool
def buscar_documentos(consulta: str) -> str:
    """Busca trechos relevantes nos documentos internos da empresa.
    Use sempre que a pergunta for sobre o conteúdo desses documentos."""
    trechos = get_retriever().invoke(consulta)
    if not trechos:
        return "Nenhum trecho relevante encontrado."
    return "\n\n".join(
        f"[Fonte: {t.metadata.get('source', '?')}]\n{t.page_content}" for t in trechos
    )