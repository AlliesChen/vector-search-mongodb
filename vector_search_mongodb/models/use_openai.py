
import openai


def generate_embedding(text: str, api_key: str) -> list[float]:
    openai.api_key = api_key
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=[text],
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error while generating embedding: {e}")
        return None
