def test_top_citacoes_respeita_parametro_n(client):
    response = client.get("/top-citacoes", params={"n": 2})

    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) <= 2

