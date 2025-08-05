# C:\Users\soyam\Documents\GitHub\SheRanks_Python\sheranks_project\api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from universities.views import UniversityViewSet, PostViewSet, RatingViewSet, CommentViewSet

router = DefaultRouter()
router.register('universities', UniversityViewSet)
router.register('posts', PostViewSet)
router.register('ratings', RatingViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]