from django.shortcuts import render
from rest_framework import status
from .models import Inventaris,Inventaris_status
from .serializers import InventarisSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from utils.custome_response import CustomResponse

# Create your views here.
User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny,])
def inventaris(request):
    inventaris = Inventaris.objects.all()
    serializer = InventarisSerializer(inventaris,many=True)
    return CustomResponse(serializer.data).response_success()

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def create_inventaris(request):
    if request.method == 'POST':
        serializer = InventarisSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    