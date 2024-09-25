from django.db import models


# Create your models here.
class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postale = models.IntegerField()
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    surface = models.IntegerField()

    class Meta:
        abstract = True


class SiegeSocial(Local):
    pass


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    numero_de_serie = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"


class Usine(Local):
    machines = models.ManyToManyField(Machine)


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    class Meta:
        abstract = True


class Ressource(Objet):
    pass

    def __str__(self):
        return f"{self.nom}"


class Stock(models.Model):
    objet = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    nombre = models.IntegerField()


class QuantiteRessource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ressource}"


class Etape(models.Model):
    nom = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    quantite_ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    duree = models.IntegerField()
    etape_suivante = models.ForeignKey(
        "self", null=True, on_delete=models.PROTECT, blank=True
    )


class Produit(Objet):
    premiere_etape = models.ForeignKey(Etape, on_delete=models.PROTECT)
