
import openai


class Openai:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate_embedding(self, text: str) -> list[float]:
        try:
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=[text],
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error while generating embedding: {e}")
            return None
