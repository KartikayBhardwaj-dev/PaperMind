import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

SECTION_PROTOTYPES = {
    "abstract": "summary of the paper and key contributions",
    "introduction": "background motivation and problem statement",
    "method": "proposed method and technical approach",
    "results": "experimental results and performance evaluation",
    "conclusion": "summary of findings and future work"
}

class SemanticClassifier:
    def __init__(self, embedder):
        self.embedder = embedder
        self.prototype_embeddings = {
            label: embedder.embed(desc)
            for label, desc in SECTION_PROTOTYPES.items()
        }

    def predict(self, section_text):
        section_embedding = self.embedder.embed(section_text)

        scores = {}
        for label, proto_emb in self.prototype_embeddings.items():
            score = cosine_similarity(
                section_embedding.reshape(1, -1),
                proto_emb.reshape(1, -1)
            )[0][0]
            scores[label] = float(score)

        return max(scores, key=scores.get), scores