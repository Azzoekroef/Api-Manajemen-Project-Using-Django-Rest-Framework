from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    mulai = models.DateField()
    estimasi = models.DateField()
    modal = models.IntegerField()
    harga = models.IntegerField()
    desc = models.TextField(null=True,blank=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    progres = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True)
    
    
    def __str__(self):
        return self.name
