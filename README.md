# In Medias Res (privat)
Source Code für das das Masterarbeitsprojekt einer semantischen Suche für das Gesamtwerk von Immanuel Kant.

Enthalten sind:

Django
: Dajngo Projekt

Vorbereitung
: Dateien zur Modellerstellung und Datenverarbeitung

Trivia
: Sonstige Informationen

## Djangoprojekt

Vollständiges Djangoprojekt mit allen Daten und Modellen, das lauffähig ist. Bereit zur Veröffentlichung auf der Webseite. 
- Es gibt ein rudimentäres CSS-Stylesheet.
- Alle haben eine Überschrift und eine "Navigation". 

- Es gibt eine Datenbank:
    - Modell Suchbegriff mit
        - suchbegriff_text (String mit max. 200 Zeichen): Suchtext für einzelne Suche
        - anzahl (Integer mit Defaultwert 0): Anzahl der Suchaufrufe dieses Suchtextes
        - absatz (String mit max. 7 Zeichen): Absatz, in dem bestes Ergebnis zu finden ist

- Folgende Seiten sind implementiert:
    - Startseite (Index)
    - Dankseite
    - Suchseite
    - Ergebnisseite

### Startseite

Startseite mit Liste der häufigst gesuchten Sucheingaben.

### Dankseite

Seite mit Dank für Open Source Projekte und dedizierte Erlaubnis der Nutzung, sowie Dank für Unterstützung.

### Suchseite

Suchformular zur Eingabe des Suchstrings (200 Zeichen):
- verlinkt auf Ergebnis bei guter Eingabe
- sonst wird wieder die Suchseite aufgerufen
- !CSRF-Token wurde ausgeschaltet, da es nicht funktioniert ist und keine Gefahr davon ausgeht

### Ergebnisseite

Seite zum aufzeigen der Ergebnisse:
- Der Zielabsatz:
    - wird berechnet falls nötig
    - wird gekennzeichnet, 
    - wird als Anker gesetzt (Sprungpunkt zum Öffnen der Seite)
- Zusatzinformationen zum Seitenbeginn:
    - Sucheingabe als Überschrift
    - Angabe des Zielbandes (bisher hardcodiert auf 1)

## Dateien zur Modellerstellung und Datenverarbeitung

Dateien mit Daten und Skripten zum Training und Vorbereiten der Daten.

Daten
: Daten die nötig sind für die Suche.
: Kantkorpus wird vorerst mittels .gitignore nicht geteilt

Modelle
: NLP-Modelle

Skripte
: Skripte zur Vor- und Verarbeitung der Daten


### Daten

#### Kantkorpus

Vorerst nicht geteilt.

#### Vektoren

Vektoren getrennt nach Modellen für alle Bände. Erstellt durch Vektoren-Test.py

### Modelle

Es wurden folgende Modelle lokal installiert:
- deepset/gelectra-large-germanquad
- HuggingFace/distilbert-base-german-cased
- svalabs/bi-electra-ms-marco-german-uncased

### Skripte

Textprozess.py
: Vorbereitung des Korpus für die Ausgabe.

Training.py
: Training der Modelle mithilfe des Kantkorpus.

Vektoren-Test.py
: Test der Modelle und Erstellung der Vektoren zu dem in Textprozess vorbereiteten Korpus.

## Trivia

### .gitignore

Kantkorpus, Datenbankmigrationen und Modelle (wegen der Größe) werden nicht übertragen.