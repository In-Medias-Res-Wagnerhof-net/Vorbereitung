# Vorbereitung
Source Code für das das Masterarbeitsprojekt einer semantischen Suche für das Gesamtwerk von Immanuel Kant.

[Link](http://www.in-medias-res.wagnerhof.net)

[temporärer Link](http://138.201.94.48/plesk-site-preview/in-medias-res.wagnerhof.net/https/172.31.1.100)

---

Enthalten sind:

- **Vorbereitung**: Dateien zur Modellerstellung und Datenverarbeitung
- **Trivia**: Sonstige Informationen

---

## Dateien zur Modellerstellung und Datenverarbeitung

Dateien mit Daten und Skripten zum Training und Vorbereiten der Daten.

- **Daten**: Daten die nötig sind für die Suche. ! Kantkorpus wird vorerst mittels .gitignore nicht geteilt
- **Modelle**: NLP-Modelle
- **Skripte**: Skripte zur Vor- und Verarbeitung der Daten


### Daten

#### Kantkorpus

Vorerst nicht geteilt.

#### Vektoren

Vektoren getrennt nach Modellen für alle Bände. Erstellt durch Vektoren-Test.py

### Modelle

Es wurden folgende Modelle lokal installiert:
- *deepset/gelectra-large-germanquad*
- *HuggingFace/distilbert-base-german-cased*
- *svalabs/bi-electra-ms-marco-german-uncased*

### Skripte

- **Textprozess.py**: Vorbereitung des Korpus für die Ausgabe.
- **Training.py**: Training der Modelle mithilfe des Kantkorpus.
- **Vektoren-Test.py**: Test der Modelle und Erstellung der Vektoren zu dem in Textprozess vorbereiteten Korpus.

---

## Trivia

### .gitignore

Kantkorpus und Modelle (wegen der Größe) werden nicht übertragen.
