from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import User
from .serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Allow anyone to create a user or log in
        if self.action in ['create', 'login']:
            permission_classes = [AllowAny]
        # Require authentication for other actions
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        # Use different serializers for different actions
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UpdateUserSerializer
        elif self.action == 'login':
            return LoginSerializer
        else:
            return UserSerializer

    def create(self, request, *args, **kwargs):
        # Create a new user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': status.HTTP_201_CREATED,
            'detail': 'Account created successfully',
            'data': {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        # Log in an existing user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = serializer.validated_data['login']
        password = serializer.validated_data['password']
        user = User.objects.filter(Q(email=login) | Q(username=login)).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': status.HTTP_200_OK,
                'detail': 'Login successful',
                'data': {
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        else:
            return Response({
                'status': status.HTTP_401_UNAUTHORIZED,
                'detail': 'Invalid credentials',
                'data': {}
            }, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        # Update an existing user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': status.HTTP_200_OK,
            'detail': 'Account updated successfully',
            'data': UserSerializer(instance).data
        })

    def destroy(self, request, *args, **kwargs):
      # Delete an existing user
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'detail': 'Account deleted successfully',
            'data': {}
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        # Get the current user's information
        user = request.user
        return Response({
            'status': status.HTTP_200_OK,
            'detail': 'User information retrieved',
            'data': UserSerializer(user).data
        })