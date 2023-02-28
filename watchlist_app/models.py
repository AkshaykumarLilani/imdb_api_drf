from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    # when anyone is going to access any object of this class, then we will return the name of the object.
    def __str__(self):
        return self.name