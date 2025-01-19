from django.db import models

# Create your models here.
class Inventaris_status(models.Model):
    name = models.CharField(max_length=20)

    
    def __str__(self):
        return self.name


class Inventaris(models.Model):
    name = models.CharField(max_length=40)
    tanggal_beli = models.DateField()
    harga = models.IntegerField()
    status = models.ForeignKey(Inventaris_status,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
    