from django.urls import path
from .views import RegisterView,TestAuthView,LoginView
from rest_framework_simplejwt.views import  TokenRefreshView,TokenObtainPairView


urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('login/',TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('test/',TestAuthView.as_view()),

]