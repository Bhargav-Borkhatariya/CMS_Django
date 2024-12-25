from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    is_public = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True, null=True) 
    tags = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(upload_to='post_covers/', blank=True, null=True)
    dt_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    dt_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user} likes {self.post.title}'