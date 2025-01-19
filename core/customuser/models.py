from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.hashers import make_password

class Jabatan(models.Model):
    name = models.CharField(max_length=50)

class LevelJabatan(models.Model):
    name = models.CharField(max_length=50)

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='image/',null=True,blank=True)
    qoute = models.TextField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE, blank=True, null=True)
    level_jabatan = models.ForeignKey(LevelJabatan, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    mulai_bekerja = models.DateField(blank=True, null=True)
    keahllian = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            if not self.password: 
                default_password = "12345678"
                self.password = make_password(default_password)  
        super().save(*args, **kwargs)

    def update_password(self, new_password):
        self.password = make_password(new_password) 
        self.save()

    def __str__(self):
        return self.username
    

    