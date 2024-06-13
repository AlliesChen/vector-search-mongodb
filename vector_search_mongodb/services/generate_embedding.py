from enum import Enum


class ModelType(Enum):
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"


def generate_embedding(text: str, model: ModelType, api_key: str) -> list[float]:
    match model:
        case ModelType.HUGGINGFACE:
            return generate_embedding_hf(text, api_key)
        case ModelType.OPENAI:
            return generate_embedding_openai(text, api_key)
        case _:
            raise ValueError(f"Unsupported model type: {model}")
