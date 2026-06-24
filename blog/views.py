from django.shortcuts import render
from django.utils import timezone
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'posts': posts})

#Vista API REST
class PostViewSet(viewsets.ModelViewSet):
    #Endpoint de API que permite CRUD COMPLETO con los posts
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostSerializer