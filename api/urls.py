from django.urls import path
from .views import MovieView
from . import views

urlpatterns = [
    path('', MovieView.as_view()),
    path('search/', views.search, name='search'),
    path('find/', views.find, name='find'),
    path('movies/', views.m_list, name='m_list'),
]