# Generated by Django 4.2.17 on 2024-12-25 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("content", models.TextField()),
                (
                    "creation_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("is_public", models.BooleanField(default=True)),
                ("category", models.CharField(blank=True, max_length=100, null=True)),
                ("tags", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "cover_image",
                    models.ImageField(blank=True, null=True, upload_to="post_covers/"),
                ),
                ("dt_updated", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("dt_created", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="blog.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("post", "user")},
            },
        ),
    ]
