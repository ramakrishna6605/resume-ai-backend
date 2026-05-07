from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_resume_from_prompt(user_input):
    prompt=f"""
    You are an AI Resume Builder.

    Based on the user input, generate a professional resume.

    Return ONLY valid JSON in this format:

    {{
        "name": "",
        "email": "",
        "skills": [],
        "projects": [],
        "education": "",
        "experience": "",
        "summary": ""
    }}

    User Input:
    {user_input}
    """


    try:
        response=client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}],
            temperature=0.4

        )
        return response.choices[0].message.content
    except Exception as e:
        print("AI ERROR:",str(e))
        return ""
