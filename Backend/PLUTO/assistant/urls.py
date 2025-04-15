from django.urls import path
from .views import VoiceAssistantView, RegisterView

urlpatterns = [
    path('voice/', VoiceAssistantView.as_view(), name='voice-assistant'),
    path('register/', RegisterView.as_view(), name='register'),
]
