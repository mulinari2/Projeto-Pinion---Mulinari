from fastapi import FastAPI, Query
import app.main as main
from models.model_resposta import Resposta

app = FastAPI()


@app.get("/")
def bem_vindo() -> str:
    return "Hello!"


@app.get("/respostas")
def listar_respostas() -> list[Resposta]:
    return main.carregar_respostas()


@app.get("/share-of-voice")
def obter_share_of_voice():
    return main.calcular_sov(main.carregar_respostas(), main.marcas_monitoradas)



@app.get("/top-citacoes")
def obter_top_citacoes(n: int = Query(..., gt=0)):
    return main.buscar_top_citacoes(main.carregar_respostas(),main.marcas_monitoradas,n=n,)


@app.post("/respostas")
def criar_resposta(resposta: Resposta):
    return main.adicionar_resposta(main.carregar_respostas(), resposta)