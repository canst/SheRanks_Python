from django.urls import path
from . import views

app_name = 'universities'
urlpatterns = [
    path('', views.university_list, name='list'),
    path('<slug:university_slug>/', views.university_detail, name='detail'),
    path('<slug:university_slug>/rate/', views.rate_university, name='rate'),
]