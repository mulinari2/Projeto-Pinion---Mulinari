def test_share_of_voice_retorna_sucesso(client):
    response = client.get("/share-of-voice")

    assert response.status_code == 200
    assert isinstance(response.json(), (dict, list))