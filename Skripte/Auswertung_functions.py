##############################################################################################################
##############################################################################################################
###
###     Für die Auswertung relevante Funktionen
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
from Textprozess_functions import öffne_Datei
from Anwendung_functions import lade_stmodell, bereite_daten, vektorenberechnen, suche_absatz

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################
def erhalte_eingaben (pfad:str = "Vorbereitung/Daten/Auswertung/Auswertungseingaben.txt"):
    """
        Gibt Datei an Zeilenumbrüchen gespalten als Liste zurück
        Input: 
            pfad        String,     (optional) Pfad zu Daten
        Output:
            list,       Dateiinhalt, getrennt an Zeilenumbruch
                ! Fehler wird abgefangen und False gesetzt
    """
    # Versuche Datei zu öffnen und zu splitten
    try:
        data = öffne_Datei(pfad).split("\n")

        return data
    except:
        return False
    

def suchen(eingaben:list, modellname:str, bandanzahl:int = 10, suchergebnisanzahl:int = 10):
    """
        Führe Suche aus
        Input: 
            eingaben:           Liste,      Liste der Suchanfragen
            modellname:         String,     Name des genutzten Modells
            bandanzahl:         Integer,    Anzahl der miteinzubeziehenden Bände
            suchergebnisanzahl: Integer,    Anzahl der miteinzubeziehenden Suchergebnisse
        Output:
            list,       Ergebnislisten pro Frage - [[{"ID": id, "Absatz": abs}}...][{"ID": id, "Absatz": abs}}...]...]
    """
    print("Suchabfrage für Modell " + modellname)
    # Relevante Informationen laden
    modell = lade_stmodell(modellname)
    alleidsnorm, alledokumentenorm, idanzahl, alleidsorig, alledokumenteorig = bereite_daten(bandanzahl, modellname)
    features_docs = vektorenberechnen(modell, modellname, alledokumentenorm, bandanzahl)

    ## Suche durchführen
    # Initialisieren
    queries = []
    erg = []
    
    # Query bereiten
    for eingabe in eingaben:
        if "bielectra" in modellname:
            queries.append(eingabe.lower())
        else:
            queries.append(eingabe)
    
    ## Bearbeitung der Abfrage
    print("Erstelle Text Vektoren...")
    # Vektoren- und Ähnlichkeitsberechnung
    features_queries = modell.encode(queries)
    sim = cosine_similarity(features_queries, features_docs)

    # Ausgabe der Ergebnisse
    for i, query in enumerate(queries):
        # sortieren
        ranking = np.argsort(-sim[i])
        print("Query:", query)
        erg.append([])
        for j, r in enumerate(ranking[:suchergebnisanzahl]):
            # Absatz erhalten
            abs, aid = suche_absatz(alleidsnorm, alleidsorig, alledokumenteorig, idanzahl, r, True)
            if not abs == False:
                print(f"[Übereinstimmung zu Ergebnis {j+1}: {sim[i, r]: .3f}]")
                print(abs)
                print()
                erg[i].append({"ID": aid, "Absatz": abs})
            else:
                print("Es gab ein Problem mit Ergebnis " + str(j+1) + "!")
        print("-"*100)

    return erg