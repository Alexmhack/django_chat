from django.db import models
from django.contrib.auth import get_user_model

from uuid import uuid4

User = get_user_model()

def deserialize_user(user):
	"""Deserialize user instance to JSON"""
	return {
		'id': user.id, 'username': user.username, 'email': user.email,
		'first_name': user.first_name, 'last_name': user.last_name
	}
