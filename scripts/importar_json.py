import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path

# Script para transformar o arquivo .json em um banco de dados

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "respostas.json"
DB_PATH = BASE_DIR / "data" / "respostas.db"
REJEITADOS_PATH = BASE_DIR / "data" / "rejeitados.jsonl"
VALIDOS_PATH = BASE_DIR / "data" / "respostas_validas.json"

CAMPOS_OBRIGATORIOS = [
    "id",
    "pergunta",
    "plataforma",
    "modelo",
    "resposta_texto",
    "data_hora",
]

MAX_TEXTO = 100_000


def validar_resposta(item):
    """Retorna uma lista de erros encontrados no registro."""
    erros = []

    if not isinstance(item, dict):
        return ["O registro não é um objeto JSON."]

    for campo in CAMPOS_OBRIGATORIOS:
        valor = item.get(campo)

        if not isinstance(valor, str) or not valor.strip():
            erros.append(f"Campo ausente ou inválido: {campo}")

    if erros:
        return erros

    texto = item["resposta_texto"]

    if len(texto) > MAX_TEXTO:
        erros.append("Texto excede o limite permitido.")

    # Detecta sequências extremas de caracteres repetidos.
    if re.search(r"(.)\1{100,}", texto):
        erros.append("Texto contém repetição excessiva de caracteres.")

    try:
        datetime.fromisoformat(item["data_hora"].replace("Z", "+00:00"))
    except ValueError:
        erros.append("Data e hora em formato inválido.")

    sentimento = item.get("sentimento")

    if sentimento is not None and not isinstance(sentimento, str):
        erros.append("Sentimento deve ser texto ou null.")

    return erros


def criar_tabela(conexao):
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id TEXT PRIMARY KEY,
            pergunta TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            modelo TEXT NOT NULL,
            resposta_texto TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            sentimento TEXT
        )
    """)


def importar_dados():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError) as erro:
        print(f"Não foi possível ler o JSON: {erro}")
        return

    if not isinstance(dados, list):
        print("Erro: a raiz do JSON deve ser uma lista.")
        return

    aceitos = 0
    rejeitados = []
    respostas_validas = []
    ids_processados = set()

    with sqlite3.connect(DB_PATH) as conexao:
        criar_tabela(conexao)

        for indice, item in enumerate(dados):
            erros = validar_resposta(item)

            if erros:
                rejeitados.append({
                    "indice": indice,
                    "id": item.get("id") if isinstance(item, dict) else None,
                    "erros": erros,
                })
                continue

            identificador = item["id"]

            # Evita IDs repetidos no próprio arquivo.
            if identificador in ids_processados:
                rejeitados.append({
                    "indice": indice,
                    "id": identificador,
                    "erros": ["ID duplicado no arquivo de origem."],
                })
                continue

            ids_processados.add(identificador)

            try:
                cursor = conexao.execute("""
                    INSERT INTO respostas (
                        id, pergunta, plataforma, modelo,
                        resposta_texto, data_hora, sentimento
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO NOTHING
                """, (
                    item["id"],
                    item["pergunta"],
                    item["plataforma"],
                    item["modelo"],
                    item["resposta_texto"],
                    item["data_hora"],
                    item.get("sentimento"),
                ))

                if cursor.rowcount == 0:
                    rejeitados.append({
                        "indice": indice,
                        "id": identificador,
                        "erros": ["ID já existente no banco."],
                    })
                else:
                    aceitos += 1
                    respostas_validas.append(item)

            except sqlite3.Error as erro:
                rejeitados.append({
                    "indice": indice,
                    "id": identificador,
                    "erros": [f"Erro no banco: {erro}"],
                })

    # Salva os motivos de serem rejeitados para permitir revisão posterior.
    with open(REJEITADOS_PATH, "w", encoding="utf-8") as arquivo:
        for registro in rejeitados:
            arquivo.write(
                json.dumps(registro, ensure_ascii=False) + "\n"
            )

    # Salva os arquivos válidos.
    with open(VALIDOS_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(
            respostas_validas,
            arquivo,
            ensure_ascii=False,
            indent=4,
        )

    print(f"Registros no arquivo: {len(dados)}")
    print(f"Novos registros importados: {aceitos}")
    print(f"Registros rejeitados/ignorados: {len(rejeitados)}")


if __name__ == "__main__":
    importar_dados()
