from django.shortcuts import render
from rest_framework import status
from .models import Note,Project
from .serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from utils.custome_response import CustomResponse
from django.conf import settings
# Create your views here.
User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def note_project(request,id):
    notes = Note.objects.filter(project=id)
    notes_data = []
    for note in notes:
        note_data = {
            'id': note.id,
            'note': note.note,
        }
        notes_data.append(note_data)
    return CustomResponse({
            'notes': notes_data,
   }).response_success()