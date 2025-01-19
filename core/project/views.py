from django.shortcuts import render, redirect
# from .models import New, Category
from django.contrib import messages
from django.http import  HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
class Home:
    def home(request):
        
        return render(request,'home.html')