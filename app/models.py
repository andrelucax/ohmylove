from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    username = None
    first_name = None
    last_name = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class Cloupe(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cloupe_user_1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cloupe_user_2')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.email} - {self.user2.email}"

class CoupleSpecialDate(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    cloupe = models.ForeignKey(Cloupe, on_delete=models.CASCADE, related_name='special_dates')

    def __str__(self):
        return f"{self.name} - {self.date}"
    
class CoupleMessage(models.Model):
    message = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    cloupe = models.ForeignKey(Cloupe, on_delete=models.CASCADE, related_name='messages')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message-creator')

    def __str__(self):
        return self.message
    
class CoupleWishList(models.Model):
    message = models.CharField(max_length=255)
    completed = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    cloupe = models.ForeignKey(Cloupe, on_delete=models.CASCADE, related_name='wishlists')

    def __str__(self):
        return self.message
    
class CoupleImage(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='couple_images')
    created = models.DateTimeField(auto_now_add=True)
    cloupe = models.ForeignKey(Cloupe, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.name