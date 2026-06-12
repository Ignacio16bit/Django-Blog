from django.db import models
from django.conf import settings
from django.utils import timezone

# Indica que es un modelo por parámetros
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #RELACIÓN con otro modelo
    title = models.CharField(max_length=200) #Texto con límite 
    text = models.TextField() #Texto sin límite
    created_date = models.DateTimeField(
        default=timezone.now
    )
    published_date = models.DateTimeField(
        blank = True, null= True
    )

    def publish(self):
        self.published_date = timezone.now
        self.save()

    def __str__(self): #ToString()
        return self.title