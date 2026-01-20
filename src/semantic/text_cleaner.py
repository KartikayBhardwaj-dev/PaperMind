import re

def clean_text(text_list):
    """
    Cleans list of paragraphs into a single normalised string
    """

    text = " ".join(text_list)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9., ]", "", text)
    
    return text.strip()