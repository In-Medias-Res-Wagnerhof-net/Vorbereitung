##############################################################################################################
##############################################################################################################
###
###     Vereinheitlichung der Datengrundlagen
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


##############################################################################################################
##
##      Programm
##
##############################################################################################################

# Alle Dateien durchgehen
for i in range(1,10):
    
    # Öffnen der normalisierten Datei
    pfad = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/" + str(i) + ".xml"
    f = open(pfad)
    tei = f.read()
    f.close()

    # Namespaces vereinheitlichen
    if i == 3 or i == 9:
        tei = re.sub(r"<tei:(.*?)>", r"<\1>", tei)
        tei = re.sub(r"</tei:(.*?)>", r"</\1>", tei)

    # Zusätze aus dem Normalizer entfernen 
    tei = re.sub(r"<w.*?norm=\"(.*?)\".*?</w>", r"\1", tei, flags=re.DOTALL)
    tei = re.sub(r"<s xml:id=\".*?\">(.*?)</s>", r"\1", tei, flags=re.DOTALL)

    # Fußnoten, Marginalia und Appendix entfernen und Formalia vereinheitlichen
    data = bs(tei, 'xml')
    if data.find(type = "footnotes"):
        data.find(type = "footnotes").decompose()
    if data.find(type = "marginalia"):
        data.find(type = "marginalia").decompose()
    if data.find(type = "appendix"):
        data.find(type = "appendix").decompose()
    text = data.prettify()

    # Datei speichern
    f = open("Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/bearbeitet/" + str(i) + "_pre.txt", "a")
    f.write(text)
    f.close()


    # Öffnen der originalen Datei
    pfad = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/original/" + str(i) + ".xml"
    f = open(pfad)
    tei = f.read()
    f.close()

    # Namespaces vereinheitlichen
    if i == 3 or i == 9:
        tei = re.sub(r"<tei:(.*?)>", r"<\1>", tei)
        tei = re.sub(r"</tei:(.*?)>", r"</\1>", tei)

    # Fußnoten, Marginalia und Appendix entfernen und Formalia vereinheitlichen
    data = bs(tei, 'xml')
    if data.find(type = "footnotes"):
        data.find(type = "footnotes").decompose()
    if data.find(type = "marginalia"):
        data.find(type = "marginalia").decompose()
    if data.find(type = "appendix"):
        data.find(type = "appendix").decompose()
    text = data.prettify()

    # Datei speichern
    f = open("Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/original/bearbeitet/" + str(i) + "_pre.txt", "a")
    f.write(text)
    f.close()
