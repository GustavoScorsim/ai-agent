from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.workflow import graph_com_memoria

app = FastAPI(title="Meu Agente de IA")


class ChatRequest(BaseModel):
    mensagem: str
    thread_id: str = "default"


class ChatResponse(BaseModel):
    resposta: str
    thread_id: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    resultado = graph_com_memoria.invoke(
        {"messages": [{"role": "user", "content": req.mensagem}]},
        config=config,
    )
    return ChatResponse(
        resposta=resultado["messages"][-1].content,
        thread_id=req.thread_id,
    )