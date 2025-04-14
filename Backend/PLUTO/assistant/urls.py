from django.urls import path
from .views import VoiceAssistantView

urlpatterns = [
    path('voice/', VoiceAssistantView.as_view(), name='voice-assistant'),
]
