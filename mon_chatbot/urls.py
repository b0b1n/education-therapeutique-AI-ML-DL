
from django.urls import path
from .views import *
urlpatterns = [
    path('chatbot/<id>',display_chatbot,name='chat'),
    #path('chat/',chatting,name='chatting'),
]
