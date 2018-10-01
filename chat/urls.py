from django.urls import path

from .views import (
	ChatSessionView, ChatSessionMessageView
)

urlpatterns = [
	path('chats/', ChatSessionView.as_view()),
	path('chats/<uri>/', ChatSessionView.as_view()),
	path('chats/<uri>/messages/', ChatSessionMessageView.as_view()),
]
