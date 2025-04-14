from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai_handler import handle_query
from .voice_processor import text_to_speech
from .serializers import InteractionSerializer
from .models import Interaction

class VoiceAssistantView(APIView):
    def post(self, request):
        user_input = request.data.get('voice_input')
        if not user_input:
            return Response({"error": "No input provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Process input with AI
        ai_response = process_query(user_input)

        # Convert response to speech (now using gTTS)
        tts_result = text_to_speech(ai_response, output_file=os.path.join("media", "response.mp3"))

        # Check for TTS errors
        if tts_result.get("error"):
            return Response({"error": tts_result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save interaction
        interaction = Interaction(user_input=user_input, ai_response=ai_response)
        interaction.save()

        # Serialize response
        serializer = InteractionSerializer(interaction)
        response_data = {
            "interaction": serializer.data,
            "audio_file": tts_result['audio_file']
        }

        return Response(response_data, status=status.HTTP_200_OK)