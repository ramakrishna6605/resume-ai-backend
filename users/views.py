from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        # ✅ ADD strip() here also
        username = request.data.get("username", "").strip()
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "").strip()

        if not username or not password:
            return Response({"error": "Username & password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({"message": "User created successfully"})


# 🔐 Login (JWT)
class LoginView(APIView):
    def post(self, request):
        # ✅ ADD THIS (fixes space / input issues)
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "").strip()

        user = authenticate(username=username, password=password)

        # ✅ ADD DEBUG (optional but helpful)
        print("LOGIN ATTEMPT:", username, password)
        print("USER:", user)

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username
        })


class TestAuthView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        return Response({"message":"Authenticated!"})
