from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import os
from .ai_handler import handle_query
from .voice_processor import text_to_speech
from .models import Interaction

class VoiceAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get('voice_input')
        if not user_input:
            return Response({"error": "No input provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Process input with AI
        ai_response = handle_query(user_input)
        if "Error processing query" in ai_response:
            return Response({"error": ai_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Convert response to speech
        tts_result = text_to_speech(ai_response, output_file=os.path.join("media", "response.mp3"))
        if tts_result.get("error"):
            return Response({"error": tts_result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save interaction
        interaction = Interaction.objects.create(
            user=request.user,
            user_input=user_input,
            ai_response=ai_response
        )

        # Return response
        return Response({
            "interaction": {
                "user_input": user_input,
                "ai_response": ai_response,
                "created_at": interaction.created_at
            },
            "audio_file": "media/response.mp3"
        }, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)