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
from Textprozess_functions import öffne_Datei, speichere, anpassen, abkürzungen_auflösen, strukturiereDIV, lösche_kinder, erstelle_plaintext

##############################################################################################################
##
##      Programm
##
##############################################################################################################
'''
    Initialisierung
'''
# Pfade initialisieren
pfado = "../In Medias Res/Vorbereitung/Daten/Kant/original/"
pfadn = "../In Medias Res/Vorbereitung/Daten/Kant/normalized/"
pfadt = "../In Medias Res/Vorbereitung/Daten/Kant/training/"

# Ergebnisvariablen initialisieren
train = ""
eval = ""
sentt = ""
sente = ""

z = 1

'''
    Dateien durchgehen
'''
# Alle Dateien durchgehen
print("Es wird bearbeitet:")
for i in range(1,10):
    print("Band " + str(i))
    
    # Vorlagedateien einlesen
    orig = öffne_Datei(pfado + str(i) + ".xml")
    norm = öffne_Datei(pfadn + str(i) + ".xml")


    ''' Mit Ids ausgestattete xml-Dateien erstellen '''

    ## Original
    # Datei anpassen und auflösen
    odata = bs(
        anpassen(orig, i, True, True), 
        'xml'
    )
    # Absätze markieren
    odata.body, z = strukturiereDIV(odata.body, i)

    # Dateien speichern
    speichere( 
        pfado + "mitID/" + str(i) + "_out.xml", 
        odata.prettify(formatter=None)
    )


    ## Normalisiert
    # Datei anpassen und auflösen
    data = bs(
        abkürzungen_auflösen( anpassen(norm, i) ), 
        'xml'
    )

    # Absätze markieren
    data.body, z = strukturiereDIV(data.body, i)

    # zusätzliche Bereinigung
    for tid in data.find_all(id=True):
        tid = lösche_kinder(tid, ["note", "ref"])

    # Dateien speichern
    speichere( 
        pfadn + "mitID/" + str(i) + "_out.xml", 
        data.prettify(formatter=None)
    )


    ''' Trainings- und Evaluationsdatensatz aus allen Bänden zusammenbauen '''

    ## Absatzweise
    # Datei anpassen und zwischenspeichern
    if train == "" and eval == "":
        train, eval = erstelle_plaintext(data)
    else:
        tempt, tempe = erstelle_plaintext(data, True)
        train += tempt
        eval += tempe


    ## Satzweise
    # Datei anpassen und zwischenspeichern
    # - Satzteilung blibt erhalten, dafür ist keine Trennungen in Absätze nötig
    data = lösche_kinder(
            bs(
                abkürzungen_auflösen( anpassen(norm, i, False ) ), 
                'xml'
            ), 
            ["note", "ref"] 
        )
    
    if sentt == "" and sente == "":
        sentt, sente = erstelle_plaintext(data, teiler="s")
    else:
        tempt, tempe = erstelle_plaintext(data, True, teiler="s")
        sentt += tempt
        sente += tempe
      

# Plaintextdateien erstellen
speichere(pfadt + "train_absatzweise.txt", train)
speichere(pfadt + "eval_absatzweise.txt", eval)
speichere(pfadt + "train_satzweise.txt", sentt)
speichere(pfadt + "eval_satzweise.txt", sente)

# Plaintextdateien mit lower() erstellen
speichere(pfadt + "train_absatzweise_lower.txt", train.lower())
speichere(pfadt + "eval_absatzweise_lower.txt", eval.lower())
speichere(pfadt + "train_satzweise_lower.txt", sentt.lower())
speichere(pfadt + "eval_satzweise_lower.txt", sentt.lower())