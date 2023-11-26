from django.db import models

# Create your models here.

class Mobiles(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price=models.PositiveIntegerField()
    brand=models.CharField(max_length=200)
    specs=models.CharField(max_length=200)
    display=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",null=True)

    def __str__(self):
        return self.name
