from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home, name='home'),
    path('methodology/', views.methodology_page, name='methodology'),
]