from django.db import models
from project.models import Project
from customuser.models import CustomUser,Jabatan
# Create your models here.
class Peran(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class ProjectHandle(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    peran = models.ForeignKey(Peran, on_delete=models.CASCADE)
