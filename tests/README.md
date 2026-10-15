# Testes pytest: API de monitoramento de marcas

## Estrutura esperada

O template assume que a aplicação FastAPI está em `app/routes.py` e que o objeto se chama `app`:

```python
from fastapi import FastAPI
app = FastAPI()
```

Se o módulo ou o nome do objeto forem diferentes, ajuste o import em `tests/conftest.py`.

## Instalação

No ambiente virtual do projeto:

```bash
pip install -r requirements-test.txt
```

## Execução

Na raiz do projeto:

```bash
pytest
```

Para saída detalhada:

```bash
pytest -v
```

Para executar apenas um arquivo:

```bash
pytest tests/test_respostas.py -v
```

## Importante: banco de testes

Os testes de `POST /respostas` criam registros com IDs iniciados em `pytest-`.
Antes de executar, confirme que a aplicação está configurada para usar um banco de testes, ou configure uma fixture que substitua a dependência/conexão do banco por um SQLite temporário. Não execute testes de escrita contra dados de produção.

## Ajustes esperados

Este é um template porque o código real dos endpoints e seus contratos de resposta não foi incluído nesta conversa. As expectativas de status HTTP, especialmente para IDs duplicados, marcas desconhecidas e `n=0`, devem refletir as regras que sua API realmente implementa.
