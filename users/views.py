from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Auto-login after registration
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login endpoint."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Also login via Django session for frontend
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """User logout endpoint."""
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    """List all users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# Frontend Views
def register_view(request):
    """Frontend registration page."""
    if request.user.is_authenticated:
        return redirect('auctions:home')
    return render(request, 'users/register.html')


def login_view(request):
    """Frontend login page."""
    if request.user.is_authenticated:
        return redirect('auctions:home')
    return render(request, 'users/login.html')

