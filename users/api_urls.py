from django.urls import path
from . import views

app_name = 'users_api'

urlpatterns = [
    # API endpoints only
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('list/', views.UserListView.as_view(), name='user-list'),
]
