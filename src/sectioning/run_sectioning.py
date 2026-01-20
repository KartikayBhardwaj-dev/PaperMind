import json
from pathlib import Path
from section_segmenter import segment_sections

INPUT_DIR = Path("/Users/kartikaybhardwaj/PaperMind/data/extracted_text")
OUTPUT_DIR = Path("/Users/kartikaybhardwaj/PaperMind/data/sections")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for json_file in INPUT_DIR.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        paper = json.load(f)

    sections = segment_sections(paper)

    output_path = OUTPUT_DIR / json_file.name
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2)

    print(f"Sectioned → {output_path.name}")