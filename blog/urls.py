from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PostViewSet

#Ruteo de URLs de la API
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', views.post_list, name='post_list'), #HTML
    path('api/', include(router.urls)) #API
]