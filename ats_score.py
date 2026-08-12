def calculate_score(skills, resume_text=""):

    required_skills = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "mysql",
        "machine learning",
        "power bi"
    ]

    score = 0

    # Skills - maximum 60 points
    found_skills = []

    for skill in required_skills:

        if skill.lower() in [
            s.lower().strip()
            for s in skills
        ]:
            found_skills.append(skill)
            score += 6

    # Resume sections - maximum 40 points
    text = resume_text.lower()

    sections = {
        "education": ["education", "b.tech", "bachelor"],
        "experience": ["experience", "internship"],
        "projects": ["projects", "project"],
        "certifications": ["certification", "certifications"],
        "contact": ["email", "phone", "contact"],
        "summary": ["summary", "objective"]
    }

    for section_keywords in sections.values():

        if any(keyword in text for keyword in section_keywords):
            score += 6

    # Maximum 100
    return min(score, 100)