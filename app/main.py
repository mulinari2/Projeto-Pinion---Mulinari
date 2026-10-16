import sqlite3
from pathlib import Path
import re
from collections import Counter
from models.model_resposta import Resposta
from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "respostas.db"

# Marcas monitoradas (lista fixa) -> ["Acme", "Zenith", "Nimbus"]
marcas_monitoradas = ["Acme", "Zenith", "Nimbus"]

def carregar_respostas() -> list[dict]:
    with sqlite3.connect(DB_PATH) as conexao:
        conexao.row_factory = sqlite3.Row
        registros = conexao.execute("""
            SELECT id, pergunta, plataforma, modelo,
                   resposta_texto, data_hora, sentimento
            FROM respostas
            ORDER BY rowid
        """)
        return [dict(registro) for registro in registros]

def calcular_sov(respostas: list[dict], marcas: list[str]) -> dict:
    """Calcula o SOV geral e por plataforma para todas as marcas."""

    total = len(respostas)
    resultados = {}

    for marca in marcas:
        citacoes = 0
        total_por_plataforma = Counter()
        citacoes_por_plataforma = Counter()

        padrao = rf"(?<!\w){re.escape(marca)}(?!\w)"

        for resposta in respostas:
            plataforma = resposta["plataforma"]
            texto = resposta["resposta_texto"]

            total_por_plataforma[plataforma] += 1

            # Cada resposta conta apenas uma vez para o SOV.
            if re.search(padrao, texto, re.IGNORECASE):
                citacoes += 1
                citacoes_por_plataforma[plataforma] += 1

        sov_geral = citacoes / total * 100 if total else 0.0

        resultados[marca] = {
            "total_respostas": total,
            "respostas_com_mencao": citacoes,
            "share_of_voice": round(sov_geral, 2),
            "por_plataforma": {
                plataforma: {
                    "total_respostas": quantidade,
                    "respostas_com_mencao": citacoes_por_plataforma[plataforma],
                    "share_of_voice": round(
                        citacoes_por_plataforma[plataforma] / quantidade * 100,
                        2,
                    ) if quantidade else 0.0,
                }
                for plataforma, quantidade in total_por_plataforma.items()
            },
        }

    return resultados


def buscar_top_citacoes(respostas: list[dict], marcas: list[str], n: int) -> list[dict]:
    ranking = []

    for resposta in respostas:
        texto = resposta.get("resposta_texto", "")

        if not isinstance(texto, str) or not texto.strip():
            continue

        marcas_citadas = []

        for marca in marcas:
            padrao = rf"(?<!\w){re.escape(marca)}(?!\w)"

            if re.search(padrao, texto, re.IGNORECASE):
                marcas_citadas.append(marca)

        if marcas_citadas:
            ranking.append({
                **resposta,
                "marcas_citadas": marcas_citadas,
                "total_marcas": len(marcas_citadas),
            })

    ranking.sort(
        key=lambda resposta: resposta["total_marcas"],
        reverse=True,
    )

    return ranking[:n]


def adicionar_resposta(respostas: list[dict], resposta: Resposta):

    if any(
        item.get("id") == resposta.id
        for item in respostas
    ):
        raise HTTPException(
            status_code=409,
            detail="Já existe uma resposta com esse ID.",
        )

    # Converte o modelo Pydantic para um dicionário serializável
    nova_resposta = resposta.model_dump(mode="json")

    try:
        with sqlite3.connect(DB_PATH) as conexao:
            conexao.execute("""
                INSERT INTO respostas (
                    id, pergunta, plataforma, modelo,
                    resposta_texto, data_hora, sentimento
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nova_resposta["id"],
                nova_resposta["pergunta"],
                nova_resposta["plataforma"],
                nova_resposta["modelo"],
                nova_resposta["resposta_texto"],
                nova_resposta["data_hora"],
                nova_resposta["sentimento"],
            ))
    except sqlite3.IntegrityError as erro:
        raise HTTPException(
            status_code=409,
            detail="Já existe uma resposta com esse ID.",
        ) from erro

    respostas.append(nova_resposta)

    return {
        "mensagem": "Resposta adicionada com sucesso.",
        "resposta": nova_resposta,
    }
