from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.routes import app
from scripts import importar_json

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def banco_teste(tmp_path, monkeypatch):
    """Cria um banco SQLite isolado com os dados válidos do JSON de exemplo."""
    db_path = tmp_path / "respostas.db"
    monkeypatch.setattr(
        importar_json,
        "JSON_PATH",
        BASE_DIR / "data" / "respostas_exemplo.json",
    )
    monkeypatch.setattr(importar_json, "DB_PATH", db_path)
    rejeitados_path = tmp_path / "rejeitados.jsonl"
    monkeypatch.setattr(importar_json, "REJEITADOS_PATH", rejeitados_path)
    importar_json.importar_dados()
    monkeypatch.setattr(main, "DB_PATH", db_path)
    try:
        yield db_path
    finally:
        db_path.unlink(missing_ok=True)
        rejeitados_path.unlink(missing_ok=True)


@pytest.fixture
def client(banco_teste):
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
