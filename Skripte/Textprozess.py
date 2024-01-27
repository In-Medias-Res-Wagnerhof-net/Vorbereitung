### Absatzweise Markierung der Daten mit id

## Import externer Bibliotheken
from bs4 import BeautifulSoup as bs
import re


## Funktionen
def satzextraktion (data, z):
    """
        Unterteilung der Daten in Absätze und Auszeichnung dieser mit einer ID
        Input: 
            data:   bs4,        DIV-Inhalte
            z:      Integer,    ID-Zähler
        Output:
            Liste,  Liste mit Sätzen
                ! Gibt es keinen Änderungen, wird data unverändert zurückgegeben
    """
    # p- & h-tags mit id auszeichnen
    if data.name == "h1" or data.name == "h2" or data.name == "h3" or data.name == "h4" or data.name == "h5" or data.name == "p":
        t = str(data)
        t = re.sub("\s+", " ", t)
        if data.name != "p":
            t = re.sub('<[^!].*?/?>', "", t)
        else:
            t = re.sub("<(.*?)>", "", t)
        t = re.sub("\s+", " ", t)
        t = t.strip()
        if not t == " " and not t == "":
            data['id'] = z
            z += 1
    # Verzweigungen auflösen
    else:
        temp = str(data)
        if "<p>" in temp or "<h1>" in temp or "<h2>" in temp or "<h3>" in temp or "<h4>" in temp or "<h5>" in temp:
            for t in data.children:
                if t != data:
                    t, z = satzextraktion (t, z)
        #print(data)
        return data, z
    
    # Strings mit id auszeichnen
    if data.name == None:
        t = str(data)
        t = re.sub("\s+", " ", t)
        t = re.sub("<(.*?)>", "", t)
        t = re.sub("\s+", " ", t)
        t = t.strip()
        if not t == " " and not t == "":
            x = str(data)
            x = re.sub(r'^(\s*)(.*?)(\s*)$', r"\1<p id='" + str(z) + r"'>\2</p>\3", x, flags=re.DOTALL)
            data.string.replace_with(x)
            z += 1
        return data, z
    return data, z


def strukturiereDIV(data, z = 1):
    """
        DIVs untersuchen und Absätze mit ID versehen
        Input: 
            data:   bs4,        Beautiful Soup body-Element der zu bearbeitenden Datei 
            z:      Integer,    ID-Zähler
        Output:
            bs4.element,    Dateiinhalt mit ausgezeichneten ids
            Integer,        Zähler
    """
    # Abbruchbedingung
    if data == None:
        print("---None---") 
        return None
    
    # Gehe alle Elemente durch
    for child in data: 
        # Grabe tiefer in div-Elementen
        if child.name == "div" and child.has_attr("n"):
            child, z = strukturiereDIV(child, z)
        # Setze ansonsten ids
        else:
            #print(child)
            child, z = satzextraktion(child, z)

    return data, z


## Programm
# Datei einlesen
band = 1
pfad = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/original/" + str(band) + ".xml"
f = open(pfad)
tei = f.read()
data = bs(tei, 'xml')
f.close()

# Datei bereinigen
for pb in data.find_all("pb"):
    pb.decompose()
for lb in data.find_all("lb"):
    lb.decompose()

# Überschriften auszeichnen
for chapter in data.find_all(n="3"):
    for h in chapter.find_all("head"):
        h.name = "h5"
for chapter in data.find_all(n="2"):
    for h in chapter.find_all("head"):
        h.name = "h4"
for chapter in data.find_all(n="1"):
    for h in chapter.find_all("head"):
        h.name = "h3"

# Absätze markieren
data.body, z = strukturiereDIV(data.body)
#print(z)

# Datei speichern
f = open("Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/bearbeitet/" + str(band) + "_out.xml", "a")
f.write(data.prettify(formatter=None))
f.close()