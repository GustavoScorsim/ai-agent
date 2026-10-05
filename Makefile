install:
	pip install -r requirements.txt

ingest:
	python -m app.rag.ingest

chat:
	python -m scripts.chat_cli

dev:
	langgraph dev

server:
	uvicorn app.server.webapp:app --reload

test:
	pytest

eval:
	python -m scripts.eval_rag