##############################################################################################################
##############################################################################################################
###
###     Für das Textprozessieren relevante Funktionen
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
import bs4
from bs4 import BeautifulSoup as bs
import re


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################
'''
    Inhalt:
    1. Dateiverarbeitung
    2. Vorbereitung
    3. Strukturierung
    4. Nachbereitung
'''

'''
    1. Dateiverarbeitung
'''
def öffne_Datei(pfad: str):
    '''
        Inhalt einer Datei extrahieren
        Input: 
            pfad:   String,     Pfad zu Datei
        Output:
            String,    Dateiinhalt
    '''
    # Datei einlesen
    f = open(pfad)
    data = f.read()
    f.close()

    return data


def speichere(pfad: str, inhalt: str, form = "w"):
    '''
        Daten abspeichern
        Input: 
            pfad:   String,         Pfad zu Datei
            inhalt: String,         abzuspeichernder Inhalt
            form:   "w" oder "a",   Angabe, ob überschrieben ("w") oder angehängt ("a") werden soll     ! Standardmäßig wird überschrieben
                                        
    '''
    # Datei abspeichern
    f = open(pfad, form)
    f.write(inhalt)
    f.close()

    return


'''
    2. Vorbereitung
'''
def anpassen(tei: str, band: int, satzteilung: bool = True, wortteilung: bool = True, pbs: bool = True):
    '''
        Bereinige die Datei in grundsätzlicher Hinsicht:
            Namespaces angleichen, 
            Normalizerzusätze, Anhänge und Angaben zu Umbrüchen entfernen
            Überschriften als HTML auszeichnen
        Input: 
            tei:            String,     Inhalt einer Tei-Datei
            band:           Integer,    aktueller Band
            satzteilung:    Boolean,    Angabe ob Satzteilung des Normalizers entfernt werden soll
            wortteilung:    Boolean,    Angabe ob Wortteilung des Normalizers entfernt werden soll
            pbs:            Boolean,    Angabe ob Seitenangaben entfernt werden sollen
        Output:
            String,     bereinigter Inhalt
    '''
    # Namespaces vereinheitlichen - nur zur Sicherheit
    if band == 3 or band == 9:
        tei = re.sub(r"<tei:(.*?)>", r"<\1>", tei)
        tei = re.sub(r"</tei:(.*?)>", r"</\1>", tei)

    # Zusätze aus dem Normalizer gegebenenfalls entfernen
    # Wortzusätze
    if wortteilung:
        # inhaltsleere Elemente löschen
        tei = re.sub(r"<w([^>]*?)/>", r"", tei, flags=re.DOTALL)
        # Elemente mit schließendem Tag
        def w_auflösen(matchobj):
            #... mit norm-Angabe
            if (re.search(r"^.*norm=\"(.*?)\".*$", matchobj.group(1))):
                return re.sub(r"^.*norm=\"(.*?)\".*$", r"\1", matchobj.group(1))
            #...ohne
            else: 
                return matchobj.group(2)
        tei = re.sub(r"<w(.*?)>(.*?)</w>", w_auflösen, tei, flags=re.DOTALL)
    # Satzzusätze
    if satzteilung:
        tei = re.sub(r"<s xml:id=\".*?\">(.*?)</s>", r"\1", tei, flags=re.DOTALL)

    # Beautiful Soup erstellen
    data = bs(tei, 'xml')

    # Fußnoten, Marginalia und Appendix entfernen
    if data.find(type = "footnotes"):
        data.find(type = "footnotes").decompose()
    if data.find(type = "marginalia"):
        data.find(type = "marginalia").decompose()
    if data.find(type = "appendix"):
        data.find(type = "appendix").decompose()

    # Datei von Seiten- und Zeilenumbrüchen bereinigen
    if pbs:
        for pb in data.find_all("pb"):
            pb.decompose()
    else:
        for pb in data.find_all("pb"):
            if pb.has_attr("ed"):
                pb.decompose()
    for lb in data.find_all("lb"):
        lb.decompose()

    # Überschriften auszeichnen
    for chapter in data.find_all(n="9"):
        for h in chapter.find_all("head"):
            h.name = "h9"
    for chapter in data.find_all(n="8"):
        for h in chapter.find_all("head"):
            h.name = "h8"
    for chapter in data.find_all(n="7"):
        for h in chapter.find_all("head"):
            h.name = "h7"
    for chapter in data.find_all(n="6"):
        for h in chapter.find_all("head"):
            h.name = "h6"
    for chapter in data.find_all(n="5"):
        for h in chapter.find_all("head"):
            h.name = "h5"
    for chapter in data.find_all(n="4"):
        for h in chapter.find_all("head"):
            h.name = "h4"
    for chapter in data.find_all(n="3"):
        for h in chapter.find_all("head"):
            h.name = "h3"
    for chapter in data.find_all(n="2"):
        for h in chapter.find_all("head"):
            h.name = "h2"
    for chapter in data.find_all(n="1"):
        for h in chapter.find_all("head"):
            h.name = "h1"
    
    return str(data)


def abkürzungen_auflösen(tei: str):
    '''
        Löse Abkürzungen auf
        Input: 
            tei:    String,     String mit Abkürzungen
        Output:
            String, bearbeiteter String
    '''
    # Abkürzungen auflösen
    # 3 Zeichenkombinationen
    tei = re.sub(r"a\.\s*?a\.\s*?O\.", r"an angegebenem Orte", tei)
    tei = re.sub(r"u\.\s*?a\.\s*?m\.", r"und andere mehr", tei)
    tei = re.sub(r"u\.\s*?s\.\s*?w\.", r"und so weiter", tei)
    tei = re.sub(r"u\.\s*?s\.\s*?f\.", r"und so fort", tei)
    # Abkürzungen zu "und dergleichen (mehr)"
    tei = re.sub(r"u\.\s*?d\.\s*?g\.", r"und dergleichen", tei)
    tei = re.sub(r"u\.\s*?d\.\s*?gl\.", r"und dergleichen", tei)
    tei = re.sub(r"u\.\s*?dgl\.", r"und dergleichen", tei)
    tei = re.sub(r"u\.\s*?dg\.", r"und dergleichen", tei)
    tei = re.sub(r"u\.\s*?dergl\.", r"und dergleichen", tei)
    tei = re.sub(r"u\.\s*?d\.\s*?m\.", r"und dergleichen mehr", tei)
    tei = re.sub(r"u\.\s*?d\.\s*?gl\.\s*?m\.", r"und dergleichen mehr", tei)

    # 2 Zeichenkombinationen
    tei = re.sub(r"d\.\s*?i\.", r"das heißt", tei)
    tei = re.sub(r"d\.\s*?h\.", r"das heißt", tei)
    tei = re.sub(r"D\.\s*?i\.", r"Das heißt", tei)
    tei = re.sub(r"z\.\s*?E\.", r"zum Beispiel", tei)
    tei = re.sub(r"Z\.\s*?E\.", r"Zum Beispiel", tei)
    tei = re.sub(r"z\.\s*?B\.", r"zum Beispiel", tei)
    tei = re.sub(r"Z\.\s*?B\.", r"Zum Beispiel", tei)
    tei = re.sub(r"u\.\s*?f\.", r"und folgende", tei)
    tei = re.sub(r"u\.\s*?a\.", r"und andere", tei)
    tei = re.sub(r"i\.\s*?J\.", r"im Jahr", tei)
    tei = re.sub(r"N\.\s*?T\.", r"Neues Testament", tei)
    tei = re.sub(r"z\.\s*?Merkm\.", r"zum Merkmal", tei)

    # 1 Zeichenkombination
    tei = re.sub(r"usw\.", r"und so weiter", tei)
    tei = re.sub(r"Hr\.", r"Herr", tei)
    tei = re.sub(r"Hrn\.", r"Herrn", tei)
    tei = re.sub(r"Dr\.", r"Doktor", tei)
    tei = re.sub(r"Bd\.", r"Band", tei)
    tei = re.sub(r"St\.", r"Sankt", tei)
    tei = re.sub(r"Nr\.", r"Nummer", tei)
    tei = re.sub(r"Vf\.", r"Verfasser", tei)
    tei = re.sub(r"etc\.", r"etcetera", tei)

    # Whitespaces Bereinigen
    tei = re.sub(r"\s+", r" ", tei, flags=re.DOTALL)

    return tei


def lösche_kinder(data: bs4.element, tagname: list):
    '''
        Lösche alle Kindknoten, die in tagname enthalten sind
        Input: 
            data:       bs4,    Beautiful Soup Element, dessen Kindknoten gelöscht werden sollen
            tagname:    list,   Liste mit zu löschenden Tag-Namen
        Output:
            bs4,    Beautiful Soup Element ohne Tag-Elemente, die in tagname enthalten sind
    '''
    # alle Kindelemente durchgehen
    for c in data.children:
        # Falls es ein entsprechender Tag ist, lösche ihn...
        if c.name in tagname:
            c.decompose()
        # ... ansonsten: versuche weitere Knoten rekursiv bei Kindeskindern ausfindig zu machen und zu löschen
        else:
            try:
                if len(c.contents) > 0:
                    lösche_kinder(c, tagname)
            except:
                None
    
    return data


'''
    3. Strukturierung
'''
def satzextraktion (data: bs4.element, band: int, z: int):
    '''
        Unterteilung der Daten in Absätze und Auszeichnung dieser mit einer ID
            ! Gibt es keinen Änderungen, wird data unverändert zurückgegeben
        Input: 
            data:   bs4,        DIV-Inhalte
            band:   Integer,    aktueller Band
            z:      Integer,    ID-Zähler
        Output:
            bs4,    DIV-Inhalte mit ausgezeichneten ids
            Integer,        aktueller Stand des Zählers
    '''
    # Strings mit id auszeichnen
    if data.name == None:
        # Bereinigen
        t = str(data)
        t = re.sub("<(.*?)>", "", t, flags=re.DOTALL)
        t = re.sub("\s+", " ", t)
        t = t.strip()
        # Tags auszeichnen, die auch bereinigt nicht leer sind
        if len(t) > 1:
            x = str(data)
            x = re.sub(r'^(\s*)(.*?)(\s*)$', r"\1<p id='" + str(band) + "." + str(z) + r"'>\2</p>\3", x, flags=re.DOTALL)
            data.string.replace_with(x)
            z += 1
        return data, z
    
    # p- & h-tags mit id auszeichnen
    h = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
    if data.name in h or data.name == "p":
        # Bereinigen
        t = str(data)
        t = re.sub("<(.*?)>", "", t, flags=re.DOTALL)
        t = re.sub("\s+", " ", t)
        t = t.strip()
        # Tags auszeichnen, die auch bereinigt nicht leer sind
        if len(t) > 1:
            data['id'] = str(band) + "." + str(z)
            z += 1

    # Verzweigungen auflösen
    else:
        temp = str(data)
        if "<p>" in temp or "<h1>" in temp or "<h2>" in temp or "<h3>" in temp or "<h4>" in temp or "<h5>" in temp or "<h6>" in temp or "<h7>" in temp or "<h8>" in temp or "<h9>" in temp:
            for t in data.children:
                if t != data:
                    t, z = satzextraktion (t, band, z)
    
    return data, z


def strukturiereDIV(data: bs4.element, band: int, z: int = 1):
    '''
        DIVs untersuchen und Absätze mit ID versehen
            ! Gibt es keinen Änderungen, wird data unverändert zurückgegeben
        Input: 
            data:   bs4,        Beautiful Soup body-Element der zu bearbeitenden Datei 
            band:   Integer,    aktueller Band
            z:      Integer,    ID-Zähler
        Output:
            bs4,    Dateiinhalt mit ausgezeichneten ids
            Integer,        aktueller Stand des Zählers
    '''
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
            child, z = satzextraktion(child, band, z)

    return data, z


'''
    4. Nachbereitung
'''
def erstelle_plaintext (data: bs4.element, nl: bool = False, teiler: str = None):
    '''
        Plaintext erstellen
                ! zu bearbeitende Textstellen müssen bereits mit id-tag ausgezeichnet sein
                ! Gibt es trotz id-tag keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
        Input: 
            data:   bs4,        Beautiful Soup Element der zu bearbeitenden Datei 
            nl:     Boolean,    Angabe, ob ein Zeilenumbruch vor den Ausgabestring gesetzt werden soll
            teiler: String,     Name des Tags, an dem geteilt werden soll (bspw. "p")
                                ! Default (None) werden alle Elemente mit IDs herangezogen
        Output:
            String, String mit den Textteilen getrennt mit Zeilenumbruch (alle Textteile)
            String, String mit den Textteilen getrennt mit Zeilenumbruch (jedes 10te Textteil nicht)
            String, String mit den Textteilen getrennt mit Zeilenumbruch (nur jedes 10te Textteil)
    '''
    # Initialisierungen
    ges = ""
    train = ""
    eval = ""
    z = 1

    # Lese alle Tags mit gegebenem Namen aus oder...
    if teiler != None:
        for inh in data.find_all(teiler):
            
            # Teilung in Trainingsdaten und Evaluationsdaten - jeder zehnte Absatz wird für die Evaluation vorgesehen
            if z%10 == 0:
                if eval == "":
                    eval += plain(inh)
                else:
                    eval += plain(inh, True)
            else:
                if train == "":
                    train += plain(inh)
                else:
                    train += plain(inh, True)
            z += 1
            if ges == "":
                ges += plain(inh)
            else:
                ges += plain(inh, True)
            
        if nl:
            return "\n" + ges, "\n" + train, "\n" + eval
        else:
            return ges, train, eval
        
    # ... lese alle Tags mit gesetzter id aus
    else:
        for inh in data.find_all(id=True):
            
            # Alle Tags sollten eine Überschrift oder Absatz sein
            h = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
            if inh.name in h or inh.name == "p":

                # Teilung in Trainingsdaten und Evaluationsdaten - jeder zehnte Absatz wird für die Evaluation vorgesehen
                if z%10 == 0:
                    if eval == "":
                        eval += plain(inh)
                    else:
                        eval += plain(inh, True)
                else:
                    if train == "":
                        train += plain(inh)
                    else:
                        train += plain(inh, True)
                z += 1
                if ges == "":
                    ges += plain(inh)
                else:
                    ges += plain(inh, True)
                
            # ... ansonsten: Probleme aufzeigen
            else:
                print("Es gab ein Problem mit den Inhalten eines Tags mit ID. Sie hat nicht das geforderte Format (h1-5 oder p):")
                print(inh.name)
            
        if nl:
            return "\n" + ges, "\n" + train, "\n" + eval
        else:
            return ges, train, eval


def plain(data: bs4.element, nl: bool = False):
    '''
        Plaintext pro Einheit erstellen
        Input: 
            data:   bs4,        Beautiful Soup Element des zu bearbeitenden Elements
            nl:     Boolean,    Angabe, ob ein Zeilenumbruch vor den Ausgabestring gesetzt werden soll
        Output:
            String, String mit dem bereinigten Element
    '''
    # Initialisierungen
    t = re.sub("\s+", " ", str(data))
    
    # Absätze die nur fremdsprachlichen Text, nur Datum oder nur röm. Ziffern beinhalten werden entfernt
    temp = re.sub("<foreign(.*?)>(.*?)</foreign>", "", t)
    temp = re.sub("<num rendition=\"#roman\"(.*?)>(.*?)</num>", "", temp)
    temp = re.sub("<date(.*?)>(.*?)</date>", "", temp)
    temp = re.sub("<(.*?)>", "", temp)
    temp = re.sub("\s+", " ", temp)
    temp = temp.strip()
    temp = re.sub("^(.\s)+", "", temp)
    temp = re.sub("(\s.)+$", "", temp)
    if len(temp) <= 7 or not data.find_parents("foreign") == [] or not data.find_parents("num") == [] or not data.find_parents("date") == []:
        return ""
    
    # lange foreign-tags werden herausgenommen (plus gegebenenfalls sie umgebende Klammern)
    def verringere_fremdsprachen(matchobj):
        txt = matchobj.group(1)
        txt = re.sub("<(.*?)>", "", txt)
        txt = re.sub("\s+", " ", txt).strip()
        if len(txt.split(" ")) > 5:
            return ''
        else: 
            return matchobj.group(0)
    t = re.sub(r"<foreign.*?>(.*?)</foreign>", verringere_fremdsprachen, t, flags=re.DOTALL)
    t = re.sub(r"\s*\(\s*\)", r"", t)
    
    # Bereinigung der Strings
    t = re.sub("<(.*?)>", "", t)
    t = re.sub("\s+", " ", t)
    t = t.strip()
    t = re.sub("^(.\s)+", "", t)
    t = re.sub("(\s.)+$", "", t)
    # Nichtleere Strings werden zurückgegeben (leere Strings sollten eigentlich nicht vorkommen)
    if t == " " or t == "":
        return ""
    else:
        if nl:
            return "\n" + t
        else:
            return t
        