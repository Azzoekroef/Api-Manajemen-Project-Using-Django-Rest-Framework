from django.db import models
from project.models import Project
from customuser.models import CustomUser

# Create your models here.
class Note(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    costumuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return self.note[0:20]


