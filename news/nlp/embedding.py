from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("distiluse-base-multilingual-cased-v2")


def get_embedding(text: str) -> np.array:
    return model.encode(text)
