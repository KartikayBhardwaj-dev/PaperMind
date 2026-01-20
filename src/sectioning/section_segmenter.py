import json 
import re
from pathlib import Path
from collections import Counter

SECTION_LABELS = [
    "abstract",
    "introduction",
    "related work",
    "method",
    "methodology",
    "experiment",
    "results",
    "discussion",
    "conclusion",
    "references"
]

def normalize(text):
    return re.sub(r"[^a-z ]", "", text.lower())

def is_section_heading(text, font_size, heading_font_threshold):
    text_norm = normalize(text)
    
    return (
        any(label in text_norm for label in SECTION_LABELS)
        and font_size >= heading_font_threshold
        and len(text.split()) <= 6
    )

def detect_heading_font_size(pages):
    font_sizes = []
    for page in pages:
        for block in page["blocks"]:
            font_sizes.append(block["font_size"])

    common_font = Counter(font_sizes).most_common(1)[0][0]
    return common_font + 1.5


def segment_sections(paper_json):
    pages = paper_json["pages"]
    heading_font_threshold = detect_heading_font_size(pages)

    sections = {}
    current_section = "unknown"
    sections[current_section] = []

    for page in pages:
        for block in page["blocks"]:
            text = block["text"]
            font_size = block["font_size"]

            if is_section_heading(text, font_size, heading_font_threshold):
                current_section = normalize(text)
                sections[current_section] = []
            else:
                sections[current_section].append(text)

    return sections