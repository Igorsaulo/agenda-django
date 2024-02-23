from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(default=timezone.now)
    show = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='pictures/%Y/%m', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} '