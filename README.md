# Vorbereitung
Source Code für das das Masterarbeitsprojekt einer semantischen Suche für das Gesamtwerk von Immanuel Kant.

Die vollständige Webseite ist hier zu finden:
[Link](http://www.in-medias-res.wagnerhof.net)
[temporärer Link](https://in-medias-res.honig-wagner.eu)

---

Enthalten sind:

- **HowTo**: Erklärung, wie Repositorium genutzt werden kann
- **Vorbereitung**: Dateien zur Modellerstellung und Datenverarbeitung
- **Ergebnisse**: Ergebnisse, wie gut/schlecht die Modelle abschneiden
- **Trivia**: Sonstige Informationen

---

## HowTo

### Einführung

Dieses Repositorium stellt alle Handwerkszeuge für die Aufbereitung des Korpus, das Training der Modelle und auch ein kleines Programm zur Durchführung einer Suche in dem Korpus dar. Es wird kurz auf die Einrichtung der Programmierumgebung eingegangen und enthält eine niederschwellige Schritt-für-Schritt-Anleitung, was jeweils gemacht wird (mit Hinweisen, wie der Code zur Anwendung an eigenen Daten angepasst werden sollte). Eine allgemeine Einführung in das Projekt gibt es bei der überspannenden [Organisation](https://github.com/In-Medias-Res-Wagnerhof-net), oder auch auf der Webseite.

### Vorbereitung der Daten

### Training der Modelle

### Implementierung der Suche

---

## Dateien zur Modellerstellung und Datenverarbeitung

Dateien mit Daten und Skripten zum Training und Vorbereiten der Daten.

- **Daten**: Daten die nötig sind für die Suche. ! Kantkorpus wird (vorerst) nicht geteilt
- **Modelle**: NLP-Modelle
- **Skripte**: Skripte zur Vor- und Verarbeitung der Daten


### Daten

#### Kantkorpus

Vorerst nicht geteilt.

#### Vektoren

Bereits berechnete Vektoren getrennt nach Modellen für alle Bände. Erstellt durch Vektoren-Test.py

### Modelle

Es wurden folgende Modelle lokal installiert:
- *[svalabs/bi-electra-ms-marco-german-uncased](https://huggingface.co/svalabs/bi-electra-ms-marco-german-uncased)*
- *[deepset/gelectra-large-germanquad](https://huggingface.co/deepset/gelectra-large-germanquad)*
- *[dbmdz/distilbert-base-german-europeana-cased](https://huggingface.co/dbmdz/distilbert-base-german-europeana-cased)*
- *[dbmdz/convbert-base-german-europeana-cased](https://huggingface.co/dbmdz/convbert-base-german-europeana-cased)*

### Skripte

- **Textprozess_Kant.py**: Vorbereitung des Kantkorpus.
- **Textprozess_functions.py**: Funktionen, die für die Vorbereitung benötigt werden.
- **Training.py**: Training der Modelle mithilfe des Kantkorpus.
- **Vektoren-Test.py**: Test der Modelle und Erstellung der Vektoren zu dem in Textprozess vorbereiteten Korpus.

---

## Trivia

### .gitignore

Kantkorpus und Modelle (wegen der Größe) werden (vorerst) nicht übertragen.

### Dependencies

Vorbereitung:
- Textprozess_Kant.py:
    - bs4
    - lxml
    - Textprozess_functions
- Textprozess_functions.py:
    - bs4
    - lxml
    - re

Training.py:
- Einlesen:
    - bs4
    - re
    - lxml
- Training
    - transformers
    - datasets
    - trl

Vektoren-Test.py
- Korpus:
    - bs4
    - re
    - lxml
- Modell:
    - sentence_transformers
    - numpy
    - sklearn

### TODO

#### Dringend

- Id korrekt verwenden und mit Vektoren kompatibilisieren

#### Wichtig

- Überschriftenmanagement (Bei der kompletten Suche?)
- Prozessieren des Historischen Wörterbuchs der Philosophie
- Dokumentation
- Ausgabe der ID in Vektoren-Test.py

#### Mittelfristig

- Veröffentlichung des Repositoriums