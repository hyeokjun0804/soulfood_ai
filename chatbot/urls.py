# urls.py
from django.urls import path
from chatbot import views


app_name = "chatbot"

urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chatbot_view'),
]
