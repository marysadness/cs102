from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password=None):
        """        
        Creates and saves a User with the given email and password.       
        """
        
        if email is None:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email))
        


        
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None):
        """        
        Creates and saves a superuser with the given email and password.        
        """
        
        if password is None:
            raise ValueError('Superusers must have a password.')
            
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    code = models.CharField(max_length=8, default='', null=True)

    USERNAME_FIELD = 'email'    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
