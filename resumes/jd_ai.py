from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_jd_match(resume_text, jd_text):
    prompt = f"""
    Compare the following resume with the job description.
    
    Return ONLY valid JSON in this format:

    {{
      "match_score": number (0-100),
      "strengths_for_job": ["point1", "point2"],
      "missing_skills": ["skill1", "skill2"],
      "suggestions": ["suggestion1", "suggestion2"]
    }}

    Resume:
    {resume_text[:2000]}

    Job Description:
    {jd_text}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", str(e))
        return ""