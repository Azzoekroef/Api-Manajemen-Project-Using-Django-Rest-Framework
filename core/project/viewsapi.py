from django.shortcuts import render
from rest_framework import status
from .models import Project,Status
from project_handle.models import ProjectHandle
from customuser.serializers import CustomUserSerializer
from .serializers import ProjectSerializer,CreateProjectSerializer,ProjectHandleSerializer,UpdateProjectSerializer
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
def employers(request):
    users = User.objects.all()
    users_data = []
    for user in users :
        full_name = f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else None
        base_url = settings.BASE_URL
        if user.image:
            image_url = f"{base_url}{user.image.url}"
        else:
            image_url = f"{base_url}/media/image/Screenshot1.png"
        user_data = {
            'id': user.id,
            'username': user.username,
            'fullname': full_name,
            'image': image_url,
            'email': user.email,
            'qoute': user.qoute,
            'jabatan': user.jabatan.name if user.jabatan else None
        }
        users_data.append(user_data)
    return CustomResponse({
        "users" : users_data
    }
    ).response_success()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def employer(request, id):
    user = User.objects.get(pk=id)
    address_parts = [part for part in [user.street_address, user.city, user.province] if part]  # Filter bagian alamat yang tidak None
    address = ' '.join(address_parts) if address_parts else None
    full_name = f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else None
    base_url = settings.BASE_URL
    if user.image:
        image_url = f"{base_url}{user.image.url}"
    else:
        image_url = f"{base_url}/media/image/Screenshot1.png"
    return CustomResponse({
            'id': user.id,
            'username': user.username,
            'fullname': full_name,
            'image': image_url,
            'email': user.email,
            'qoute': user.qoute,
            'salary': user.salary,
            'address': address,
            'jabatan': user.jabatan.name if user.jabatan else None,
            "level_jabatan": user.level_jabatan.name
    }
    ).response_success()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def project(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return CustomResponse(serializer.data).response_success()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def project_1(request,id):
    projects = Project.objects.get(pk=id)
    serializer = ProjectSerializer(projects)
    return CustomResponse(serializer.data).response_success()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def done_projects(request):
    status_done = Status.objects.get(name__icontains='done')
    projects = Project.objects.filter(status=status_done)
    serializer = ProjectSerializer(projects, many=True)
    return CustomResponse(serializer.data).response_success()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def fail_projects(request):
    status_fail = Status.objects.get(name__icontains='fail')
    projects = Project.objects.filter(status=status_fail)
    serializer = ProjectSerializer(projects, many=True)
    return CustomResponse(serializer.data).response_success()

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def create_project(request):
    if request.method == 'POST':
        serializer = CreateProjectSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated,])
def update_project(request,id):
    projects = Project.objects.get(pk=id)
    serializer = UpdateProjectSerializer(projects, data=request.data, context={'request': request}, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    