def test_post_resposta_sem_campo_obrigatorio(client, resposta_valida):
    payload = resposta_valida.copy()
    payload.pop("pergunta")

    response = client.post("/respostas", json=payload)

    assert response.status_code == 422