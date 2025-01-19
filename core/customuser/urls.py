from django.urls import path
from . import views
from . import viewsapi
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView

urlpatterns = [
    path('login/', viewsapi.login,name='login'),
    path('profil/', viewsapi.profile,name='profil'),
    path('update_profil/', viewsapi.update_profil,name='update_profil'),
    path('update_password_user/', viewsapi.update_password_user,name='update_password_user'),
    path('token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('create_user/', viewsapi.create_user,name='create_user'),
    path('update_user<int:id>/', viewsapi.update_user,name='update_user'),
]