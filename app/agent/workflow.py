from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.helpers import get_llm
from app.agent.prompt import SYSTEM_PROMPT
from app.agent.tools import TOOLS_GERAIS
from app.rag.tools import buscar_documentos

TOOLS = TOOLS_GERAIS + [buscar_documentos]
llm_com_tools = get_llm().bind_tools(TOOLS)


def chamar_modelo(state: MessagesState) -> dict:
    """Nó do agente: envia o histórico ao modelo e devolve a resposta."""
    mensagens = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm_com_tools.invoke(mensagens)]}


def build_graph(checkpointer=None):
    builder = StateGraph(MessagesState)  # estado = lista de mensagens

    builder.add_node("agente", chamar_modelo)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agente")
    builder.add_conditional_edges("agente", tools_condition)  # tools ou fim
    builder.add_edge("tools", "agente")

    return builder.compile(checkpointer=checkpointer)


# Sem memória própria: usado pelo LangGraph Studio (ele gerencia a memória)
graph = build_graph()

# Com memória por conversa (thread_id): usado no terminal e na API
graph_com_memoria = build_graph(MemorySaver())