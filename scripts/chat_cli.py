from app.agent.workflow import graph_com_memoria

config = {"configurable": {"thread_id": "terminal"}}

print("Agente pronto. Digite 'sair' para encerrar.\n")
while True:
    pergunta = input("Você: ").strip()
    if pergunta.lower() in {"sair", "exit"}:
        break
    resultado = graph_com_memoria.invoke(
        {"messages": [{"role": "user", "content": pergunta}]},
        config=config,
    )
    print("Agente:", resultado["messages"][-1].content, "\n")