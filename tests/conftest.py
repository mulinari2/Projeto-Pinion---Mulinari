import pytest
from fastapi.testclient import TestClient

# Ajuste este import se sua aplicação estiver em outro módulo.
from app.routes import app


@pytest.fixture
def client():
    """Cliente HTTP para testar os endpoints sem subir um servidor."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def resposta_valida():
    """Payload mínimo válido conforme o schema do projeto."""
    return {
        "id": "pytest-resposta-001",
        "pergunta": "Qual ferramenta você recomenda para automação?",
        "plataforma": "ChatGPT",
        "modelo": "modelo-teste",
        "resposta_texto": "A Acme oferece recursos de automação. A Zenith também é uma opção.",
        "data_hora": "2026-01-15T10:30:00Z",
        "sentimento": "positivo",
    }
