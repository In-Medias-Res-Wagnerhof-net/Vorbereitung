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

import re
from bs4 import BeautifulSoup as bs

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################

def ladeTEI (num):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            num:    Integer,    Nummer des zu öffnenden Bandes
        Output:
            bs4.element,    Dateiinhalt
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    pfad = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/mitID/" + str(num) + "_out.xml"

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


def satzextraktion (data):
    """
        Gibt alle Elemente mit relevanter ID zurück
        Input: 
            data:   bs4,    Beautiful Soup Element der zu bearbeitenden Datei 
                ! zu bearbeitende Textstellen sollten bereits mit id-tag ausgezeichnet sein
        Output:
            list,   Liste mit Stringelementen
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    ret = []

    # Lese alle Tags mit id aus
    for inh in data.find_all(id=True):
        
        # Alle Tags sollten eine Überschrift oder Absatz sein
        if inh.name == "h1" or inh.name == "h2" or inh.name == "h3" or inh.name == "h4" or inh.name == "h5" or inh.name == "p":
            t = str(inh)
            t = re.sub("\s+", " ", t)
            # Sonderbearbeitung der Überschriften
            if inh.name != "p":
                t = re.sub('<[^!].*?/?>', "", t)
            # Sonderbearbeitung der Absätze
            else:
                t = re.sub("<(.*?)>", "", t)
            t = re.sub("\s+", " ", t)
            t = t.strip()
            # Nichtleere Strings werden aufgenommen (leere Strings sollten eigentlich nicht vorkommen)
            if not t == " " and not t == "":
                    ret.append(t)
        # ... ansonsten: Probleme aufzeigen
        else:
            print("Es gab ein Problem mit den Inhalten eines Tags mit id. Sie hat nicht das geforderte Format (h1-5 oder p):")
            print(inh.name)
        
    return ret


def suche_absatz (texte, mapping, absatz):
    """
        Gibt den Absatz entsprechend der Id zurück, basierend auf mapping wird zum nächsten Text gesprungen
        Input: 
            texte:      Liste,      Liste aller Elemente mit relevanter ID
            mapping:    Liste,      Angaben, wie viele relevante IDs vergeben wurden (pro Band)
            absatz:     Integer,    Absatz Id in fortlaufender Form (ohne Bandzusatz)
        Output:
            String, Element mit entsprechender ID
    """
    # Bei Band eins beginnend hochzählen
    b = 0
    for m in mapping:
        # zu geringe Bände überspringen
        if absatz > m-1:
            absatz -= m
            b += 1
        # Entsprechendes Element ausgeben
        else:
            return texte[b][absatz], str(b + 1) + "." + str(absatz + 1)


##############################################################################################################
##
##      Programm
##
##############################################################################################################

# Initialisierungen
docs = []
alldocs = []
mapping = []

end = 10                                    # Anzahl der Bände max: 10
K = 10                                      # Anzahl der besten Ergebnisse, die aufgelistet werden
mod = "bi-electra-ms-marco-german-uncased-test"  # Modell

if mod == "gelectra-large-germanquad":
    bi_model = SentenceTransformer("Vorbereitung/Modelle/deepset/gelectra-large-germanquad")
elif mod == "gelectra-large-germanquad-test":
    bi_model = SentenceTransformer("Vorbereitung/Modelle/deepset/gelectra-large-germanquad-test")
elif mod == "distilbert-base-german-cased":
    bi_model = SentenceTransformer("Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased")
elif mod == "distilbert-base-german-cased-test":
    bi_model = SentenceTransformer("Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased-test")
elif mod == "bi-electra-ms-marco-german-uncased":
    bi_model = SentenceTransformer("Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased")
elif mod == "bi-electra-ms-marco-german-uncased-test":
    bi_model = SentenceTransformer("Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-test")
else:
    print("Es gab ein Problem beim Laden des Modells...")
    exit()

# Einlesen der Daten und Vorbereitung
print("Lese Datei")
docs = []
for i in range(1,end):
    # Einlesen und laden der Absätze
    tei = ladeTEI(i)
    docs = satzextraktion(tei)

    # geschachtelte Liste und Mapping erstellen
    alldocs.append(docs)
    mapping.append(len(docs))


'''
# specify documents and queries
docs = [
    "Auf Netflix gibt es endlich die neue Staffel meiner Lieblingsserie.",
    "Der Gepard jagt seine Beute.",
    "Wir haben in der Agentur ein neues System für Zeiterfassung.",
    "Mein Arzt sagt, dass mir dabei eher ein Orthopäde helfen könnte.",
    "Einen Impftermin kann mir der Arzt momentan noch nicht anbieten.",
    "Auf Kreta hat meine Tochter mit Muscheln eine schöne Sandburg gebaut.",
    "Das historische Zentrum (centro storico) liegt auf mehr als 100 Inseln in der Lagune von Venedig.",
    "Um in Zukunft sein Vermögen zu schützen, sollte man andere Investmentstrategien in Betracht ziehen.",
    "Die Ära der Dinosaurier wurde vermutlich durch den Einschlag eines gigantischen Meteoriten auf der Erde beendet.",
    "Bei ALDI sind die Bananen gerade im Angebot.",
    "Die Entstehung der Erde ist 4,5 milliarden jahre her.",
    "Finanzwerte treiben DAX um mehr als sechs Prozent nach oben Frankfurt/Main gegeben.",
    "DAX dreht ins Minus. Konjunkturdaten und Gewinnmitnahmen belasten Frankfurt/Main.",
]
'''


# Modellbearbeitungen
print("Erstelle/Speichere Korpus Model...")
for i in range(1,end):
    print("Band " + str(i))
    p = "Vorbereitung/Daten/Vektoren/" + mod + "/" + str(i) + ".txt"
    # Versuche Vektoren zu Datei zu laden
    try:
        if i == 1:
            features_docs = np.loadtxt(p)
        else:
            features_docs = np.concatenate((features_docs, np.loadtxt(p)))
    # ... ansonsten: Erstelle Vektoren
    except IOError:
        print("Model wird erstellt")
        model = bi_model.encode(alldocs[i-1])
        if i == 1:
            features_docs = model
        else:
            features_docs = np.concatenate((features_docs, model))
        
        print("Model wird gespeichert")
        np.savetxt(p, model)

# Ergebnis
print("Bitte geben Sie einen Suchbegriff ein oder beenden Sie mit 'exit'!")
inp = input()

# Bearbeitung der Abfragen
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
        ranks = np.argsort(-sim[i])
        print(sim[0,0])
        print("Query:", query)
        for j, r in enumerate(ranks[:K]):
            print(r)
            abs, eid = suche_absatz(alldocs, mapping, r)
            print(eid)
            print(f"[{j}: {sim[i, r]: .3f}]", abs)
        print("-"*96)

    print("Bitte geben Sie einen neuen Suchbegriff ein oder beenden Sie mit 'exit'!")
    inp = input()




"""
"""