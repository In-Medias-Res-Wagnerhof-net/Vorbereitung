# Vorbereitung
Source Code für das das Masterarbeitsprojekt einer semantischen Suche für das Gesamtwerk von Immanuel Kant. Das Projekt basiert auf der [online Ausgabe des Gesamtwerks von Immanuel Kant](http://kant.korpora.org). Vielen Dank für die Bereitstellung der Daten!

Die Webseite mit der implementierten Suche ist unter folgendem Link zu finden:
[Link](http://www.in-medias-res.wagnerhof.net) (Momentan leider offline)
[temporärer Link](https://in-medias-res.honig-wagner.eu)

---

Enthalten sind:

- **[Inhalte des Repositoriums](#aufbau-des-repositoriums)**: Dateien zur Modellerstellung und Datenverarbeitung
- **[HowTo](#howto)**: Erklärung, wie das Repositorium genutzt werden kann und wie die unten genannten Ergebnisse erzielt wurden
- **[Ergebnisse](#ergebnisse)**: Ergebnisse, wie gut/schlecht die Modelle abschneiden
- **[Trivia](#trivia)**: Sonstige Informationen


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
- ***Trainingspipeline.py***: Pipeline, die das gesamte Training managed.
- ***Training_functions.py***: Funktionen, die für das Training benötigt werden.
- ***Vektoren-Test.py***: Test der Modelle und Erstellung der Vektoren zu dem in Textprozess vorbereiteten Korpus.


---

## HowTo

Dieses HowTo richtet sich vor allem an Neulinge der Natürlichen Sprachverarbeitung. Für Fortgeschrittenere ist wohl eher die [Auswertung](#ergebnisse) der Ergebnisse relevant, bzw. wie das Verfahren Implementiert wurde. Auf Feinheiten der Implementierung kann aufgrund des Platzes nicht in vollem Umfang eingegangen werden. Dazu gibt es auf der Webseite weitere Informationen.


### Einführung

Dieses Repositorium stellt alle Handwerkszeuge für die Aufbereitung des Korpus, das Training der Modelle und auch ein kleines Programm zur Durchführung einer Suche in dem Korpus dar. Es wird kurz auf die Einrichtung der Programmierumgebung eingegangen und enthält eine niederschwellige Schritt-für-Schritt-Anleitung, was jeweils gemacht wird (mit Hinweisen, wie der Code zur Anwendung an eigene Daten angepasst werden sollte). Eine allgemeine Einführung in das Projekt gibt es bei der überspannenden [Organisation](https://github.com/In-Medias-Res-Wagnerhof-net), oder auch auf der Webseite.

Grundsätzlich wurde versucht die Implementierung der Suche möglicht so zu gestalten, dass zumindest einzelne Funktionen oder vielleicht sogar ganze Programmteile auch für andere Projekte nutzbar sind. Jedoch ist jeder Korpus anders, sodass vor allem die Aufbereitung dessen nicht verallgemeinbar ist. Umso wichtiger ist die Dokumentation, in welcher Form die Daten vorliegen müssen um mit den restlichen Funktionen zusammen arbeiten zu können. So soll es möglich sein bereits aufbereitete Modelle zum Beispiel einfach zu benutzen um die Modelle zu trainieren, oder mit den eigenen trainierten Modellen oder auch Modellen anderer Institutionen darin zu suchen. Das eigene Modell mit den hier genutzten Daten zu trainieren ist leider momentan nicht möglich, wenden Sie sich dazu gerne an die [Herausgeber des online-Kantkorpus](http://kant.korpora.org).

Je nach Vorhaben kann direkt zu den entsprechenden Kapiteln gesprungen werden:
- **[Vorbereitung der Daten](#vorbereitung-der-daten)**: In dieser Sektion wird die hier durchgeführte Bereinigung der Daten und die Aufbereitung der drei notwendigen Formen der Daten aufgezeigt.
- **[Training der Modelle](#training-der-modelle)**: Hier wird das (weitere) Training der Modelle implementiert.
- **[Implementierung der Suche](#implementierung-der-suche)**: Hier ist der Quellcode um lokal eine Suche zu implementieren sowie die zugehörige Erklärung.
- **[Auswertung der Modelle](#auswertung)**: Zuletzt gibt es noch eine implementierte Auswertung unter anderem mithilfe des [Mean Reciprocal Rank](https://en.wikipedia.org/wiki/Mean_reciprocal_rank).

### Programmierumgebung einrichten


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

In die Trainingspipeline sind zwei Arten des Trainings verbaut: Einmal das Training des grundlegenden Modells mittels Masked Language modeling (entsprechend dem offiziellen Paper von [Bert](https://arxiv.org/pdf/1810.04805)) mit anschließendem Feintuning und zum anderen das Training mittels [TSDAE](https://arxiv.org/abs/2104.06979) und anschließendem Feintuning. Mit ein paar Anpassungen ist es auch möglich dies zu koppeln und auf das grundlegende Training mit TSDAE aufzubauen und danach feinzutunen. Auch eine Anpassung des Vokabulars ist bereits eingebaut, wird in Trainingspipeline.py allerdings nicht genutzt, da mit dem geringen Umfang des hier genutzten Koprus zu befürchten steht, dass die Gewichtungen der neuen Einträge nicht ausreichend trainiert werden.

Wie bei der Vorbereitung der Daten ist auch das Programm in Funktionen und Anwendung des Trainings geteilt. Das Training geschieht mittels HuggingFace Vorlagen und Benutzung von SentenceTransformer. Das Modell sollte eine dafür entsprechende Form haben. Für TSDAE sind die Vorgaben noch strikter (Distilbert und ConvBERT bspw. funktionieren nicht). Für das Feintuning wird ein deutsches Datenset von deepset, [GermanDPR](https://huggingface.co/datasets/deepset/germandpr), verwendet und nicht extra eigene Information Retrieval Daten aus dem Kantkorpus extrahiert. 

<details>
<summary>Schritt 0: Grundsätzliches</summary>

In *Training_functions.py* werden vier Funktionen bereitgestellt. Mithilfe von *lade_Modell()* kann das Modell enstprechend den Vorgaben eingelesen werden. Es deckt auch die neue Initialisierung eines SentenceTransformermodells ab. Die Funktion deckt für den Moment nur die Modelle *[svalabs/bi-electra-ms-marco-german-uncased](https://huggingface.co/svalabs/bi-electra-ms-marco-german-uncased)*, *[deepset/gelectra-large-germanquad](https://huggingface.co/deepset/gelectra-large-germanquad)*, *[dbmdz/distilbert-base-german-europeana-cased](https://huggingface.co/dbmdz/distilbert-base-german-europeana-cased)* und *[dbmdz/convbert-base-german-europeana-cased](https://huggingface.co/dbmdz/convbert-base-german-europeana-cased)* ab (Vielen Dank für die Bereitstellung dieser vortrainierten Modelle!). Die anderen drei Funktionen sind für das Laden der Daten. Auch wenn diese Funktionen in Sachen Vorbereitung einiges Abnehmen, müssen für das Training noch einige weitere Angaben gemacht werden. Dies ist allerdings Dank der entsprechenden Plattformen größtenteils vergleichsweise einfach und ist, vor allem für allgemeine Anwendungsfälle, recht gut dokumentiert.

</details>

<details>
<summary>Schritt 1.1: Training des grundlegenden Modells</summary>

Das grundlegende Transformer Modell wird hier mittels MaskedLM trainiert, entsprechend den [Handlungsanweisungen bei HuggingFace](https://huggingface.co/docs/transformers/main/tasks/masked_language_modeling) für den HuggingFace [Trainer](https://huggingface.co/docs/transformers/v4.40.2/en/main_classes/trainer). Als Datengrundlage werden zwei Textdateien benötigt, in denen die Textabschnitte mit Zeilenumbruch getrennt vorliegen und die bereits in Trainings- (Vorsilbe "train_") und Evaluierungsdate (Vorsilbe "eval_") unterteilt sind. Die Daten sollten aufbereitet sein, aber noch nicht tokenisiert. Mittels *lese_dataset()* werden die Daten dann in die Form eines [Datensets](https://huggingface.co/docs/datasets) gebracht. Für Testzwecke ist es auch möglich nur einen kleinen Auszug zu erhalten. Damit kann dann die eigene Implementierung ausführlich getestet werden, damit bei dem vollen Training alles optimal eingestellt ist und funktioniert. Wichtig ist jedoch immer, dass cased Modelle die Groß-/Kleinschreibung beachten, uncased benötigen kleinen Text. Es müssen dann nur noch die jeweils passenden Angaben für den eigenen Korpus und die eigene Hardware gemacht werden (Hierauf wird etwas ausführlicher eingegangen, weil diese Informationen teilweise etwas verstreut auf HuggingFace liegen):

- **Trainingsparameter und Evaluierung**:
    - Lernrate *learning_rate*: Angabe, wie schnell das Modell lernen darf. Es wird die niedrigste Fehlerquote gesucht. Es gilt: Je höher die Lernrate, desto schneller kann ein Modell trainiert werden, aber umso verlustreicher im Bezug auf das vorher trainierte ist das Training auch. In dem ursprünglichen Paper werden Lernraten zwischen 2e-5 bis 5e-5 angegeben (Für einen groben Überblick zum Lernen von Neuronalen Netzen: [Wie lernen neuronale Netze?](https://www.statworx.com/content-hub/blog/wie-lernen-neuronale-netze/)).
    - Epochen *num_train_epochs*: Anzahl der Durchgänge, die einen Datensatz behandeln. Viele Durchgänge verbrauchen viel Rechenkapazität und können Overfitting verursachen, allerdings wird eine gewisse Anzahl an Durchgängen gebraucht, damit die neuen Daten in dem Modell Beachtung finden. In dem Paper werden 2-3 Epochen gerechnet (Eine Möglichkeit die optimale Epochenanzahl zu berechnen ist die K-fold-Methode. Beschrieben wird sie bspw. bei [Medium](https://medium.com/geekculture/finding-optimal-epochs-using-k-fold-for-transformer-models-615a002195cb))
    - Komplexitätsbestrafung *weight_decay*: Mit diesem Wert kann weiterhin das Overfitting erschwert werden. Es wird die Komplexität eines Modells bestraft, sodass das Modell mehr generalisiert (Als erste Einführung [This thing called Weight Decay](https://towardsdatascience.com/this-thing-called-weight-decay-a7cd4bcfccab))
    - Evaluationsstrategie *evaluation_strategy*: Wann/Wie oft geprüft werden soll, ob das Training erfolgsversprechend ist. Mit der Angabe "epoch" wird nach jeder Epoche evaluiert, bei "steps" alle x Schritte. Wie groß x ist wird mit *eval_steps* gesetzt. Die Evaluierung benötigt einige Rechenkapazitäten, sodass sie nicht zu häufig gemacht werden kann, sollte allerdings auch nicht zu selten durchgeführt werden, weil es dann sein kann, dass sich das Modell in eine schlechte Richtung bewegt hat und man den großen Zwischenschritt umsonst berechnet hat.
- **Hardwareanpassungen**:
    - Batch-größe *per_device_train_batch_size*: Die Größe eines Schrittes beim Trainieren. Bei größeren Batches werden mehr Daten gleichzeitig geladen. Ist ein Batch zu klein, wird der Prozessor/die Grafikkarte nicht ausgelastet, weil zu kleine Schritte gemacht werden, ist er zu groß kann das das Training auch verlangsamen, weil die Daten nicht schnell genug herbeigeschafft werden können. Außerdem benötigen größere Batches auch mehr Arbeitsspeicher, der vorhanden sein sollte. Es ist gut eine passende Batch-Größe für das aktuelle Verfahren und die genutzten Daten zu ermitteln, bevor das volle Training gestartet wird.
    - Weitere Möglichkeiten wie *gradient_accumulation_steps*, *per_device_train_batch_size* oder *use_cpu* und viele weitere können individuell eingestellt werden, benötigen aber etwas Vorwissen und Willen sich mit der eigenen Hardware, wie auch dem eigenen Programm und den eigenen Daten auseinanderzusetzen. 
- **Rückgabe und Speicherstrategie**: 
    - Rückgabepfad *output_dir*: Hier wird das Modell, aber auch alles weitere gespeichert, sodass daraus jederzeit ein funktionierendes Modell geladen werden kann (auch der Tokenizer sollte hier gespeichert werden).
    - Speicherhäufigkeit *save_strategy*: Die Angabe hier muss zur *evaluation_strategy* passen. Nach jeder Evaluation wird das neue Modell gespeichert.
    - Speicherlimit *save_total_limit*: Ohne Limit würden alle Zwischenschritte gespeichert, was extrem viel Speicherplatz verbrauchen würde. Ist der Speicher voll, bricht der Trainingsvorgang ab. Daher ist es sinnvoll nur das Minimum zu speichern. Allerdings kann man bei mehreren Speicherungen auf eine Version eines früheren Modells zurückgreifen, wenn man vermutet, dass man zu viele Epochen treiniert hat und es z.B. zu einem Overfitting gekommen ist. Zu Beachten ist außerdem, dass immer wenigstens zwei Versionen gespeichert werden müssen, weil diese bei der Evaluierung gegeneinander abgeglichen werden. Es wird die Anzahl der zu speichernden Zwischenschritte gespeichert.
    - Bestes Modell Heraussuchen *load_best_model_at_end*: Hier wird die Angabe gemacht, ob zuletzt das beste oder das letzte Modell im Trainer geladen ist. Diese Angabe verändert, welches Modell am Ende mittels *.save_model()* gespeichert wird. 
- **Alle Angaben** und was sie jeweils bewirken sind in der Doku zu den [TrainingArguments](https://huggingface.co/docs/transformers/main/en/main_classes/trainer#transformers.TrainingArguments) bei HuggingFace zu finden.

</details>

<details>
<summary>Schritt 1.2: Feintuning des SentenceTransformerModells nach dem Training des grundlegenden Modells</summary>

Nachdem wahlweise ein neues SentenceTransformerModell als Aufsatz für das zugrundeliegende BertModell erstellt wurde oder ein schon existierendes geladen wurde, wird dieses Modell nun mithilfe von Textgruppen auf den konkreten Anwendungsfall hin trainiert. Das heißt es wird die Ähnlichkeit von Textstellen zu einer Frage berechnet. In dem Datenset [GermanDPR](https://huggingface.co/datasets/deepset/germandpr) sind Frage-Antwortkombinationen zu finden. Dabei gibt es zu jeder Frage immer mindestens eine gut passende (Positive) Antwort und eine nicht passende (negative) Antwort. Bei HuggingFace gibt es auch dazu eine [Einführung](https://huggingface.co/blog/how-to-train-sentence-transformers). Mithilfe von *lese_InputExample()* werden die Daten in das richtige Format gebracht, auch für die Evaluierung (in dem Datenset ist sowohl ein Trainings- als auch ein Testset enthalten).

Entsprechend den Daten wird der loss mittels TripletLoss und die Evaluation mittels TripletEvaluator berechnet. Dabei wird der Abstand zwischen der Frage und der positiven Antword minimiert und umgekehrt der Abstand zwischen Frage und negativer Antwort maximiert. In dem Datenset handelt es sich tatsächlich immer um Fragen als Anker, sodass das Modell dahingehend trainiert wird und besonders gut mit Fragen als Eingaben funktioniert. Hinzu kommen auch hier noch spezifische Angaben:

- **Trainingsparameter und Evaluierung**:
    - Epochen *epochs*: Anzahl der Durchgänge, die einen Datensatz behandeln. Viele Durchgänge verbrauchen viel Rechenkapazität und können Overfitting verursachen, allerdings wird eine gewisse Anzahl an Durchgängen gebraucht, damit die neuen Daten in dem Modell Beachtung finden. Standardmäßig sind 10 gesetzt, was doch recht viel ist.
    - Komplexitätsbestrafung *weight_decay*: Mit diesem Wert kann weiterhin das Overfitting erschwert werden. Es wird die Komplexität eines Modells bestraft, sodass das Modell mehr generalisiert (Als erste Einführung: [This thing called Weight Decay](https://towardsdatascience.com/this-thing-called-weight-decay-a7cd4bcfccab))
    - Evaluationsschritte *evaluation_steps*: Wann/Wie oft geprüft werden soll, ob das Training erfolgsversprechend ist. Es gibt keine Angabe für epochenweise Evaluation, das muss selbst anhand der Schrittanzahl gesetzt werden. Die Evaluierung benötigt einige Rechenkapazitäten, sodass sie nicht zu häufig gemacht werden kann, sollte allerdings auch nicht zu selten durchgeführt werden, weil es dann sein kann, dass sich das Modell in eine schlechte Richtung bewegt hat und man den großen Zwischenschritt umsonst berechnet hat.
    - Aufwärmphase *warmup_steps*: Innerhalb dieser Phase wird die Lernrate drastisch erhöht, sodass ein schnelleres Lernen möglich ist. Dies ist sinnvoll, wenn der SentenceTransformer neu initilisiert wurde und daher zuvor noch randomisierte Gewichte enthält.
- **Hardwareanpassungen**:
    - Batch-größe *batch_size*: Innerhalb des Dataloaders kann eine Batchgröße eingestellt werden, also die Größe eines Schrittes beim Trainieren. Bei größeren Batches werden mehr Daten gleichzeitig geladen. Ist ein Batch zu klein, wird der Prozessor/die Grafikkarte nicht ausgelastet, weil zu kleine Schritte gemacht werden, ist er zu groß kann das das Training auch verlangsamen, weil die Daten nicht schnell genug herbeigeschafft werden können. Außerdem benötigen größere Batches auch mehr Arbeitsspeicher, der vorhanden sein sollte. Es ist gut eine passende Batch-Größe für das aktuelle Verfahren und die genutzten Daten zu ermitteln, bevor das volle Training gestartet wird.
    - Prozessor *device*: Bei dem Training mit der GPU kam es zu einem Datenleak, gerade bei zusätzlich wenig Arbeitsspeicher kann das zu einem Out of Memory (OOM)-Fehler. Bei der Berechnung auf der CPU war dies nicht der Fall. Je nach Computerausstattung ist es allerdings sehr viel zeitintensiver mit der CPU zu rechnen.
- **Rückgabe und Speicherstrategie**: 
    - Rückgabe- und Checkpointpfad *output_path* und *checkpoint_path*: trainierte Modelle und Zwischenspeicherpunkte können gesondert gespeichert werden.
    - Speicherhäufigkeit *checkpoint_save_steps*: Angabe, alle wie viel Schritte gespeichert wird.
    - Speicherlimit *checkpoint_save_total_limit*: Ohne Limit würden alle Zwischenschritte gespeichert, was extrem viel Speicherplatz verbrauchen würde. Ist der Speicher voll, bricht der Trainingsvorgang ab. Daher ist es sinnvoll nur das Minimum zu speichern. Allerdings kann man bei mehreren Speicherungen auf eine Version eines früheren Modells zurückgreifen, wenn man vermutet, dass man zu viele Epochen treiniert hat und es z.B. zu einem Overfitting gekommen ist. Zu Beachten ist außerdem, dass immer wenigstens zwei Versionen gespeichert werden müssen, weil diese bei der Evaluierung gegeneinander abgeglichen werden. Es wird die Anzahl der zu speichernden Zwischenschritte gespeichert.
    - Bestes Modell Speichern *save_best_model*: Hier wird die Angabe gemacht, ob zuletzt das beste gespeichert werden soll. 
- **Alle Angaben** und was sie jeweils bewirken sind in der Doku zu dem [SentenceTransformer](https://www.sbert.net/docs/training/overview.html) bei sbert zu finden.

</details>

<details>
<summary>Schritt 2.1: Vortrainieren des SentenceTransformers mittels TSDAE</summary>

Nachdem wahlweise ein neues SentenceTransformerModell als Aufsatz für das zugrundeliegende BertModell erstellt wurde oder ein schon existierendes geladen wurde, wird dieses Modell nun mithilfe von korrumpierten Sätzen aus dem Korpus vortrainiert. Der Computer muss mithilfe des Modells die Sätze wiederherstellen. Dazu müssen die Daten als Liste von Sätzen vorliegen. Das Einlesen aus einer Datei, in der sie mit Zeilenumbruch getrennt vorliegen wird mit der Funktion *lese_datalisten()* realisiert. Nun muss nur noch das [Skript von den Erfindern](https://www.sbert.net/examples/unsupervised_learning/TSDAE/README.html) umgesetzt werden. Bis auf den Rückgabe/Speicherangaben sowie der Batchgröße wurden die Angaben von dort übernommen.

</details>

<details>
<summary>Schritt 2.2: Feintuning des SentenceTransformerModells nach dem Vortrainieren mittels TSDAE</summary>

Nachdem das SentenceTransformerModell als Aufsatz für das zugrundeliegende BertModell erstellt und vortrainiert wurde, wird es nun mithilfe von Textgruppen auf den konkreten Anwendungsfall hin trainiert. Dies geschieht analog zu Schritt 1.2. Es wird die Ähnlichkeit von Textstellen zu einer Frage berechnet. In dem Datenset [GermanDPR](https://huggingface.co/datasets/deepset/germandpr) sind Frage-Antwortkombinationen zu finden. Dabei gibt es zu jeder Frage immer mindestens eine gut passende (Positive) Antwort und eine nicht passende (negative) Antwort. Bei HuggingFace gibt es auch dazu eine [Einführung](https://huggingface.co/blog/how-to-train-sentence-transformers). Mithilfe von *lese_InputExample()* werden die Daten in das richtige Format gebracht, auch für die Evaluierung (in dem Datenset ist sowohl ein Trainings- als auch ein Testset enthalten).

Entsprechend den Daten wird der loss mittels TripletLoss und die Evaluation mittels TripletEvaluator berechnet. Dabei wird der Abstand zwischen der Frage und der positiven Antword minimiert und umgekehrt der Abstand zwischen Frage und negativer Antwort maximiert. In dem Datenset handelt es sich tatsächlich immer um Fragen als Anker, sodass das Modell dahingehend trainiert wird und besonders gut mit Fragen als Eingaben funktioniert. Hinzu kommen auch hier noch spezifische Angaben:

- **Trainingsparameter und Evaluierung**:
    - Epochen *epochs*: Anzahl der Durchgänge, die einen Datensatz behandeln. Viele Durchgänge verbrauchen viel Rechenkapazität und können Overfitting verursachen, allerdings wird eine gewisse Anzahl an Durchgängen gebraucht, damit die neuen Daten in dem Modell Beachtung finden. Standardmäßig sind 10 gesetzt, was doch recht viel ist.
    - Komplexitätsbestrafung *weight_decay*: Mit diesem Wert kann weiterhin das Overfitting erschwert werden. Es wird die Komplexität eines Modells bestraft, sodass das Modell mehr generalisiert (Als erste Einführung: [This thing called Weight Decay](https://towardsdatascience.com/this-thing-called-weight-decay-a7cd4bcfccab))
    - Evaluationsschritte *evaluation_steps*: Wann/Wie oft geprüft werden soll, ob das Training erfolgsversprechend ist. Es gibt keine Angabe für epochenweise Evaluation, das muss selbst anhand der Schrittanzahl gesetzt werden. Die Evaluierung benötigt einige Rechenkapazitäten, sodass sie nicht zu häufig gemacht werden kann, sollte allerdings auch nicht zu selten durchgeführt werden, weil es dann sein kann, dass sich das Modell in eine schlechte Richtung bewegt hat und man den großen Zwischenschritt umsonst berechnet hat.
    - Aufwärmphase *warmup_steps*: Innerhalb dieser Phase wird die Lernrate drastisch erhöht, sodass ein schnelleres Lernen möglich ist. Dies ist sinnvoll, wenn der SentenceTransformer neu initilisiert wurde und daher zuvor noch randomisierte Gewichte enthält.
- **Hardwareanpassungen**:
    - Batch-größe *batch_size*: Innerhalb des Dataloaders kann eine Batchgröße eingestellt werden, also die Größe eines Schrittes beim Trainieren. Bei größeren Batches werden mehr Daten gleichzeitig geladen. Ist ein Batch zu klein, wird der Prozessor/die Grafikkarte nicht ausgelastet, weil zu kleine Schritte gemacht werden, ist er zu groß kann das das Training auch verlangsamen, weil die Daten nicht schnell genug herbeigeschafft werden können. Außerdem benötigen größere Batches auch mehr Arbeitsspeicher, der vorhanden sein sollte. Es ist gut eine passende Batch-Größe für das aktuelle Verfahren und die genutzten Daten zu ermitteln, bevor das volle Training gestartet wird.
    - Prozessor *device*: Bei dem Training mit der GPU kam es zu einem Datenleak, gerade bei zusätzlich wenig Arbeitsspeicher kann das zu einem Out of Memory (OOM)-Fehler. Bei der Berechnung auf der CPU war dies nicht der Fall. Je nach Computerausstattung ist es allerdings sehr viel zeitintensiver mit der CPU zu rechnen.
- **Rückgabe und Speicherstrategie**: 
    - Rückgabe- und Checkpointpfad *output_path* und *checkpoint_path*: trainierte Modelle und Zwischenspeicherpunkte können gesondert gespeichert werden.
    - Speicherhäufigkeit *checkpoint_save_steps*: Angabe, alle wie viel Schritte gespeichert wird.
    - Speicherlimit *checkpoint_save_total_limit*: Ohne Limit würden alle Zwischenschritte gespeichert, was extrem viel Speicherplatz verbrauchen würde. Ist der Speicher voll, bricht der Trainingsvorgang ab. Daher ist es sinnvoll nur das Minimum zu speichern. Allerdings kann man bei mehreren Speicherungen auf eine Version eines früheren Modells zurückgreifen, wenn man vermutet, dass man zu viele Epochen treiniert hat und es z.B. zu einem Overfitting gekommen ist. Zu Beachten ist außerdem, dass immer wenigstens zwei Versionen gespeichert werden müssen, weil diese bei der Evaluierung gegeneinander abgeglichen werden. Es wird die Anzahl der zu speichernden Zwischenschritte gespeichert.
    - Bestes Modell Speichern *save_best_model*: Hier wird die Angabe gemacht, ob zuletzt das beste gespeichert werden soll. 
- **Alle Angaben** und was sie jeweils bewirken sind in der Doku zu dem [SentenceTransformer](https://www.sbert.net/docs/training/overview.html) bei sbert zu finden.

</details>


### Implementierung der Suche

Um die Suche anzuwenden müssen mithilfe eines SentenceTransformermodells die Vektorabbildung sowohl der Zielabsätze, als auch der Eingabe berechnet werden um anschließend den/die Zielabsatz/sätze herauszusuchen, die die größte Übereinstimmung mit der Sucheingabe aufweisen. Dazu werden die Python-Dateien *Vektoren-Test.py* und *Anwendung_functions.py* herangezogen.

<details>
<summary>Schritt 1: Vorbereitung der Daten</summary>

Für die Suche sollten die zu durchsuchenden Absätze bereits in einer tei-Datei mit ausgezeichneten Ids vorliegen. Hier werden sogar zwei Versionen verwendet: zum einen die normalisierten Texte zum Berechnen mit dem Computer, zum anderen die originalen Texte, die für die Ausgabe verwendet werden. **Die IDs müssen genau übereinstimmen**, damit von dem normalisierten Absatz wieder auf die originale Textdatei geschlossen werden kann. 

Mittels *bereite_daten()* werden diese Dateien eingelesen und Listen erstellt:
- ID-Listen:
    - Liste der IDs, die im originalen Text vorkommen.
    - Liste der IDs, die im normalisierten Text vorkommen.
- Absatzlisten:
    - Listen der Absätze die im originalen Text vorkommen.
    - Listen der Absätze die im normalisierten Text vorkommen.
- ID-Anzahlliste, die angibt, wie viele Ids in einem Band (normalisiert) vorkommen.
Solange die Ids zweifelsfrei zugeordnet werden können, ist es in Ordnung, wenn für die normalisierten Listen weniger Absätze einbezogen werden. Es können hier also Absätze aussortiert werden. Absatz- und Id-Liste müssen aber immer übereinstimmen in ihrer Form und Reihenfolge.

</details>

<details>
<summary>Schritt 2: Berechnung der Vektoren</summary>

Liegen die Listen in entsprechender Form vor, kann mithilfe von *vektorenberechnen()* die Vektorberechnung angestoßen werden. Liegen die Vektoren bereits vor, müssen sie lediglich eingelesen werden, ansonsten werden sie berechnet und für eine zukünftige Verwendung abgespeichert. Die Berechnung wird mithilfe eines SentenceTransformermodells durchgeführt, das bedeutet, wenn dieses noch nicht trainiert wurde, können auch bei einem gut trainierten Transformermodell schlechte Ergebnisse resultieren.

</details>

<details>
<summary>Schritt 3: Die eigentliche Suche</summary>

Zuletzt werden die Listen und die Vektoren mit einer Eingabe in Verbindung gesetzt. Es wird also für die Eingabe ein Vektor berechnet und dieser mit den normalisierten Vektoren verglichen. Der/die beste/n Ergebnisse werden nun mittels *suche_absatz()* aus den originalen Daten herausgesucht. Dabei wird zuerst die Id des Absatzes in dem normalisierten Datensatz herausgesucht, dann diese in der Id-Liste der originalen Absätze gesucht und mithilfe der so gewonnenen Indizes der Absatz gefunden und ausgegeben. Sollte die Id des Ergebnisses nicht in der originalen Id-Liste enthalten sein, so wird das Ergebnis übersprungen.

</details>

---

## Auswertung

Für die Auswertung der Modelle gibt es zwei Verfahren: den [Mean Reciprocal Rank](https://en.wikipedia.org/wiki/Mean_reciprocal_rank) (MRR) und den des gewichteten MRR (gMRR). Bei zweiterem werden die Ergebnisse nicht nur in Treffer und nicht Treffer unterteilt, sondern eine weitere Bewertung der Ergebnisse durchgeführt, um so auch Abschnitte einzubeziehen, die zwar kein perfekter Treffer sind, aber dennoch relevante oder spannende Informationen beinhalten. Dies geschieht mittels *Auswertung.py* und *Auswertung_functions.py*. Für beide Auswertungen muss eine **manuelle Bewertung** durchgeführt werden.

Hier die Berechnungsformeln mit |A| als Anzahl der Antworten, r als Rang der Antwort und b als Bewertung:
$$\text{MRR} = \frac{ \sum_{i=1}^{|\text{A}|} \frac{1}{\text{r}_i} }{ |\text{A}| }$$
$$\text{MRR}_text{g} = \frac{ \sum_{i=1}^{|\text{A}|} \frac{1}{ \text{min}\left(\text{r}_i \cdot \text{b}_i^4\right) } }{ |\text{A}| }$$

<details>
<summary>Schritt 1: Ergebnisse erhalten und abspeichern</summary>

Zu Beginn müssen die Ergebnisse berechnet werden. Das geschieht analog zu der [Implementierung der Suche](#implementierung-der-suche) und falls die Vektoren dort bereits berechnet wurden können sie wiederverwendet werden. Ansonsten werden sie berechnet und an dem angegebenen Ort abgespeichert. Dafür wird auf Funktionen von *Anwendung_functions.py* zurückgegriffen. Die Ergebnisse werden anschließend in zwei Formen abgespeichert: Einerseits für jedes Modell als Ergebnisliste pro Frage. Diese Datei ist nur für die anschließende Auswertung relevant. Andererseits wird für jede Frage ein Ergebniskatalog erstellt, in dem eine Bewertung durchgeführt werden muss, damit eine Auswertung durchgeführt werden kann. In diesen Dateien werden die Ergebnisse von allen Modellen duplikatfrei und ohne Angabe der Modelle gesichert.

</details>

<details>
<summary>Schritt 2: Bewertung</summary>

Die Bewertung der einzelnen Ergebnisse ist händisch durchzuführen. Es bietet sich an für jede Frage-Antwortkombination eine Bewertung zwischen 0 und 10 durchzuführen. 0 steht dabei für kein Treffer (dieses Ergebnis wird nicht einbezogen in die Auswertung), eins für perfekter Treffer. Umso höher die Zahl weiterhin ist, desto schlechter ist das Ergebnis zu bewerten. Für den MRR werden nur Treffer der Wertung 1 herangezogen, während für den gMRR auch die weiteren Wertungen herangezogen werden. Die Tabelle sollte dann folgendermaßen aussehen:

| ID    | Absatz        | {Frage}       |
|-------|---------------|---------------|
|{ID1}  | {Absatztext1} | {Bewertung1}  |
|{ID2}  | {Absatztext2} | {Bewertung2}  |
|...    | ...           | ...           |

Die Bewertung muss also in die dritte Spalte hinter ID und Abschnitttext geschrieben werden (unter die Frage), damit das Programm die Auswertung durchführen kann. Die Formatierung muss erhalten bleiben (Delimiter muss ein Komma sein). Danach ist in der Konsole mit der Eingabe *j* zu bestätigen, dass die Bewertung erfolgt ist.

</details>

<details>
<summary>Schritt 3: Auswertung</summary>

Nachdem die Bewertung erfolgt ist, werden die Dateien eingelesen und in Zusammenhang gestellt. Entscheidend ist dabei die ID, sowie die Frage und die Position. Aus diesen drei Faktoren zieht das Programm die Bewertung und den Rang und Kann so für jede Frage einen Wert ermitteln, deren Mittelwert dann den MRR/gMRR darstellt. Alle Werte werden nun pro Modell in eine Tabelle geschrieben. Es werden auch die Werte pro Frage gespeichert, sodass eine Mittelwertberechnung von nur bestimmten Fragen vereinfacht wird (Hierzu müssen nur die Werte der Fragen aufaddiert und durch die Anzahl dieser Frage geteilt werden). MRR und gMRR befinden sich in der untersten Zeile.

</details>

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

Training:
- Trainingspipeline.py:
    - transformers
    - sentence_transformers
    - torch
    - math
    - nltk
    - Training_functions
- Training_functions.py:
    - transformers
    - sentence_transformers
    - datasets
    - spacy

Anwendung:
- Anwendung.py:
    - Anwendung_functions
- Anwendung_functions.py:
    - bs4
    - lxml
    - re
    - sentence_transformers
    - numpy
    - sklearn
    - Training_functions

Auswertung:
- Auswertung.py:
    - csv
    - Auswertung_functions
- Auswertung_functions.py:
    - sklearn
    - numpy
    - Textprozess_functions
    - Anwendung_functions

</details>


<details>
<summary>.gitignore</summary>

Kantkorpus und Modelle (wegen der Größe) werden (vorerst) nicht übertragen.

</details>


### TODO

- Webseite richtig verlinken (überall)
- Zitationsvorschlag erstellen
- requirements.txt 
