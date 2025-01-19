from django.urls import path
from . import views
from . import viewsapi


urlpatterns = [
    path('project/', viewsapi.project, name='project'),
    path('project/<int:id>/', viewsapi.project_1, name='project_get1'),
    path('done_projects/', viewsapi.done_projects, name='done_projects'),
    path('fail_projects/', viewsapi.fail_projects, name='fail_projects'),
    path('create_project/', viewsapi.create_project, name='create_projects'),
    path('update_project<int:id>/', viewsapi.update_project, name='update_projects'),
    path('employer/', viewsapi.employers, name='employers'),
    path('employer/<int:id>/', viewsapi.employer, name='employer'),
]