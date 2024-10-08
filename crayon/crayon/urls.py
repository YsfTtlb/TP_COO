"""
URL configuration for crayon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from high_level.views import (
    VilleApiView,
    UsineDetailView,
    RessourceDetailView,
    EtapeDetailView,
    ProduitDetailView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/ville/<int:pk>/", VilleApiView.as_view(), name="ville_api"),
    path("usine/<int:pk>/", UsineDetailView.as_view(), name="usine_detail"),
    path("ressource/<int:pk>/", RessourceDetailView.as_view(), name="ressource_detail"),
    path("etape/<int:pk>/", EtapeDetailView.as_view(), name="etape_detail"),
    path("produit/<int:pk>/", ProduitDetailView.as_view(), name="produit_detail"),
]
