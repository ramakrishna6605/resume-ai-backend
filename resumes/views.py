from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import os
import requests
import re
import json

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .resume_builder_ai import generate_resume_from_prompt
from .jd_ai import analyze_jd_match
from .utils import extract_text_from_pdf
from .ai_utility import analyze_resume_with_ai

from .models import Resume, ResumeAnalysis, GeneratedResume


# ------------------ HELPERS ------------------

def normalize_score(score):
    try:
        score = float(score)
        if score <= 1:
            score = score * 100
        return int(score)
    except:
        return 60


def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return match.group() if match else None


# ------------------ UPLOAD ------------------
from rest_framework.permissions import IsAuthenticated

class UploadResumeView(APIView):
    permission_classes = [IsAuthenticated]   # ✅ REQUIRE LOGIN

    def post(self, request):
        try:
            file = request.FILES.get('file')

            if not file:
                return Response({"error": "No file uploaded"}, status=400)

            resume = Resume.objects.create(
                user=request.user,   # ✅ FIX
                file=file
            )

            text = extract_text_from_pdf(resume.file)
            resume.extracted_text = text
            resume.save()

            # 🔥 DIRECT ANALYSIS
            ai_response = analyze_resume_with_ai(text)

            clean_json = extract_json(ai_response)
            data = json.loads(clean_json) if clean_json else None

            return Response({
                "resume_id": resume.id,
                "analysis": data
            })

        except Exception as e:
            print("UPLOAD ERROR:", str(e))   # ✅ DEBUG
            return Response({"error": str(e)}, status=500)



# ------------------ ANALYZE ------------------

class AnalyzeResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get("resume_id")

        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

        resume_text = (resume.extracted_text or "")[:3000]

        if not resume_text.strip():
            return Response({"error": "Resume text is empty"}, status=400)

        ai_response = analyze_resume_with_ai(resume_text)

        try:
            clean_json = extract_json(ai_response)
            data = json.loads(clean_json) if clean_json else None
        except:
            data = None

        if not data:
            data = {
                "ats_score": 60,
                "strengths": ["Basic skills"],
                "weaknesses": ["Limited content"],
                "missing_skills": ["Advanced tools"],
                "suggestions": ["Improve resume"]
            }

        analysis, _ = ResumeAnalysis.objects.update_or_create(
            resume=resume,
            defaults={
                "ats_score": normalize_score(data.get("ats_score")),
                "strengths": data.get("strengths"),
                "weaknesses": data.get("weaknesses"),
                "missing_skills": data.get("missing_skills"),
                "suggestions": data.get("suggestions"),
            }
        )

        return Response({
            "ats_score": analysis.ats_score,
            "strengths": analysis.strengths,
            "weaknesses": analysis.weaknesses,
            "missing_skills": analysis.missing_skills,
            "suggestions": analysis.suggestions
        })


# ------------------ JD MATCH ------------------

class JDMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get("resume_id")
        jd_text = request.data.get("job_description")

        if not jd_text:
            return Response({"error": "Job description required"}, status=400)

        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)

        ai_response = analyze_jd_match(resume.extracted_text, jd_text)

        try:
            clean_json = extract_json(ai_response)
            data = json.loads(clean_json) if clean_json else None
        except:
            data = None

        if not data:
            data = {
                "match_score": 60,
                "strengths_for_job": ["Basic match"],
                "missing_skills": ["Advanced skills"],
                "suggestions": ["Improve resume"]
            }

        return Response(data)


# ------------------ BUILDER ------------------

class ResumeBuilderView(APIView):
    permission_classes = []   # keep open for now

    def post(self, request):
        user_input = request.data.get("input")

        if not user_input:
            return Response({"error": "input required"}, status=400)

        ai_response = generate_resume_from_prompt(user_input)
        print("AI RAW:", ai_response)

        try:
            clean_json = extract_json(ai_response)
            data = json.loads(clean_json) if clean_json else None
        except:
            data = None

        if not data:
            return Response({"error": "AI failed"}, status=500)

        # ✅ FIX IS HERE
        user = request.user if request.user.is_authenticated else None

        resume = GeneratedResume.objects.create(
            user=user,
            content=data
        )

        return Response({
            "resume_id": resume.id,
            "data": data
        })

# ------------------ PDF DOWNLOAD ------------------

from django.http import HttpResponse
from django.template.loader import get_template
from .models import GeneratedResume
from xhtml2pdf import pisa


def download_resume(request, resume_id):
    try:
        resume = GeneratedResume.objects.get(id=resume_id)
    except GeneratedResume.DoesNotExist:
        return HttpResponse("Resume not found", status=404)

    try:
        # Load template
        template = get_template("resume_template.html")

        # Render HTML
        html = template.render({
            "data": resume.content,
            "pdf": True
        })

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Check for errors
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)

        return response

    except Exception as e:
        return HttpResponse(f"Server Error: {str(e)}", status=500)


# ------------------ HOME ------------------

def home_view(request):
    return render(request, "home.html")