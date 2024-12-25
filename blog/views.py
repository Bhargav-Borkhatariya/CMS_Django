from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post, Like
from .serializers import PostSerializer, PostCreateUpdateSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count
from configuration.utils import IsPostOwner


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsPostOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return PostCreateUpdateSerializer
        else:
            return PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(is_public=True).annotate(like_count=Count('likes'))
        serializer = PostSerializer(queryset, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'detail': 'Posts retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if not post.is_public and post.author != request.user:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'detail': 'Not found.',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response({
            'status': status.HTTP_200_OK,
            'detail': 'Post retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            data = PostSerializer(post).data
            return Response({
                'status': status.HTTP_201_CREATED,
                'detail': 'Post created successfully.',
                'data': data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'detail': 'Validation Error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        partial = kwargs.pop('partial', False)
        serializer = PostCreateUpdateSerializer(post, data=request.data, partial=partial)
        if serializer.is_valid():
            post = serializer.save()
            data = PostSerializer(post).data
            return Response({
                'status': status.HTTP_200_OK,
                'detail': 'Post updated successfully.',
                'data': data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'detail': 'Validation Error',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'detail': 'Post deleted successfully.',
            'data': {}
        }, status=status.HTTP_204_NO_CONTENT)

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            return Response({
                'status': status.HTTP_201_CREATED,
                'detail': 'Post liked successfully.',
                'data': {}
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'detail': 'Post already liked.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response({
                'status': status.HTTP_204_NO_CONTENT,
                'detail': 'Post unliked successfully.',
                'data': {}
            }, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'detail': 'Post not liked.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)