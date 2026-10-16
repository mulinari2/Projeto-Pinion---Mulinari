# Análise de menções de marcas

API FastAPI que analisa respostas de IA e identifica menções a Acme, Zenith e
Nimbus. As menções não diferenciam maiúsculas de minúsculas e são contadas por
resposta.

## Estrutura

- `app/`: rotas HTTP e lógica de análise.
- `models/`: validação dos dados de resposta.
- `data/`: arquivos de origem, dados válidos e rejeitados, e banco SQLite.
- `scripts/importar_json.py`: valida e importa respostas do JSON para o banco SQLite.
- `tests/`: testes da API e da análise.

## Preparar e executar

Use Python 3.10 ou superior. Instale as dependências e prepare o arquivo de
entrada (ou coloque seu próprio histórico em `data/respostas.json`):

```bash
pip install -r requirements.txt
pip install -r tests/requirements-test.txt
python scripts/importar_json.py
python -m uvicorn app.routes:app --reload
```

Execute os comandos a partir da raiz do repositório. A importação valida os
registros, grava os aceitos em `data/respostas.db` e registra os rejeitados em
`data/rejeitados.jsonl`. A API lê e atualiza as respostas diretamente no banco
SQLite.

## Endpoints

- `GET /respostas`: lista as respostas válidas.
- `GET /share-of-voice`: calcula o percentual de respostas com menção, por marca
  e plataforma.
- `GET /top-citacoes?n=5`: retorna até `n` respostas com mais marcas citadas.
- `POST /respostas`: valida e adiciona uma resposta; envie o registro em JSON.

A documentação interativa fica em `/docs`. Para rodar os testes:

```bash
pytest
```

## Próximos passos

Com mais tempo, adicionaria configuração de ambientes e ampliaria os testes de
integração e de dados sujos.
