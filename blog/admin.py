from django.contrib import admin
from .models import Post, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'creation_date', 'is_public', 'dt_updated')
    list_filter = ('is_public', 'author')
    search_fields = ('title', 'description', 'content')
    readonly_fields = ('creation_date', 'dt_updated')
    prepopulated_fields = {'title': ('title',)}

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'dt_created')