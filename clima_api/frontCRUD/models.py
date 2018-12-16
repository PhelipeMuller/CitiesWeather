from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=25, verbose_name='Name')
    celcius = models.IntegerField(verbose_name='Celcius')
    time_rain = models.IntegerField(verbose_name='Rain')

    def __str__(self):
        return self.name
