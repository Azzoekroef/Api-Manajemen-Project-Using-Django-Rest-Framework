from django.urls import path
from . import views
from . import viewsapi


urlpatterns = [
    path('<int:id>/', viewsapi.note_project, name='note_project'),
]