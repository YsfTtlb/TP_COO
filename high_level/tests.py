from django.test import TestCase
from .models import Ville, Usine, Machine, Ressource, Stock, QuantiteRessource


class UsineModelTests(TestCase):
    def setUp(self):
        self.ville = Ville.objects.create(nom="Labège", code_postale=31670, prix=2000)
        self.machine1 = Machine.objects.create(
            nom="Scie", prix=1000, numero_de_serie=1683
        )
        self.machine2 = Machine.objects.create(
            nom="Perceuse", prix=2000, numero_de_serie=1684
        )
        self.usine = Usine.objects.create(
            nom="Usine de Labège", ville=self.ville, surface=50
        )
        self.usine.machines.set([self.machine1, self.machine2])
        self.bois = Ressource.objects.create(nom="Bois", prix=10)
        self.mine = Ressource.objects.create(nom="Mine", prix=15)
        Stock.objects.create(objet=self.bois, nombre=1000)
        Stock.objects.create(objet=self.mine, nombre=50)
        QuantiteRessource.objects.create(ressource=self.bois, quantite=1000)
        QuantiteRessource.objects.create(ressource=self.mine, quantite=50)

    def test_usine_costs_calculation(self):
        # on test le calcul du cout total de l'usine avec les machine et la surface

        usine_cost = self.usine.costs()

        expected_machine_cost = 1000 + 2000
        expected_surface_cost = 50 * 2000
        expected_total_cost = expected_machine_cost + expected_surface_cost

        self.assertEqual(usine_cost, expected_total_cost)

    def test_quantite_ressource_costs_calculation(self):
        # on test le calcul des couts pour les quantites de ressources

        # on récupère les quantités de ressources
        bois_quantite = QuantiteRessource.objects.get(ressource=self.bois)
        mine_quantite = QuantiteRessource.objects.get(ressource=self.mine)

        bois_cost = bois_quantite.costs()
        mine_cost = mine_quantite.costs()

        expected_bois_cost = 10000
        expected_mine_cost = 750

        self.assertEqual(bois_cost, expected_bois_cost)
        self.assertEqual(mine_cost, expected_mine_cost)
