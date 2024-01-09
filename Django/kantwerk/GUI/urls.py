from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dank/", views.dank, name="dank"),
    path("suche/", views.suche, name="suche"),
    path("suche/ergebnis/<str:begriff>/", views.ergebnis, name="ergebnis"),
    path("suche/ergebnis/", views.ergebnisse, name="ergebnisse"),
]

