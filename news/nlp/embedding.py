from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-xlm-r-multilingual-v1")


def get_embedding(text: str) -> np.array:
    return model.encode(text)
