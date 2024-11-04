##############################################################################################################
##############################################################################################################
###
###     Teilauswertung der Modelle
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
from Auswertung_functions import *

import csv

##############################################################################################################
##
##      Programm
##
##############################################################################################################
# Initialisierung
modelle = ["bielectra", "convbert", "distilbert", "gelectra"]
zusätze = ["training", "training-fein", "training-fein-tsdae", "tsdae", "tsdae-fein"]
einzel = []
geinzel = []
mrrs = []
gmrrs = []

for modell in modelle.copy():
    for zusatz in zusätze:
        if (modell != "distilbert" and modell != "convbert") or not "tsdae" in zusatz:
            modelle.append(modell + "-" + zusatz)

pfadek = 'Vorbereitung/Daten/Auswertung/Auswertung-'
pfadak = 'Vorbereitung/Daten/Auswertung/Teilauswertung_mehrere-Worte'
eingaben = erhalte_eingaben(pfadak + ".txt")


# Ergebnisse pro Frage und Bewertung einlesen und berechnen
for i, mod in enumerate(modelle):
    # Initialisierungen
    einzel.append([])
    geinzel.append([])
    zähler = 0
    zählerg = 0
    pfade = pfadek + mod + '.csv'

    # Datei öffnen
    try:
        with open(pfade, mode="r") as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if row[0] != "MRR" and row[2] != "" and row[2] in eingaben:
                    # Einzelergebnisse laden
                    einzel[i].append(row[0])
                    geinzel[i].append(row[1])
                    # Mittelwertberechnung
                    zähler += float(row[0])
                    zählerg += float(row[1])
            mrrs.append(zähler/len(eingaben))
            gmrrs.append(zählerg/len(eingaben))
    except:
        print("Es gab ein Problem beim einlesen der Datei: " + pfade)
        exit()


# Auswertung abspeichern
for i, modell in enumerate(modelle):
    # Datei öffnen
    pfada = pfadak + "-" + modell + '.csv'
    with open(pfada, 'w', newline='') as csvfile:
        fieldnames = ['MRR', 'gMRR', "Frage"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Inhalte speichern
        writer.writeheader()
        for j, eingabe in enumerate(eingaben):
            row = {"MRR": einzel[i][j], 'gMRR': geinzel[i][j], "Frage": eingabe}
            writer.writerow(row)
        row = {"MRR": mrrs[i], 'gMRR': gmrrs[i], "Frage":"Gesamt"}
        writer.writerow(row)

