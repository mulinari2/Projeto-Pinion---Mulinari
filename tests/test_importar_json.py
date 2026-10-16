from scripts.importar_json import validar_resposta


def resposta_com_data(data_hora):
    return {
        "id": "r006",
        "pergunta": "Pergunta de teste",
        "plataforma": "gemini",
        "modelo": "gemini-2.0-flash",
        "resposta_texto": "Resposta de teste",
        "data_hora": data_hora,
        "sentimento": "positivo",
    }


def test_validar_resposta_converte_data_com_barras():
    resposta = resposta_com_data("2026/01/19")

    assert validar_resposta(resposta) == []
    assert resposta["data_hora"] == "2026-01-19T00:00:00"


def test_validar_resposta_rejeita_data_invalida_sem_criar_valor_nao_serializavel():
    resposta = resposta_com_data("data-invalida")

    erros = validar_resposta(resposta)

    assert "Data e hora em formato inválido." in erros
    assert resposta["data_hora"] == "data-invalida"


def test_validar_resposta_preserva_timestamp_iso_com_utc():
    resposta = resposta_com_data("2026-01-19T10:30:00Z")

    assert validar_resposta(resposta) == []
    assert resposta["data_hora"] == "2026-01-19T10:30:00+00:00"