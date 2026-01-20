import json
from pathlib import Path
from text_cleaner import clean_text
from embedder import SciBERTEmbedder
from classifier import SemanticClassifier

INPUT_DIR = Path("data/sections")
OUTPUT_DIR = Path("data/semantic")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

embedder = SciBERTEmbedder()
classifier = SemanticClassifier(embedder)

for file in INPUT_DIR.glob("*.json"):
    with open(file, "r") as f:
        sections = json.load(f)

    semantic_output = {}

    for section_name, paragraphs in sections.items():
        if not paragraphs:
            continue

        cleaned = clean_text(paragraphs)
        label, scores = classifier.predict(cleaned)

        semantic_output[section_name] = {
            "predicted_label": label,
            "confidence_scores": scores,
            "text": cleaned[:2000]  # cap for storage
        }

    out_file = OUTPUT_DIR / file.name
    with open(out_file, "w") as f:
        json.dump(semantic_output, f, indent=2)

    print(f"Semantic enriched → {out_file.name}")