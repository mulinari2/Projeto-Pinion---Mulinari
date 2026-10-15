from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()


class resposta(BaseModel):
    id: str
    pergunta: str
    plataforma: str
    modelo: str
    resposta_texto: str
    data_hora: str
    sentimento: str


with open("dummy_json.json", "r", encoding= "utf-8") as file:
    respostas = json.load(file)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/respostas")
def ler_respostas() -> list[resposta]:
    return respostas