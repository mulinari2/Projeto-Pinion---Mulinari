import json

# Marcas monitoradas (lista fixa) -> ["Acme", "Zenith", "Nimbus"]
marcas_monitoradas = ["Acme", "Zenith", "Nimbus"]

contagem_marcas_monitoradas = {"Acme": 0,
                               "Zenith": 0,
                               "Nimbus": 0}

with open("dummier_json.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for answer in data:
    for marca in contagem_marcas_monitoradas.keys():
        if marca in answer["resposta_texto"]:
            contagem_marcas_monitoradas[marca] += 1

for chave, valor in contagem_marcas_monitoradas.items():
    print(f"{chave}: {valor}")
