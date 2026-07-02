from django.shortcuts import render
from django.utils import timezone
from .models import Post
from rest_framework import viewsets, permissions
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'posts': posts})

#Vista API REST
class PostViewSet(viewsets.ModelViewSet):
    #Endpoint de API que permite CRUD COMPLETO con los posts
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostSerializer

    def get_permit(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
#Vista API - register
class RegisterView(APIView):
    permission_classes= [AllowAny]
        
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        #Validaciones
        if not username or not password:
            return Response(
                {'error': 'Nombre de usuario y contraseña requeridos'},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'El usuario ya existe'},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        #Crear usuario
        user = User.objects.create_user(
            username= username,
            password= password
        )

        #Generar JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username
            }
        }, status.HTTP_201_CREATED)