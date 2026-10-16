from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class Resposta(BaseModel):
    id: str = Field(min_length=1)
    pergunta: str = Field(min_length=1)
    plataforma: str = Field(min_length=1)
    modelo: str = Field(min_length=1)
    resposta_texto: str = Field(min_length=1)
    data_hora: datetime
    sentimento: str

    @field_validator(
        "id",
        "pergunta",
        "plataforma",
        "modelo",
        "resposta_texto",
        "sentimento",
    )
    @classmethod
    def validar_texto_nao_vazio(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("O campo não pode conter apenas espaços.")
        return valor
