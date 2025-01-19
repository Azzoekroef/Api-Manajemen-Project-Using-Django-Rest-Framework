from django.shortcuts import render
from rest_framework import status
from .serializers import UpdateCustomUserSerializer,CreateUserSerializers,UpdateUserSerializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.contrib.auth import get_user_model
from utils.custome_response import CustomResponse
from django.contrib.auth import login as lo
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import Jabatan,LevelJabatan
# Create your views here.
User = get_user_model()

# @api_view(['POST'])
# @permission_classes([AllowAny,])
# def register(request):
#     serializer = CustomUserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny,])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()

    if user is None or not user.check_password(password):
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    lo(request, user)
    return Response({
        'refresh': str(refresh),
        'access' : str(refresh.access_token),
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profil(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateCustomUserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def profile(request):
    user = User.objects.get(id=request.user.id)
    full_name = f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else None
    address_parts = [part for part in [user.street_address, user.city, user.province] if part] 
    address = ' '.join(address_parts) if address_parts else None
    base_url = settings.BASE_URL
    if user.image:
        image_url = f"{base_url}{user.image.url}"
    else:
        image_url = f"{base_url}/media/image/Screenshot1.png" # gambar default
    return CustomResponse({
            "id": user.id,
            "username": user.username,
            "name": full_name,
            "image": image_url,
            "qoute": user.qoute,
            "mulai_bekerja": user.mulai_bekerja,
            "phone_number": user.phone_number,
            "address": address,
            "jabatan" : user.jabatan.name,
            "level_jabatan": user.level_jabatan.name
            }).response_success()

@api_view(['POST'])
@permission_classes([IsAdminUser,])
def create_user(request):
    data = request.data
    serializer = CreateUserSerializers(data=data)
    jabatan_id = int(data.get('jabatan'))
    try:
        jabatan_instance = Jabatan.objects.get(id=jabatan_id)
        jabatan = jabatan_instance
    except Jabatan.DoesNotExist:
        pass
    level_jabatan_id = int(data.get('level_jabatan'))
    try:
        level_jabatan_instance = LevelJabatan.objects.get(id=level_jabatan_id)
        level_jabatan = level_jabatan_instance
    except LevelJabatan.DoesNotExist:
        pass
    default_password = "12345678"
    if serializer.is_valid():
        user = User.objects.create(
            username=data.get('username'),
            first_name=data.get('username'),
            mulai_bekerja = data.get('mulai_bekerja'),
            jabatan=jabatan,
            level_jabatan=level_jabatan,
            password=make_password(default_password)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAdminUser,])
def update_user(request, id):
    user = User.objects.get(pk=id)
    serializer = UpdateUserSerializers(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,])
def update_password_user(request):
    data = request.data
    user = request.user    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_paswword = data.get('confirm_password')
    if user.check_password(old_password):
        if new_password == confirm_paswword:
            user.set_password(new_password)
            user.save()
            return Response({'success': 'Kata sandi berhasil diubah.'}) 
        else :
            return Response({'error': 'Pastikan kofirmasi password sama dengan password terbaru.'})
    else:
        return Response({'error': 'Password lama salah.'}, status=status.HTTP_400_BAD_REQUEST)

