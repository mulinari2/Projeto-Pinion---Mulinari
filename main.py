import json
import re

# Marcas monitoradas (lista fixa) -> ["Acme", "Zenith", "Nimbus"]
marcas_monitoradas = ["Acme", "Zenith", "Nimbus"]

with open("dummy_json.json", "r", encoding="utf-8") as file:
    data = json.load(file)


def buscar_marcas(arquivo: object, marcas_monitoradas: list[str]):
    """Busca as marcas espeficicadas no arquivo passado e retorna a contagem.

    Args:
        data (object): arquivo json.
        marcas (list[str]): lista contendo as marcas desejadas.

    Returns:
        dict: dicionário contendo as contagens
    """

    with open(arquivo, "r", encoding="utf-8") as file:
        respostas = json.load(file)

    contagem_marcas_monitoradas = {marca: 0 for marca in marcas_monitoradas}

    # Busca das marcas espeficicadas
    for resposta in respostas:
        for marca in contagem_marcas_monitoradas.keys():
            texto = resposta["resposta_texto"]
            padrao = rf"(?<!\w){re.escape(marca)}(?!\w)"
            if re.search(padrao, texto, re.IGNORECASE):
                ocorrencias = re.findall(padrao, texto, re.IGNORECASE)
                contagem_marcas_monitoradas[marca] += len(ocorrencias) # Adicionar 1 nas ocorrências das marcas, caso encontrado
    return contagem_marcas_monitoradas

if __name__ == "__main__":
    # Teste para verificar funcionalidade
    print(buscar_marcas(arquivo = "dummy_json.json", marcas_monitoradas=marcas_monitoradas))
