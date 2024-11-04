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
import pickle


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
    alleidsnorm, alledokumentenorm, idanzahl, alleidsorig, alledokumenteorig, seitenangaben = bereite_daten(bandanzahl, modelle)
    
    pfad = "Vorbereitung/Daten/Kant/"
    try:
        open(pfad + "alleids")
    except:
        with open(pfad + "alleids", "wb") as fp:    # Pickling
            pickle.dump(alleidsnorm, fp)
    try:
        open(pfad + "idanzahl")
    except:
        with open(pfad + "idanzahl", "wb") as fp:   # Pickling
            pickle.dump(idanzahl, fp)


    # Modell laden
    bi_model = lade_stmodell(modelle)


    # Modellbearbeitungen
    features_docs = vektorenberechnen(bi_model, modelle, alledokumentenorm, bandanzahl)

    # Suche
    suche(bi_model, modelle, features_docs, alleidsnorm, alleidsorig, alledokumenteorig, idanzahl, suchergebnisanzahl, zitmapping=seitenangaben)


elif type(modelle) == list:
    # Suchabfrage wiederholen, solange Modell existiert
    suchen = True
    while suchen:
        suchen = suchmodellabfrage(modelle, bandanzahl, suchergebnisanzahl)

