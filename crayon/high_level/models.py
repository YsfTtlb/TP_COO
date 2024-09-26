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

    def __str__(self):
        return f"{self.nom}"


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    numero_de_serie = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def costs(self):
        return self.prix


class Usine(Local):
    machines = models.ManyToManyField(Machine)

    def __str__(self):
        return f"{self.nom}"

    def costs(self):
        total_machine_costs = sum(machine.costs() for machine in self.machines.all())
        surface_costs = self.surface * self.ville.prix
        total_costs = total_machine_costs + surface_costs
        return total_costs


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

    def __str__(self):
        return f"{self.objet}"


class QuantiteRessource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ressource}"

    def costs(self):
        return self.quantite * self.ressource.prix


class Etape(models.Model):
    nom = models.CharField(max_length=100)
    machine = models.ManyToManyField(Machine)
    quantite_ressource = models.ManyToManyField(Ressource)
    duree = models.IntegerField()
    etape_suivante = models.ForeignKey(
        "self", null=True, on_delete=models.PROTECT, blank=True
    )

    def __str__(self):
        return f"{self.nom}"


class Produit(Objet):
    premiere_etape = models.ForeignKey(
        Etape, null=True, on_delete=models.PROTECT, blank=True
    )

    def __str__(self):
        return f"{self.nom}"
