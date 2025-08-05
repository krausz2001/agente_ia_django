from django.urls import path
from .views import chat_gemini

urlpatterns = [
    path("", chat_gemini, name="chat_gemini"),
]