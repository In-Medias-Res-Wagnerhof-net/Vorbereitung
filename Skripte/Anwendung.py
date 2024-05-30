##############################################################################################################
##############################################################################################################
###
###     Test der Modelle im Terminal und Erstellung der Vektoren der Bände
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
from Anwendung_functions import *


##############################################################################################################
##
##      Programm
##
##############################################################################################################

# Initialisierungen
bandanzahl = 10                                     # Anzahl der Bände max: 10
suchergebnisanzahl = 20                             # Anzahl der besten Ergebnisse, die aufgelistet werden
modelle = ["convbert", "distilbert"]                # Modell

## Suche
if type(modelle) == str:
    # Bände einlesen
    alleidsnorm, alledokumentenorm, idanzahl, alleidsorig, alledokumenteorig = bereite_daten(bandanzahl, modelle)

    # Modell laden
    bi_model = lade_stmodell(modelle)


    # Modellbearbeitungen
    features_docs = vektorenberechnen(bi_model, modelle, alledokumentenorm, bandanzahl)

    # Suche
    suche(bi_model, modelle, features_docs, alleidsnorm, alleidsorig, alledokumenteorig, idanzahl, suchergebnisanzahl)

elif type(modelle) == list:
    # Suchabfrage wiederholen, solange Modell existiert
    suchen = True
    while suchen:
        suchen = suchmodellabfrage(modelle, bandanzahl, suchergebnisanzahl)

