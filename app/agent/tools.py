from datetime import datetime

from langchain_core.tools import tool


@tool
def data_e_hora_atual() -> str:
    """Retorna a data e a hora atuais."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


@tool
def somar(a: float, b: float) -> float:
    """Soma dois números e retorna o resultado."""
    return a + b


TOOLS_GERAIS = [data_e_hora_atual, somar]