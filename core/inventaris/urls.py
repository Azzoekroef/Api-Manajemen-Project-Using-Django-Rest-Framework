from django.urls import path
from . import views
from . import viewsapi


urlpatterns = [
    path('', viewsapi.inventaris, name='inventaris'),
    path('create/', viewsapi.create_inventaris, name='create_inventaris'),
]