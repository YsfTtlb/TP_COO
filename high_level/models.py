from django.db import models


# Create your models here.
class Ville(models.Model):
    nom = models.CharField(max_length=100)
    code_postale = models.IntegerField()
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def json_extend(self):
        return {
            "nom": self.nom,
            "code_postale": self.code_postale,
            "prix": self.prix,
        }


class Local(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.PROTECT)
    surface = models.IntegerField()

    class Meta:
        abstract = True

    def json(self):
        return {
            "nom": self.nom,
            "ville": {
                "nom": self.ville.nom,
                "code_postale": self.ville.code_postale,
                "prix": self.ville.prix,
            },
            "surface": self.surface,
        }


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

    def json(self):
        return {
            "nom": self.nom,
            "prix": self.prix,
            "numero_de_serie": self.numero_de_serie,
        }


class Usine(Local):
    machines = models.ManyToManyField(Machine)

    def __str__(self):
        return f"{self.nom}"

    def costs(self):
        total_machine_costs = sum(machine.costs() for machine in self.machines.all())
        surface_costs = self.surface * self.ville.prix
        total_costs = total_machine_costs + surface_costs
        return total_costs

    def json(self):
        return {
            "nom": self.nom,
            "ville": {
                "nom": self.ville.nom,
                "code_postale": self.ville.code_postale,
                "prix": self.ville.prix,
            },
            "surface": self.surface,
            "machines": [
                {
                    "nom": machine.nom,
                    "prix": machine.prix,
                    "numero_de_serie": machine.numero_de_serie,
                }
                for machine in self.machines.all()
            ],
        }


class Objet(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    class Meta:
        abstract = True

    def json(self):
        return {
            "nom": self.nom,
            "prix": self.prix,
        }


class Ressource(Objet):
    pass

    def __str__(self):
        return f"{self.nom}"


class Stock(models.Model):
    objet = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    nombre = models.IntegerField()

    def __str__(self):
        return f"{self.objet}"

    def json(self):
        return {
            "objet": {
                "nom": self.objet.nom,
                "prix": self.objet.prix,
            },
            "nombre": self.nombre,
        }


class QuantiteRessource(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ressource}"

    def costs(self):
        return self.quantite * self.ressource.prix

    def json(self):
        return {
            "ressource": {
                "nom": self.ressource.nom,
                "prix": self.ressource.prix,
            },
            "quantite": self.quantite,
            "costs": self.costs(),
        }


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

    def json(self):
        return {
            "nom": self.nom,
            "machines": [
                {
                    "nom": machine.nom,
                    "prix": machine.prix,
                    "numero_de_serie": machine.numero_de_serie,
                }
                for machine in self.machine.all()
            ],
            "duree": self.duree,
            "etape_suivante": {
                "nom": self.etape_suivante.nom,
                "duree": self.etape_suivante.duree,
            }
            if self.etape_suivante
            else None,
        }


class Produit(Objet):
    premiere_etape = models.ForeignKey(
        Etape, null=True, on_delete=models.PROTECT, blank=True
    )

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {
            "nom": self.nom,
            "prix": self.prix,
            "premiere_etape": {
                "nom": self.premiere_etape.nom,
                "duree": self.premiere_etape.duree,
            }
            if self.premiere_etape
            else None,
        }
