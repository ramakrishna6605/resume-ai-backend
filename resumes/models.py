from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

User=settings.AUTH_USER_MODEL

# Create your models here.

class Resume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    file=models.FileField(upload_to='resume/')
    extracted_text=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.id}"
    



class ResumeAnalysis(models.Model):
    resume=models.OneToOneField(Resume,on_delete=models.CASCADE,null=True,blank=True)
    ats_score=models.IntegerField()
    strengths=models.JSONField(default=list)
    weaknesses=models.JSONField(default=list)
    missing_skills=models.JSONField(default=list)
    created_at=models.DateTimeField(auto_now_add=True)
    suggestions=models.JSONField(default=list)


class GeneratedResume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    content=models.JSONField()
    created_at=models.DateTimeField(auto_now_add=True)