from django.urls import path
from .views import chat_gemini,home

urlpatterns = [
    path("home/", home, name="home"),
    path("", chat_gemini, name="chat_gemini"),
]