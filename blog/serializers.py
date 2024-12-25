from rest_framework import serializers
from .models import Post, Like
from accounts.serializers import UserSerializer

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user']

class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    cover_image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'creation_date', 'dt_updated', 'author', 'is_public', 'category', 'tags', 'cover_image', 'likes', 'like_count']
        read_only_fields = ['author', 'creation_date', 'dt_updated']

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'is_public', 'category', 'tags', 'cover_image']