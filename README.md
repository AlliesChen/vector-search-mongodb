# Mongo DB Vector Search Demo

## Initialization

Prerequisites:

- [pipx](https://pipx.pypa.io/stable/)

- [poetry](https://python-poetry.org/)

Create Environment Variants:

- MONGODB_URL
- HUGGINGFACE_TOKEN
- EMBEDDING_URL=https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2

```bash
poetry install
poetry run python vector_search_mongodb/__init__.py
```

## FAQ

[Connect to mongodb when you have Google login as credentials for Mongodb Atlas](https://stackoverflow.com/a/77422391/18972098);

[SSL Handshake issue with Pymongo on Python3 on Windows](https://stackoverflow.com/a/77084663/18972098)

