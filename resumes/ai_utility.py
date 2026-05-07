from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume_with_ai(resume_text):
    prompt=f"""
    Analyze this resume and return JSON:
    DO NOT include any explanation or text outside JSON.
    STRICT FORMAT:
    {{
    "ats_score":"ats_score":integer(0-100),
    "strengths":["point1","point2"],
    "weaknesses":["point1","point2"],
    "missing_skills":["skill1","skill2"],
    "suggestions":["suggestion1","suggestion2"]
    }}
    Resume:
    {resume_text[:2000]}
    """
    try:
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"user","content":prompt}
                ],
                temperature=0.3
                )
        result=response.choices[0].message.content
        print("AI RESPONSE:", result)

        return result
    except Exception as e:
        print("GROQ ERROR:",str(e))
        return ""