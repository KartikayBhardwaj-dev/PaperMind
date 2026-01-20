import torch
from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "allenai/scibert_scivocab_uncased"

class SciBERTEmbedder:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModel.from_pretrained(MODEL_NAME).to(self.device)
        self.model.eval()

    def embed(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        #CLS token embedding
        embedding = outputs.last_hidden_state[:, 0, :]
        return embedding.squeeze().cpu().numpy()