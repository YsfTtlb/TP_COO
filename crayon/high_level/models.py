from django.db import models


# Create your models here.
class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postale = models.IntegerField()
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"
