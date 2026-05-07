from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

import re

def extract_keywords(text):
    # convert to lowercase
    text = text.lower()

    # extract only words
    words = re.findall(r'[a-zA-Z]+', text)

    # remove common useless words
    stopwords = {
        "and","or","the","a","an","to","for","with","of","in","on",
        "looking","experience","developer"
    }

    keywords = [w for w in words if w not in stopwords and len(w) > 2]

    return set(keywords)


def calculate_match_score(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    print("RESUME KEYWORDS:", resume_keywords)
    print("JD KEYWORDS:", jd_keywords)

    if not jd_keywords:
        return 0

    matched = resume_keywords.intersection(jd_keywords)

    print("MATCHED:", matched)

    score = (len(matched) / len(jd_keywords)) * 100

    return round(score, 2)


def get_missing_keywords(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    missing = jd_keywords - resume_keywords

    return list(missing)