from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Frontend views (HTML pages)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    
    # API endpoints
    path('api/register/', views.register, name='register-api'),
    path('api/login/', views.login, name='login-api'),
    path('api/logout/', views.logout, name='logout'),
    path('api/profile/', views.profile, name='profile'),
    path('api/list/', views.UserListView.as_view(), name='user-list'),
]

