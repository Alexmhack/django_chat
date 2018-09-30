from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import (
	deserialize_user, ChatSession, ChatSessionMessage, ChatSessionMember
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class ChatSessionView(APIView):
	"""Manage Chat Session"""

	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		"""create a new chat session"""
		user = request.user

		chat_session = ChatSession.objects.create(owner=user)

		return Response({
			'status': 'SUCCESS', 'uri': chat_session.uri,
			'message': 'New chat session created'
		})
