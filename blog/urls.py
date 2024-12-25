from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'blog', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('blog/<int:pk>/like/', LikeViewSet.as_view({'post': 'create'}), name='like-create'),
    path('blog/<int:pk>/unlike/', LikeViewSet.as_view({'delete': 'destroy'}), name='like-destroy'),
]
