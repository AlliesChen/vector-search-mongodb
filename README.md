# MongoDB Vector Search Demo

> `openai.Embedding.create` has been changed to `openai.embedding.create`, see [the document](https://cookbook.openai.com/examples/using_embeddings)

This project use MongoDB sample_mflix data for demo natural language query.

## Initialization

I built the project on top of the project 1 (from 00:00 - 32:55) of [the tutorial](https://youtu.be/JEBDfGqrAUA?si=e_AMVU-zkTcF1j31) on YouTube by freeCodeCamp.

### Prerequisites

- [pipx](https://pipx.pypa.io/stable/)
- [poetry](https://python-poetry.org/)

### Install dependencies

```bash
poetry install
```

### Create Environment Variants

Put a file named `.env` under the folder with the following attributes in case of the features you need:

- MONGODB_URL **The URL for connecting to your MongoDB**

For who doesn't want to bind a credit card to OpenAI-- consider [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) on Hugging Face:

- HUGGINGFACE_TOKEN
- EMBEDDING_URL=https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2

For who would like to use [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings):

- OPENAI_API_KEY

### Create Search Index On MongoDB

Check [this article](https://www.mongodb.com/developer/products/atlas/quickstart-vectorsearch-mongodb-python/) by MongoDB if you want more detail about the search parameters.

#### Search Index

```
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "plot_embedding_hf": {
        "dimensions": 384,
        "similarity": "dotProduct",
        "type": "knnVector"
      }
    }
  }
}
```

#### Vector Search Index

```
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "plot_embedding",
      "similarity": "euclidean",
      "type": "vector"
    }
  ]
}
```

### Run the program

```bash
poetry run python vector_search_mongodb/__init__.py --query "your imagination"
```

## FAQ

- [Connect to mongodb when you have Google login as credentials for Mongodb Atlas](https://stackoverflow.com/a/77422391/18972098)
- [SSL Handshake issue with Pymongo on Python3 on Windows](https://stackoverflow.com/a/77084663/18972098)

