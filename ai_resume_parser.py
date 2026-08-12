import pdfplumber
import re

def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_skills(text):

    skill_list = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "mysql",
        "machine learning",
        "power bi",
        "pandas",
        "numpy",
        "excel"
    ]

    found = []

    text = text.lower()

    for skill in skill_list:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)

    return found