from typing import Set
from pathlib import Path
def load_skills(file_path: str) -> Set[str]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Skills file not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        skills = {line.strip().lower() for line in file if line.strip()}

    return skills

def extract_skills(text: str, skills_db: Set[str]) -> Set[str]:
    extracted = set()
    for skill in skills_db:
        if skill in text:
            extracted.add(skill)
    return extracted