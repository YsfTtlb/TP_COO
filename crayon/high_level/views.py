# Create your views here.

from django.http import JsonResponse
from django.views import View
from .models import Ville, Usine, Ressource, Etape, Produit


class VilleDetailView(View):
    def get(self, request, pk):
        ville = Ville.objects.get(pk=pk)
        return JsonResponse(ville.json())


class UsineDetailView(View):
    def get(self, request, pk):
        usine = Usine.objects.get(pk=pk)
        return JsonResponse(usine.json())


class RessourceDetailView(View):
    def get(self, request, pk):
        ressource = Ressource.objects.get(pk=pk)
        return JsonResponse(ressource.json())


class EtapeDetailView(View):
    def get(self, request, pk):
        etape = Etape.objects.get(pk=pk)
        return JsonResponse(etape.json())


class ProduitDetailView(View):
    def get(self, request, pk):
        produit = Produit.objects.get(pk=pk)
        return JsonResponse(produit.json())
