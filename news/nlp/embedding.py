from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-xlm-r-multilingual-v1")


def embedding(text: str) -> np.array:
    return model.encode(text)
