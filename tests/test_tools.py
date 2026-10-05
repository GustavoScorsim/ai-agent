from app.agent.tools import somar


def test_somar():
    assert somar.invoke({"a": 2, "b": 3}) == 5