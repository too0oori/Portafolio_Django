from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('proyectos/', views.todos_proyectos, name='todos_proyectos'),
]