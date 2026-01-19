import fitz
import json
from pathlib import Path
from tqdm import tqdm

def extract_pdf(pdf_path):
    """
    Extracts text blocks with font sizes from a PDF.
    Returns a list of pages with blocks.
    """
    doc = fitz.open(pdf_path)
    pages_data = []

    for page_num, page in enumerate(doc, start=1):
        blocks = []
        page_dict = page.get_text("dict")

        for block in page_dict.get("blocks", []):
            lines = block.get("lines", [])
            if not lines:
                continue

            for line in lines:
                text = ""
                font_sizes = []

                for span in line.get("spans", []):
                    text += span.get("text", "")
                    font_sizes.append(span.get("size", 0))

                if text.strip():
                    blocks.append({
                        "text": text.strip(),
                        "font_size": round(
                            sum(font_sizes) / len(font_sizes), 2
                        ) if font_sizes else 0
                    })

        pages_data.append({
            "page": page_num,
            "blocks": blocks
        })

    return pages_data

def process_pdf(pdf_path, output_dir):
    """
    Processess a PDF and saves structured JSON
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paper_data = {
        "paper_id": pdf_path.stem,
        "pages": extract_pdf(pdf_path)
    }

    output_file = output_dir / f"{pdf_path.stem}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(paper_data, f, indent=2)

    print(f"Saved Structured JSON: {output_file}")

if __name__ == "__main__":
    input_dir = "/Users/kartikaybhardwaj/PaperMind/data/raw_pdfs"
    output_dir = "/Users/kartikaybhardwaj/PaperMind/data/extracted_text"

    pdf_files = list(Path(input_dir).glob("*.pdf"))
    for pdf_file in tqdm(pdf_files):
        process_pdf(pdf_file, output_dir)
 