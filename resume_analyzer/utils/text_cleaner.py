import re

stop_words = {"the", "is", "in", "at", "of", "and", "to", "for", "on", "with", "as", "by", "an", "be", "this", "that", "are", "from", "or", "it"}

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    text = text.lower()

    text = re.sub(r"\S+@\S+", " ", text) # to remove email address
    text = re.sub(r"\+?\d[\d\s\-]{8,}\d", " ", text) # to remove phone numbers
    text = re.sub(r"http\S+|www\S+", " ", text) # to remove links
    text = re.sub(r"[^a-z\s]", " ", text) # to remove special characters
    text = re.sub(r"\s+", " ", text).strip() # to remove spaces

    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    
    return " ".join(filtered_words)