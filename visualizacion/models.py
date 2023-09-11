from django.db import models

class Visualizacion(models.Model):
    headline = models.CharField(max_length=250)
    body = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.headline
