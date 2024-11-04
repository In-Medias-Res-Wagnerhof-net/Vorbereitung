##############################################################################################################
##############################################################################################################
###
###     Für die Nutzung relevante Funktionen
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
from Training_functions import lade_modell

from bs4 import BeautifulSoup as bs
import re
import pickle

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################
'''
    Inhalt:
    1. Daten laden
    2. Datenvorbereitung
    3. Modell/Vektoren
    4. Suche
'''

'''
    1. Daten laden
'''
def ladeTEI (num: int, normalized:bool = True, pfad:str = "Vorbereitung/Daten/Kant/"):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            num:        Integer,    Nummer des zu öffnenden Bandes
            normalized: Boolean,    (optional) Angabe, ob original oder normalized Datei benutzt wird
            pfad        String,     (optional) Pfad zu Daten
        Output:
            bs4.element,    Dateiinhalt
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Pfad setzen
    if normalized:
        pfad = pfad + "/normalized/mitID/" + str(num) + "_out.xml"
    else:
        pfad = pfad + "/original/mitID/" + str(num) + "_out.xml"

    # Versuche Datei zu öffnen
    try:
        f = open(pfad)
        tei = f.read()
        data = bs(tei, 'xml')
        f.close()
    # ... ansonsten: gebe Fehlermeldung aus
    except IOError:
        print("Die Datei konnte nicht geladen werden.")
        return
    
    return data


'''
    2. Datenvorbereitung
'''
def satzextraktion (data:bs, low:bool = False):
    """
        Gibt alle Elemente mit relevanter ID und ihre IDs zurück
        Input: 
            data:   bs4,        Beautiful Soup Element der zu bearbeitenden Datei 
                                ! zu bearbeitende Textstellen sollten bereits mit id-tag ausgezeichnet sein
            low:    Boolean,    Angabe, ob Kleinschribung verwendet werden soll
        Output:
            list,   Liste mit den IDs
                 ...konkruent...
            list,   Liste mit den Absätzen
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    ids = []
    absätze = []

    # Lese alle Tags mit id aus
    for inh in data.find_all(id=True):
        
        # Alle Tags sollten eine Überschrift oder Absatz sein
        h = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
        if inh.name in h or inh.name == "p":
            text = str(inh)
            text = re.sub("\s+", " ", text)
            # Sonderbearbeitung der Überschriften
            if inh.name != "p":
                text = re.sub('<[^!].*?/?>', "", text)
            # Sonderbearbeitung der Absätze
            else:
                text = re.sub("<(.*?)>", "", text)
            text = re.sub("\s+", " ", text)
            text = text.strip()
            # Nichtleere Strings werden aufgenommen (leere Strings sollten eigentlich nicht vorkommen)
            if not text == " " and not text == "":
                if low:
                    absätze.append(text.lower())
                else:
                    absätze.append(text)
                ids.append(inh["id"])
        # ... ansonsten: Probleme aufzeigen
        else:
            print("Es gab ein Problem mit den Inhalten eines Tags mit id. Sie hat nicht das geforderte Format (h1-9 oder p):")
            print(inh.name)
        
    return ids, absätze


def erstelle_zitmapping (band:int, pfad:str = "Vorbereitung/Daten/Kant/mapping", data:bs = None):
    """
        Speichert Mapping von ID zu Seitenzahl
        Input: 
            band:   Integer,    Angabe, um welchen Band es sich handelt
            pfad:   String,     Speicherpfad für Mapping (ohne Bandnummer)
            data:   bs4,        Beautiful Soup Element der zu Grunde liegenden Datei 
                                ! zu bearbeitende Textstellen sollten bereits mit id-tag ausgezeichnet sein und pb Element mit Seitenzahl haben
        Output:
            dict,   Mapping von ID zu Seiten- und Buchangaben; Form: {id: angaben}
                ! None falls weder Datei noch Daten vorhanden
    """
    # Testen ob Datei existiert
    try:
        with open(pfad+str(band), "rb") as fp:   # Unpickling
            return pickle.load(fp)
    except:
        print("Es konnte keine nutzbare Datei gefunden werden. Sie muss daher neu erstellt werden.")
        if (data == None):
            return None
        
    plist = re.split('<pb n="', str(data.body))
    mapping = {}
    for p in plist:
        ids = re.findall(r'id="(\d+\.\d+)"', p)
        for i in ids:
            mapping[i] = p[:3]

    with open(pfad+str(band), "wb") as fp:      # Pickling
        pickle.dump(mapping, fp)
        
    return mapping


def bereite_daten (bandanzahl:int = 10, modell:str = None, low:bool = None, zit:bool = False):
    """
        Bereite Daten aller Bände vor. Es wird eine ID-Liste und eine Dokumentenliste jeweils für die normalisierten und originalen Dateien aller Bände erstellt sowie ein Mapping, das die Gesamtanzahl der Ids jedes Bandes enthält.
        Input: 
            bandanzahl: Integer,    Anzahl der zu durchsuchenden Bände
            modell:     String,     Modellkürzel
            low:        Boolean,    Angabe, ob mit .lower() Text verändert werden soll
            zit:        Boolean,    Angabe, ob Mapping von ID auf Buch miterstellt werden soll
        Output:
            list,   ID-Liste der normalisierten Datei
            list,   Absatzliste der normalisierten Datei
            list,   Gesamtanzahl an Ids je Band (basierend auf der normalisierten Datei)
            list,   ID-Liste der originalen Datei
            list,   Absatzliste der originalen Datei
            list,   [optional] Liste mit Zitationsmapping
    """
    # Initialisierung und gegebenenfalls low setzen
    alleidsnorm = []
    alledokumentenorm = []
    idanzahl = []
    alleidsorig = []
    alledokumenteorig = []
    czit = []
    if low == None and modell != None:
        if "bi-electra" in modell:
            low = True
        else:
            low = False
    elif low == None:
        low = False

    # Daten lesen und vorbereiten
    print("Lese Datei")
    for i in range(1,bandanzahl):
        # Einlesen und laden der Suchabsätze
        tei = ladeTEI(i)
        ids, docs = satzextraktion(tei, low)
        # Einlesen und laden der Ausgabeabsätze
        teia = ladeTEI(i, False)
        aids, adocs = satzextraktion(teia, low)

        # Seitenangabenliste erstellen
        if zit:
            zitmapping = erstelle_zitmapping(i, data=teia)
            czit.append(zitmapping)

        # geschachtelte Liste und Mapping erstellen
        alleidsnorm.append(ids)
        alledokumentenorm.append(docs)
        idanzahl.append(len(docs))
        # geschachtelte Liste erstellen für Ausgabe
        alleidsorig.append(aids)
        alledokumenteorig.append(adocs)

    if zit:
        return alleidsnorm, alledokumentenorm, idanzahl, alleidsorig, alledokumenteorig, czit
    else:
        return alleidsnorm, alledokumentenorm, idanzahl, alleidsorig, alledokumenteorig


'''
    3. Modell/Vektoren
'''
def lade_stmodell (modellname:str):
    """
        Lade das SentenceTransformerModell mithilfe von Training_functions.py
        Input: 
            modellname:     String, Modellkürzel
        Output:
            SentenceTransformer,    existierendes Sentencetransformermodell
    """
    # Lade Modell
    if "fein" in modellname or "tsdae" in modellname:
        stmodell = lade_modell(modellname, typ="SentenceTransformer", stexist=True)
    else:
        stmodell = lade_modell(modellname, typ="SentenceTransformer")

    return stmodell[0]


def vektorenberechnen (bi_model:SentenceTransformer, modell:str, alledokumentenorm:list, bandanzahl:int = 10):
    """
        Berechne die Vektoren zu den Absätzen, falls nötig; sonst: Lade sie.
        Input: 
            bi_model:           SentenceTransformer,    SentenceTransformermodell, mit dem die Vektoren berechnet werden
            modellname:         String,                 Modellkürzel
            alledokumentenorm:  Liste,                  Liste mit allen normalisierten Absätzen
            bandanzahl:         Integer,                Anzahl der Bände, die beachtet werden sollen
        Output:
            ndarray,    Vektorenliste
    """
    print("Erstelle/Speichere Korpus Model...")
    for i in range(1,bandanzahl):
        print("Band " + str(i))
        p = "Vorbereitung/Daten/Vektoren/" + modell + "/" + str(i) + ".txt"
        # Versuche Vektoren zu Datei zu laden
        try:
            if i == 1:
                features_docs = np.loadtxt(p)
            else:
                features_docs = np.concatenate((features_docs, np.loadtxt(p)))
        # ... ansonsten: Erstelle Vektoren
        except IOError:
            print("Model wird erstellt")
            model = bi_model.encode(alledokumentenorm[i-1])
            if i == 1:
                features_docs = model
            else:
                features_docs = np.concatenate((features_docs, model))
            
            print("Model wird gespeichert")
            np.savetxt(p, model)

    return features_docs


'''
    4. Suche
'''
def suche_absatz (alleidsnorm:list, alleidsorig:list, alledokumenteorig:list, idanzahl:list, absatznummer:int, getid:bool = False, zitmapping:dict = None):
    """
        Gibt den Absatz entsprechend der Id zurück, basierend auf mapping wird zum nächsten Text gesprungen
        Input: 
            alleidsnorm:        Liste,      Liste der Ids, basierend auf den normalisierten Absätzen
            alleidsorig:        Liste,      Liste der Ids, basierend auf den originalen Absätzen
            alledokumenteorig:  Liste,      Liste der Absätze, basierend auf den originalen Absätzen
            idanzahl:           Liste,      Gesamtanzahl an Ids je Band (basierend auf der normalisierten Datei)
            absatznummer:       Integer,    Indize des Absatzes in fortlaufender Form (ohne Bandzusatz)
            getid:              Boolean,    Angabe, ob SID mitgeliefert werden soll
            zitmapping:         Dictionary, Mapping von der ID auf Buch
        Output:
            String, Absatz der zu entsprechender ID zugehörig ist
            String, [optional] entsprechende ID
            String, [optional] Link zu korpora.org
                    ! Falls kein Absatz gefunden werden kann wird false zurückgegeben
    """
    # Bei Band eins beginnend hochzählen
    band = 0
    for m in idanzahl:
        # zu geringe Bände überspringen
        if absatznummer > m-1:
            absatznummer -= m
            band += 1
        # Entsprechendes Element ausgeben
        else:
            break
    # ID speichern
    sid = alleidsnorm[band][absatznummer]
    print("Die ID des gesuchten Absatzes lautet: " + str(sid))
    if zitmapping:
        link = "https://korpora.org/kant/aa0" + str(band+1) + "/" + zitmapping[band][sid] + ".html"

    # Rückgabe des Absatzes in der originalen Absatzliste entsprechend der ID
    try:
        if getid:
            if zitmapping:
                return alledokumenteorig[band][alleidsorig[band].index(str(sid))], sid, link
            else:
                return alledokumenteorig[band][alleidsorig[band].index(str(sid))], sid
        else:
            if zitmapping:
                return alledokumenteorig[band][alleidsorig[band].index(str(sid))], link
            else:
                return alledokumenteorig[band][alleidsorig[band].index(str(sid))]
    except:
        return False


def suche (bi_model:SentenceTransformer, modell:str, features_docs:np.ndarray, alleidsnorm:list, alleidsorig:list, alledokumenteorig:list, idanzahl:list, suchergebnisanzahl:int = 10, zitmapping:dict = None):
    """
        Suche in der Konsole
        Input: 
            bi_model:           SentenceTransformer,    SentenceTransformermodell, mit dem die Vektoren berechnet werden/wurden
            modell:             String,                 Modellkürzel
            features_docs:      NDArray,                Vektorenliste
            alleidsnorm:        Liste,                  Liste der Ids, basierend auf den normalisierten Absätzen
            alleidsorig:        Liste,                  Liste der Ids, basierend auf den originalen Absätzen
            alledokumenteorig:  Liste,                  Liste der Absätze, basierend auf den originalen Absätzen
            idanzahl:           Liste,                  Gesamtanzahl an Ids je Band (basierend auf der normalisierten Datei)
            suchergebnisanzahl: Integer,                Anzahl der angezeigten Suchergebnisse
            zitmapping:         Dictionary,             Mapping von der ID auf Buch
    """
    # Abfrage einer Suchabfrage
    print("Bitte geben Sie einen Suchbegriff ein oder beenden Sie mit 'exit'!")
    inp = input()
    if "bi-electra" in modell:
        inp = inp.lower()

    # Bearbeitung der Abfrage
    while( inp != "exit" ):
        
        queries = [
            inp
        ]

        print("Erstelle Text Vektoren...")
        # Vektoren- und Ähnlichkeitsberechnung
        features_queries = bi_model.encode(queries)
        sim = cosine_similarity(features_queries, features_docs)

        # Ausgabe der Ergebnisse
        for i, query in enumerate(queries):
            # sortieren
            ranking = np.argsort(-sim[i])
            print("Query:", query)
            for j, r in enumerate(ranking[:suchergebnisanzahl]):
                # Absatz erhalten
                if zitmapping:
                    abs, link = suche_absatz(alleidsnorm, alleidsorig, alledokumenteorig, idanzahl, r, zitmapping=zitmapping)
                else:
                    abs = suche_absatz(alleidsnorm, alleidsorig, alledokumenteorig, idanzahl, r, zitmapping=zitmapping)
                if not abs == False:
                    print(f"[Übereinstimmung zu Ergebnis {j+1}: {sim[i, r]: .3f}]")
                    print(abs)
                    if zitmapping:
                        print("Der resultierende Link des gesuchten Absatzes lautet: " + link)
                    print()
                else:
                    print("Es gab ein Problem mit Ergebnis " + str(j+1) + "!")
            print("-"*100)

        # gegebenenfalls erneute Abfrage einer Suchabfrage
        print("Bitte geben Sie einen neuen Suchbegriff ein oder beenden Sie mit 'exit'!")
        inp = input()
        if "bi-electra" in modell:
            inp = inp.lower()


def suchmodellabfrage (modelle:list, bandanzahl:int = 10, suchergebnisanzahl:int = 10):
    """
        Suche in der Konsole mit individuellem Modell
        Input: 
            modelle:            Liste,      Liste der möglichen Modellkürzel
            bandanzahl:         Integer,    Anzahl der zu durchsuchenden Bände
            suchergebnisanzahl: Integer,    Anzahl der angezeigten Suchergebnisse
        Output:
            Boolean,    False, falls eingegebenes Modell nicht in modelle enthalten, sonst True
    """
    # Abfrage des Suchverfahrens
    print("Welches Suchverfahren soll verwendet werden? Es stehen folgende zur Auswahl:")
    print(modelle)
    inp = input()

    # Start der Suche, falls eingegebenes Modellkürzel in modelle vorkommt
    if not inp in modelle:
        return False
    else:
        # Vorbereitung der Suche
        modell = lade_stmodell(inp)
        alleidsnorm, alledokumentenorm, idanzahl, alleidsorig, alledokumenteorig = bereite_daten(bandanzahl, inp)
        features_docs = vektorenberechnen(modell, inp, alledokumentenorm, bandanzahl)

        # Suche durchführen
        suche(modell, inp, features_docs, alleidsnorm, alleidsorig, alledokumenteorig, idanzahl, suchergebnisanzahl)
        return True