from typing import Set, Dict

def match_skills(resume_skills: Set[str], jd_skills: Set[str]) -> Dict[str, object]:
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)

    if not jd_skills:
        match_percentage = 0
    else:
        match_percentage = round((len(matched_skills)/len(jd_skills))*100, 2)
    
    return {"matched_skills": matched_skills, "missing_skills": missing_skills, "match_percentage": match_percentage}

def evaluate_experience(user_level: str, jd_text: str) -> str:
    jd_text = jd_text.lower()

    if "3+ years" in jd_text or "5+ years" in jd_text or "senior" in jd_text:
        required_level = "3+ Years"
    elif "1-3 years" in jd_text or "1 - 3 years" in jd_text or "2 years" in jd_text:
        required_level = "1 - 3 Years"
    else:
        required_level = "Fresher"
    
    if user_level == required_level:
        return "Your experience level aligns well with this role."
    
    if user_level == "Fresher" and required_level != "Fresher":
        return "This role seems to require prior experience. Consider gaining more hands-on experience before applying."

    if user_level == "1 - 3 Years" and required_level == "3+ Years":
        return "This seems to be a senior-level role. Consider strengthening your profile with advanced projects as well as professional experience."
    
    return "Your experience level is acceptable, but reviewing the requirements carefully is recommended."