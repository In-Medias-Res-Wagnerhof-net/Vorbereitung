# Vorbereitung
Source Code für das das Masterarbeitsprojekt einer semantischen Suche für das Gesamtwerk von Immanuel Kant. Das Projekt basiert auf der [online Ausgabe des Gesamtwerk von Immanuel Kant](http://kant.korpora.org). Vielen Dank für die Bereitstellung der Daten!

Die Webseite mit der implementierten Suche ist unter folgendem Link zu finden:
[Link](http://www.in-medias-res.wagnerhof.net) (Momentan leider offline)
[temporärer Link](https://in-medias-res.honig-wagner.eu)

---

Enthalten sind:

- **[Inhalte des Repositoriums](#-aufbau-des-repositoriums)**: Dateien zur Modellerstellung und Datenverarbeitung
- **[HowTo](#-howto)**: Erklärung, wie das Repositorium genutzt werden kann und wie die unten genannten Ergebnisse erzielt wurden
- **[Ergebnisse](#-ergebnisse)**: Ergebnisse, wie gut/schlecht die Modelle abschneiden
- **[Trivia](#-trivia)**: Sonstige Informationen


---

## Aufbau des Repositoriums

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

- ***Textprozess_Kant.py***: Vorbereitung des Kantkorpus.
- ***Textprozess_functions.py***: Funktionen, die für die Vorbereitung benötigt werden.
- ***Training.py***: Training der Modelle mithilfe des Kantkorpus.
- ***Vektoren-Test.py***: Test der Modelle und Erstellung der Vektoren zu dem in Textprozess vorbereiteten Korpus.


---

## HowTo

### Einführung

Dieses Repositorium stellt alle Handwerkszeuge für die Aufbereitung des Korpus, das Training der Modelle und auch ein kleines Programm zur Durchführung einer Suche in dem Korpus dar. Es wird kurz auf die Einrichtung der Programmierumgebung eingegangen und enthält eine niederschwellige Schritt-für-Schritt-Anleitung, was jeweils gemacht wird (mit Hinweisen, wie der Code zur Anwendung an eigene Daten angepasst werden sollte). Eine allgemeine Einführung in das Projekt gibt es bei der überspannenden [Organisation](https://github.com/In-Medias-Res-Wagnerhof-net), oder auch auf der Webseite.

Grundsätzlich wurde versucht die Implementierung der Suche möglicht so zu gestalten, dass zumindest einzelne Funktionen oder vielleicht sogar ganze Programmteile auch für andere Projekte nutzbar sind. Jedoch ist jeder Korpus anders, sodass vor allem die Aufbereitung dessen nicht verallgemeinbar ist. Umso wichtiger ist die Dokumentation, in welcher Form die Daten vorliegen müssen um mit den restlichen Funktionen zusammen arbeiten zu können. So soll es möglich sein bereits aufbereitete Modelle zum Beispiel einfach zu benutzen um die Modelle zu trainieren, oder mit den eigenen trainierten Modellen oder auch Modellen anderer Institutionen darin zu suchen. Das eigene Modell mit den hier genutzten Daten zu trainieren ist leider momentan nicht möglich, wenden Sie sich dazu gerne an die [Herausgeber des online-Kantkorpus](http://kant.korpora.org).

Je nach Vorhaben kann direkt zu den entsprechenden Kapiteln gesprungen werden:
- **[Vorbereitung der Daten](#-vorbereitung-der-daten)**: In dieser Sektion wird die hier durchgeführte Bereinigung der Daten und die Aufbereitung der drei notwendigen Formen der Daten aufgezeigt.
- **[Training der Modelle](#-training-der-modelle)**: Hier wird das (weitere) Training der Modelle implementiert.
- **[Implementierung der Suche](#-implementierung-der-suche)**: Hier ist der Quellcode um lokal eine Suche zu implementieren sowie die zugehörige Erklärung.

### Vorbereitung der Daten

Für die Suche, wie sie hier umgesetzt wurde, sind drei verschiedene Versionen der Datei(en) nötig:

- **Datei(en) für das Training**: Der Korpus wird stark bereinigt und von allen formatierenden und zusätzlichen Informationen bereinigt.
- **Datei(en) für die Durchführung der Suche**: Der Korpus wird stark bereinigt und in Absätze mit einmaligen IDs unterteilt.
- **Datei(en) für die Suchausgabe**: Die Bereinigung fällt möglichst gering aus und die Absätze werden mit IDs ausgestattet, die zu den IDs der Dateien für die Durchführung der Suche passen.

Die Dateien lagen dazu im [TEI](https://tei-c.org)-Format vor und wurden für das Training und die Suche noch zusätzlich mittels [CAB-Normalisierung](https://www.deutschestextarchiv.de/cab/) aufbereitet -also die historische Schreibweise durch eine moderne ersetzt- da es sich bei dem Korpus um einen historischen Text handelt. Darum hatten sie vorerst zusätzliche Tags, die entfernt werden müssen. Die Vorgehensweise um diese Daten vorzubereiten unterteilt sich in verschiedene Schritte und wird mittels der Skripte *Textprozess_Kant.py* und *Textprozess_functions.py* umgesetzt:

<details>
<summary>Schritt 1: Anpassen der originalen und normalisierten Dateien</summary>

Um die Aufbereitung möglichst simpel zu gestalten, werden alle unnötigen Zusätze wie Fußnoten, Marginalia, Appendix, Seiten- und Zeilenumbrüche entfernt. Außerdem werden bereits die Überschriften in h-tags gewandelt und doppelte Leerzeichen entfernt. Dies geschieht mittels der *anpassen()*-Funktion. In den normalisierten Dateien werden zusätzlich die Abkürzungen aufgelöst (mithilfe von *abkürzungen_auflösen()*) und die zusätzlichen w- und s-tags so entfernt, dass die neuen Begriffe stehen bleiben. 

</details>

<details>
<summary>Schritt 2: ID-Setzung innerhalb der originalen und normalisierten Dateien</summary>

Nachdem die Dateien in Schritt 1 vorbereitet wurden, werden die IDs gesetzt mit *strukturiereDIV()*. Da die Absätze bereits vorgefiltert werden, ist hier zwingend darauf zu achten, dass ein Absatz in der originalen Datei die gleiche ID hat wie der gleiche Absatz in dem normalisierten Text, da sonst die Zuweisung der Ergebnisse auf die Ausgabedatei am Ende nicht korrekt erfolgen kann und nicht nur falsche Ergebnisse auftreten, sondern im schlimmsten Fall auch das Programm abbrechen kann. 

</details>

<details>
<summary>Schritt 3: Aufbereiten der normalisierten Dateien unterteilt in Absätze</summary>

Mithilfe der in Schritt 2 erstellten Texte wird nun mittels *erstelle_plaintext()* und der Hilfsfunktion *plain()* ein reiner Text erstellt, bei dem die Mithilfe von Zeilenumbrüchen Absätze getrennt werden. Dabei werden drei Dateien erzeugt: Eine Datei mit allen Absätzen, eine mit allen außer dem zehnten und eine mit nur allen zehnten Absätzen. Die Bereingigung verringert dabei den fremdsprachlichen Anteil, Nummern und Daten, überflüßige Leerzeichen, Satzzeichen und Klammern und entfernt alle verbleibenden Tags.

</details>

<details>
<summary>Schritt 4: Aufbereiten der normalisierten Dateien unterteilt in Sätze</summary>

Grundsätzlich wird hier wie in Schritt 3 verfahren, jedoch werden in den normalisierten Dateien zu Beginn nicht die Satzunterteilungen entfernt, sodass diese dann als Teiler genutzt werden können und aus den resultierenden Sätzen drei Dateien nach dem oben genannten Schema erstellt werden.

</details>


### Training der Modelle

### Implementierung der Suche


---

## Ergebnisse


---

## Trivia

<details>
<summary>Dependencies</summary>

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

</details>


<details>
<summary>.gitignore</summary>

Kantkorpus und Modelle (wegen der Größe) werden (vorerst) nicht übertragen.

</details>


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
- Webseite richtig verlinken (überall)
- Seitenumbrüche einbeziehen und Zitationsvorschlag erstellen