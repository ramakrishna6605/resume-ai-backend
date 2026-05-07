from django.urls import path
from .views import (
    UploadResumeView,
    AnalyzeResumeView,
    JDMatchView,
    ResumeBuilderView,
    download_resume,
    home_view

)


urlpatterns=[
    path('upload/',UploadResumeView.as_view()),
    path('analyze/',AnalyzeResumeView.as_view()),
    path('match-jd/',JDMatchView.as_view()),
    path('build-resume/',ResumeBuilderView.as_view()),
    path('download/<int:resume_id>/', download_resume, name='download_resume'),
    path('',home_view),
]
