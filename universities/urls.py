from django.urls import path, re_path
from . import views

app_name = 'universities'
urlpatterns = [
    path('', views.university_list, name='list'),
    path('<slug:university_slug>/', views.university_detail, name='detail'),
    path('<slug:university_slug>/rate/', views.rate_university, name='rate'),
    path('<slug:university_slug>/post/', views.create_post, name='create_post'),
    path('add/', views.add_university, name='add_university'), # The new URL
    re_path(r'^compare/(?P<slugs>[\w-]+(?:/[\w-]+)*)/$', views.compare_universities, name='compare'),
]