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

O pytest cria um `respostas.db` temporário por teste a partir dos dados válidos
de `data/respostas_exemplo.json`. O banco fica isolado do banco real e é
removido automaticamente ao fim de cada teste.
