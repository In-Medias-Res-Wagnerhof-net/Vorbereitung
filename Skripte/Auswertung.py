##############################################################################################################
##############################################################################################################
###
###     Auswertung der Modelle
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
import csv
from Auswertung_functions import *
    

##############################################################################################################
##
##      Programm
##
##############################################################################################################
# Initialisierung
modelle = ["bielectra", "convbert", "distilbert", "gelectra"]
zusätze = ["training", "training-fein", "tsdae", "tsdae-fein"]

for modell in modelle.copy():
    for zusatz in zusätze:
        if (modell != "distilbert" and modell != "convbert") or not "tsdae" in zusatz:
            modelle.append(modell + "-" + zusatz)
        
eingaben = erhalte_eingaben()

## Überprüfen, ob Dateianzahl stimmt
fileanzahl = 0

# Überprüfen, ob Anzahl der fragenweisen Ergebnisse existieren
for i, e in enumerate(eingaben):
    pfad = 'Vorbereitung/Daten/Auswertung/ergebnis' + str(i) + '.csv'
    try:
        open(pfad)
        fileanzahl += 1
    except:
        continue

# Überprüfen, ob Anzahl der modellweisen Ergebnisse existieren
for modell in modelle:
    pfad = 'Vorbereitung/Daten/Auswertung/modergebnis-' + modell + '.csv'
    try:
        open(pfad)
        fileanzahl += 1
    except:
        continue


## Falls nicht: führe Ergebnisberechnung durch
if  fileanzahl != len(eingaben) + len(modelle):

    ergebnisse = []
    ergebnisseeingabe = []

    # Suchergebnisse für alle Eingaben pro Modell erlangen und speichern
    for modell in modelle:
        # erlangen
        erg = suchen(eingaben, modell)
        # speichern
        pfad = 'Vorbereitung/Daten/Auswertung/modergebnis-' + modell + '.csv'
        with open(pfad, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Absatz']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            
            for i, er in enumerate(erg):
                writer.writerow({'Absatz': eingaben[i]})
                for e in er:
                    writer.writerow(e)
        
        ergebnisse.append(erg)

    # Für manuelle Auswertung fragenweise Ergebnisse zusammenstellen und abspeichern
    # zusammenstellen
    for moderg in ergebnisse:
        for i, eingabeerg in enumerate(moderg):
            try:
                for inh in eingabeerg:
                    dazu = True
                    for e in ergebnisseeingabe[i]:
                        if inh["ID"] == e["ID"]:
                            dazu = False
                            break
                    if dazu:
                        ergebnisseeingabe[i].append(inh)
            except:
                ergebnisseeingabe.insert(i, eingabeerg)
    # speichern
    for i, ein in enumerate(ergebnisseeingabe):
        pfad = 'Vorbereitung/Daten/Auswertung/ergebnis' + str(i) + '.csv'
        with open(pfad, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Absatz', eingaben[i]]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for e in ein:
                writer.writerow(e)
                    
# Abfrage, ob Bewertung durchgeführt wurde
inp = ""

while inp != "j":
    print("Wurden alle Ergebnisse bewertet? [j/n]")
    inp = input().lower()[0]


## Auswertung durchführen
ergebnisse = []
ergebnisseeingabe = []

# Ergebnisse pro Frage und Bewertung einlesen
for i, e in enumerate(eingaben):
    ergebnisse.append([])
    pfad = 'Vorbereitung/Daten/Auswertung/ergebnis' + str(i) + '.csv'
    try:
        with open(pfad, mode="r") as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                # Überprüfen, dass Frage übereinstimmt
                if row[0] == "ID" and row[2] != e:
                    print("Warnung!")
                    print(row[2])
                    print("ist nicht gleich:")
                    print(e)
                    print("Das sollte nicht vorkommen, kann aber möglicherweise mit der Kodierung zusammenhängen. Bitte Daten überprüfen!")
                if row[0] != "ID":
                    ergebnisse[i].append({"ID": row[0], "Absatz": row[1], "Bewertung": row[2]})
    except:
        print("Es gab ein Problem beim einlesen der Datei: " + pfad)
        exit()

# Ergebnisse pro Modell einlesen
for i, modell in enumerate(modelle):
    ergebnisseeingabe.append([])
    pfad = 'Vorbereitung/Daten/Auswertung/modergebnis-' + modell + '.csv'
    try:
        with open(pfad, mode="r") as csvfile:
            spamreader = csv.reader(csvfile)
            # Ergebnis für ein Modell zusammensetzen...
            erg = []
            for row in spamreader:
                if row[0] != "ID":
                    if row[0] == "":
                        if erg != []:
                            ergebnisseeingabe[i].append(erg)
                        erg = []
                        x = 1
                    else:
                        erg.append({"ID": row[0], "Absatz": row[1], "Rang": x})
                        x +=1
            # ...und speichern
            if erg != []:
                ergebnisseeingabe[i].append(erg)
    except:
        print("Es gab ein Problem beim einlesen der Datei: " + pfad)
        exit()


## Bewertung
# Initialisierung
gmrrs = []
geinzel = []
mrrs = []
einzel = []
maximum = 99999999999999999

# Auswertung durchführen
for j, moderg in enumerate(ergebnisseeingabe):
    # Modell untersuchen
    geinzel.append([])
    einzel.append([])
    zähler = 0
    zählerg = 0
    for i, qmoderg in enumerate(moderg):
        # Frageergebnisse untersuchen
        zählernenner = maximum
        zählernennerg = maximum
        for e in qmoderg:
            # Bewertung suchen
            for er in ergebnisse[i]:
                if e["ID"] == er["ID"]:
                    b = int(er["Bewertung"])
                    r = int(e["Rang"])
                    # gegebenenfalls Zählernenner neu setzen
                    if b != 0:
                        zählernennerg = min(zählernennerg, b*b*r)
                        if b == 1:
                            zählernenner = min(zählernenner, b*b*r)
                    break
        # Fragebewertungen berechnen und speichern
        zähler += 1/zählernenner
        zählerg += 1/zählernennerg
        einzel[j].append(1/zählernenner)
        geinzel[j].append(1/zählernennerg)
    # MRRs speichern
    mrrg = zählerg/len(moderg)
    gmrrs.append(mrrg)
    mrr = zähler/len(moderg)
    mrrs.append(mrr)

# Auswertung abspeichern
for i, modell in enumerate(modelle):
    # Datei öffnen
    pfad = 'Vorbereitung/Daten/Auswertung/Auswertung-' + modell + '.csv'
    with open(pfad, 'w', newline='') as csvfile:
        fieldnames = ['MRR', 'gMRR', "Frage"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Inhalte speichern
        writer.writeheader()
        for j, eingabe in enumerate(eingaben):
            row = {"MRR": einzel[i][j], 'gMRR': geinzel[i][j], "Frage": eingabe}
            writer.writerow(e)
        row = {"MRR": mrrs[i], 'gMRR': gmrrs[i]}
        writer.writerow(e)