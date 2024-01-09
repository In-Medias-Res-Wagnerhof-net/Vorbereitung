### Absatzweise Markierung der Daten mit id

from bs4 import BeautifulSoup as bs
import re

def satzextraktion (data, z):
    """
        Unterteilung der Daten in Satz
        Input: 
            data:   Liste,      durchsucheDIV - Ergebnis
            head:   Integer,    Umgang mit Überschriften
                    0:  weglassen
                    1:  mit Auszeichnung und mit Kommentaren übernehmen
                    2:  mit Auszeichnung und ohne Kommentaren übernehmen
                    3:  ohne Auszeichnung und ohne Kommentaren übernehmen
                    ! Standardmäßig wird sie mit Auszeichnung und mit Kommentaren übernommen
                    ! Wenn keine genannte Zahl gesetzt wird, wird weggelassen
        Output:
            Liste, Liste mit Sätzen
                ! Gibt es keinen Treffer, wird ein leerer String zurückgegeben
    """
    # p- &h-tags mit id auszeichnen
    if data.name == "h1" or data.name == "h2" or data.name == "h3" or data.name == "h4" or data.name == "h5" or data.name == "p":
        if data.name != "p":
            t = str(data)
            t = re.sub("\s+", " ", t)
            t = re.sub('<[^!].*?/?>', "", t)
            t = re.sub("\s+", " ", t)
            t = t.strip()
            if not t == " " and not t == "":
                data['id'] = z
                z += 1
        else:
            t = str(data)
            t = re.sub("\s+", " ", t)
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
            #temp = re.split("<p>", temp)
            for t in data.children:
                if t!=data:
                    t, z = satzextraktion (t, z)
        print(data)
        return data, z
    
    # Strings mit id auszeichnen
    if(data.name==None):
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
    if data == None:
        print("---None---") 
        return None
    
    for child in data: 
        if child.name == "div" and child.has_attr("n"):
            child, z = strukturiereDIV(child, z)
        else:
            #print(child)
            child, z = satzextraktion(child, z)
    return data, z


band = 1
pfad = "Daten/Kant-Abt1-TEI-vorlaeufig/" + str(band) + ".xml"
f = open(pfad)
tei = f.read()
data = bs(tei, 'xml')
f.close()
for pb in data.find_all("pb"):
    pb.decompose()
for lb in data.find_all("lb"):
    lb.decompose()
for chapter in data.find_all(n="3"):
    for h in chapter.find_all("head"):
        h.name = "h5"
for chapter in data.find_all(n="2"):
    for h in chapter.find_all("head"):
        h.name = "h4"
for chapter in data.find_all(n="1"):
    for h in chapter.find_all("head"):
        h.name = "h3"

data.body, z = strukturiereDIV(data.body)

print(z)

f = open("Daten/Kant-Abt1-TEI-vorlaeufig/" + str(band) + "_out.xml", "a")
f.write(data.prettify(formatter=None))
f.close()