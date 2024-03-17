##############################################################################################################
##############################################################################################################
###
###     Glätten und ID-Setzung der normalisierten Dateien
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################

from bs4 import BeautifulSoup as bs
import re


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################

def satzextraktion (data, band, z):
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
            data['id'] = str(band) + "." + str(z)
            z += 1
    # Verzweigungen auflösen
    else:
        temp = str(data)
        if "<p>" in temp or "<h1>" in temp or "<h2>" in temp or "<h3>" in temp or "<h4>" in temp or "<h5>" in temp:
            for t in data.children:
                if t != data:
                    t, z = satzextraktion (t, band, z)
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
            x = re.sub(r'^(\s*)(.*?)(\s*)$', r"\1<p id='" + str(band) + "." + str(z) + r"'>\2</p>\3", x, flags=re.DOTALL)
            data.string.replace_with(x)
            z += 1
        return data, z
    return data, z


def strukturiereDIV(data, band, z = 1):
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
            child, z = strukturiereDIV(child, band, z)
        # Setze ansonsten ids
        else:
            #print(child)
            child, z = satzextraktion(child, band, z)

    return data, z


def erstelle_plaintext (data):
    """
        Plaintext erstellen
        Input: 
            data:   bs4,    Beautiful Soup Element der zu bearbeitenden Datei 
                ! zu bearbeitende Textstellen sollten bereits mit id-tag ausgezeichnet sein
        Output:
            list,   Liste mit Stringelementen (den Absätzen)
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    ret = ""
    z = 0
    # Lese alle Tags mit id aus
    for inh in data.find_all(id=True):
        
        # Alle Tags sollten eine Überschrift oder Absatz sein
        if inh.name == "h1" or inh.name == "h2" or inh.name == "h3" or inh.name == "h4" or inh.name == "h5" or inh.name == "p":
            t = str(inh)
            t = re.sub("\s+", " ", t)
            # Absätze die nur fremdsprachlichen Text, nur Datum oder nur röm. Ziffern beinhalten werden entfernt
            temp = re.sub("<foreign(.*?)>(.*?)</foreign>", "", t)
            temp = re.sub("<num rendition=\"#roman\"(.*?)>(.*?)</num>", "", temp)
            temp = re.sub("<date(.*?)>(.*?)</date>", "", temp)
            temp = re.sub("<(.*?)>", "", temp)
            temp = re.sub("\s+", " ", temp)
            if temp == " " or temp == "":
                t = ""
            t = re.sub("<(.*?)>", "", t)
            t = re.sub("\s+", " ", t)
            t = t.strip()
            # Nichtleere Strings werden aufgenommen (leere Strings sollten eigentlich nicht vorkommen)
            if not t == " " and not t == "":
                # lange foreign-tags werden herausgenommen
                def verringere_latein(matchobj):
                    print(matchobj.group(0))
                    if matchobj.group(0).split(" ") >= 5:
                        return ''
                    else: 
                        return matchobj.group(0)
                t = re.sub(r"<foreign.*?>(.*?)</foreign>", verringere_latein, t, flags=re.DOTALL)
                ret += " " + t
        # ... ansonsten: Probleme aufzeigen
        else:
            print("Es gab ein Problem mit den Inhalten eines Tags mit ID. Sie hat nicht das geforderte Format (h1-5 oder p):")
            print(inh.name)
        
        
    return ret


##############################################################################################################
##
##      Programm
##
##############################################################################################################

# Datei einlesen
for i in range(1,10):
    pfad = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/" + str(i) + ".xml"
    f = open(pfad)
    tei = f.read()
    if i == 3 or i == 9:
        tei = re.sub(r"<tei:(.*?)>", r"<\1>", tei)
        tei = re.sub(r"</tei:(.*?)>", r"</\1>", tei)

    tei = re.sub(r"<w.*?norm=\"(.*?)\".*?</w>", r"\1", tei, flags=re.DOTALL)
    tei = re.sub(r"<s xml:id=\".*?\">(.*?)</s>", r"\1", tei, flags=re.DOTALL)
    tei = re.sub(r"<note.*?</note>", r"", tei, flags=re.DOTALL)
    tei = re.sub(r"<ref.*?</ref>", r"", tei, flags=re.DOTALL)

    tei = re.sub(r"u\.\s*?s\.\s*?w\.", r"und so weiter", tei)
    tei = re.sub(r"u\.\s*?s\.\s*?f\.", r"und so fort", tei)
    tei = re.sub(r"u\.\s*?d\.\s*?g\.", r"und dergleichen", tei)
    tei = re.sub(r"u\.\s*?d\.\s*?gl\.", r"und dergleichen", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?dgl\.", r"und dergleichen", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?dg\.", r"und dergleichen", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?dergl\.", r"und dergleichen", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?d\.\s*?m\.", r"und dergleichen mehr", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?d\.\s*?gl\.\s*?m\.", r"und dergleichen mehr", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?a\.\s*?m\.", r"und andere mehr", tei, flags=re.DOTALL)
    tei = re.sub(r"a\.\s*?a\.\s*?O\.", r"am angegebenen Orte", tei, flags=re.DOTALL)

    tei = re.sub(r"z\.\s*?Merkm\.", r"zum Merkmal", tei, flags=re.DOTALL)

    tei = re.sub(r"d\.\s*?i\.", r"das heißt", tei, flags=re.DOTALL)
    tei = re.sub(r"d\.\s*?h\.", r"das heißt", tei, flags=re.DOTALL)
    tei = re.sub(r"D\.\s*?i\.", r"Das heißt", tei, flags=re.DOTALL)
    tei = re.sub(r"z\.\s*?E\.", r"zum Beispiel", tei, flags=re.DOTALL)
    tei = re.sub(r"Z\.\s*?E\.", r"Zum Beispiel", tei, flags=re.DOTALL)
    tei = re.sub(r"z\.\s*?B\.", r"zum Beispiel", tei, flags=re.DOTALL)
    tei = re.sub(r"Z\.\s*?B\.", r"Zum Beispiel", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?f\.", r"und folgende", tei, flags=re.DOTALL)
    tei = re.sub(r"u\.\s*?a\.", r"und andere", tei, flags=re.DOTALL)
    tei = re.sub(r"i\.\s*?J\.", r"im Jahr", tei, flags=re.DOTALL)
    tei = re.sub(r"N\.\s*?T\.", r"Neues Testament", tei, flags=re.DOTALL)

    tei = re.sub(r"usw\.", r"und so weiter", tei, flags=re.DOTALL)
    tei = re.sub(r"Hr\.", r"Herr", tei, flags=re.DOTALL)
    tei = re.sub(r"Hrn\.", r"Herrn", tei, flags=re.DOTALL)
    tei = re.sub(r"Dr\.", r"Doktor", tei, flags=re.DOTALL)
    tei = re.sub(r"Bd\.", r"Band", tei, flags=re.DOTALL)
    tei = re.sub(r"St\.", r"Sankt", tei, flags=re.DOTALL)
    tei = re.sub(r"Nr\.", r"Nummer", tei, flags=re.DOTALL)
    tei = re.sub(r"Vf\.", r"Verfasser", tei, flags=re.DOTALL)
    tei = re.sub(r"etc\.", r"etcetera", tei, flags=re.DOTALL)

    tei = re.sub(r"\s+", r" ", tei, flags=re.DOTALL)

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
    data.body, z = strukturiereDIV(data.body, i)

    # Datei speichern
    f = open("Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/bearbeitet/" + str(i) + "_out.xml", "a")
    f.write(data.prettify(formatter=None))
    f.close()

    # Plaintextdatei erstellen
    data.find(type = "footnotes").decompose()
    text = erstelle_plaintext(data)
    f = open("Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/bearbeitet/" + str(i) + "_string.txt", "a")
    f.write(text)
    f.close()

    