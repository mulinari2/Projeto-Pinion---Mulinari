def test_post_resposta_sem_campo_obrigatorio(client, resposta_valida):
    payload = resposta_valida.copy()
    payload.pop("pergunta")

    response = client.post("/respostas", json=payload)

    assert response.status_code == 422


def test_post_resposta_persiste_no_banco_e_fica_disponivel_na_leitura(
    client, resposta_valida
):
    response = client.post("/respostas", json=resposta_valida)

    assert response.status_code == 200
    assert response.json()["resposta"]["id"] == resposta_valida["id"]
    respostas = client.get("/respostas").json()
    resposta_salva = next(
        resposta
        for resposta in respostas
        if resposta["id"] == resposta_valida["id"]
    )
    assert resposta_salva["resposta_texto"] == resposta_valida["resposta_texto"]