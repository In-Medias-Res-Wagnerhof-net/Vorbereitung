from django.db import models

# Create your models here.

class Suchbegriff(models.Model):
    '''
        Daten zum Suchbegriff
    '''
    # Suchbegrifftext - Eingabe um Ergebnisse zu finden (es können auch mehrere Begriffe sein)
    suchbegriff_text = models.CharField(max_length=200)
    # Annzahl der Suchen dieser Art
    anzahl = models.IntegerField(default=0)
    # Ergebnisabsatz auf Ergebnisseite - verweist auf ID des Absatzes/der Überschrift
    absatz = models.CharField(max_length=7, default=None)           # Hier wäre eine Liste schön, sodass mehrere Absätze angezeigt werden und vielleicht ein Zähler, welcher am häufigsten angeschaut wurde, aus dem man auswählen kann.

    # Ausgabe ist suchbegriff_text
    def __str__(self):
        return self.suchbegriff_text