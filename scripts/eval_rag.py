import json

from ragas import EvaluationDataset, evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
    ResponseRelevancy,
)

from app.agent.helpers import get_embeddings, get_llm
from app.rag.tools import get_retriever


def main():
    with open("tests/data/perguntas.json", encoding="utf-8") as f:
        casos = json.load(f)

    llm = get_llm()
    retriever = get_retriever()
    amostras = []

    for caso in casos:
        trechos = [d.page_content for d in retriever.invoke(caso["pergunta"])]
        contexto = "\n\n".join(trechos)
        resposta = llm.invoke(
            "Responda apenas com base no contexto.\n\n"
            f"Contexto:\n{contexto}\n\nPergunta: {caso['pergunta']}"
        ).content
        amostras.append(
            {
                "user_input": caso["pergunta"],
                "retrieved_contexts": trechos,
                "response": resposta,
                "reference": caso["referencia"],
            }
        )

    resultado = evaluate(
        dataset=EvaluationDataset.from_list(amostras),
        metrics=[
            Faithfulness(),
            ResponseRelevancy(),
            LLMContextPrecisionWithReference(),
            LLMContextRecall(),
        ],
        llm=LangchainLLMWrapper(llm),
        embeddings=LangchainEmbeddingsWrapper(get_embeddings()),
    )
    print(resultado)
    resultado.to_pandas().to_csv("ragas_resultado.csv", index=False)


if __name__ == "__main__":
    main()