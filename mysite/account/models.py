from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, blank=True)
    bio = models.TextField()
    location = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
