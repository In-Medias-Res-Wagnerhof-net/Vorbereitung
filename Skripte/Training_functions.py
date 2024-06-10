##############################################################################################################
##############################################################################################################
###
###     Für das Training relevante Funktionen
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
from transformers import AutoModelForMaskedLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, models, InputExample

from datasets import load_dataset
from spacy import blank


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################
'''
    Inhalt:
    1. Modelle laden
    2. Datenvorbereitung
'''

'''
    1. Modelle laden
'''
def lade_modell(mod:str, output:str = "training", typ:str = "maskedLM", pfad:str = "../In Medias Res/Vorbereitung/Modelle/", stexist:bool = False, device:str = None, name:bool = False):
    '''
        Modell laden
        Input: 
            mod:        String,     Name des Modells
            output:     String,     Name des Ausgabepfades
            typ:        String,     Name des zu ladenden Modells ("maskedLM" oder "SentenceTransformer")
            pfad:       String,     Pfad zu Ordner mit Modellen
            stexist:    Boolean,    Angabe, ob SentenceTranfsormermodell bereits existiert
            device:     String,     Deviceangabe für Sentencetransformer
            name:       Boolean,    Angabe, ob Modellname zurückgegeben werden soll
        Output:
            HuggingFaceModell
    '''
    ## Modellinformationen setzen
    if mod == "gelectra":
        model_name = pfad + "deepset/gelectra-large-germanquad"
        ausgabepfad = pfad + "deepset/gelectra-large-germanquad-" + output
    elif mod == "gelectra-training":
        model_name = pfad + "deepset/gelectra-large-germanquad-training"
        ausgabepfad = pfad + "deepset/gelectra-large-germanquad-training-" + output
    elif mod == "gelectra-training-fein":
        model_name = pfad + "deepset/gelectra-large-germanquad-training-fein"
        ausgabepfad = pfad + "deepset/gelectra-large-germanquad-training-fein-" + output
    elif mod == "gelectra-training-fein-tsdae":
        model_name = pfad + "deepset/gelectra-large-germanquad-training-fein-tsdae"
        ausgabepfad = pfad + "deepset/gelectra-large-germanquad-training-fein-tsdae-" + output
    elif mod == "gelectra-tsdae":
        model_name = pfad + "deepset/gelectra-large-germanquad-tsdae"
        ausgabepfad = pfad + "deepset/gelectra-large-germanquad-tsdae-" + output
    elif mod == "gelectra-tsdae-fein":
        model_name = pfad + "deepset/gelectra-large-germanquad-tsdae-fein"
        ausgabepfad = pfad + "deepset/gelectra-large-germanquad-tsdae-fein-" + output
    elif mod == "convbert":
        model_name = pfad + "dbmdz/convbert-base-german-europeana-cased"
        ausgabepfad = pfad + "dbmdz/convbert-base-german-europeana-cased-" + output
    elif mod == "convbert-training":
        model_name = pfad + "dbmdz/convbert-base-german-europeana-cased-training"
        ausgabepfad = pfad + "dbmdz/convbert-base-german-europeana-cased-training-" + output
    elif mod == "convbert-training-fein":
        model_name = pfad + "dbmdz/convbert-base-german-europeana-cased-training-fein"
        ausgabepfad = pfad + "dbmdz/convbert-base-german-europeana-cased-training-fein-" + output
    elif mod == "distilbert":
        model_name = pfad + "dbmdz/distilbert-base-german-europeana-cased"
        ausgabepfad = pfad + "dbmdz/distilbert-base-german-europeana-cased-" + output
    elif mod == "distilbert-training":
        model_name = pfad + "dbmdz/distilbert-base-german-europeana-cased-training"
        ausgabepfad = pfad + "dbmdz/distilbert-base-german-europeana-cased-training-" + output
    elif mod == "distilbert-training-fein":
        model_name = pfad + "dbmdz/distilbert-base-german-europeana-cased-training-fein"
        ausgabepfad = pfad + "dbmdz/distilbert-base-german-europeana-cased-trainin-feing-" + output
    elif mod == "bielectra":
        model_name = pfad + "svalabs/bi-electra-ms-marco-german-uncased"
        ausgabepfad = pfad + "svalabs/bi-electra-ms-marco-german-uncased-" + output
    elif mod == "bielectra-training":
        model_name = pfad + "svalabs/bi-electra-ms-marco-german-uncased-training"
        ausgabepfad = pfad + "svalabs/bi-electra-ms-marco-german-uncased-training-" + output
    elif mod == "bielectra-training-fein":
        model_name = pfad + "svalabs/bi-electra-ms-marco-german-uncased-training-fein"
        ausgabepfad = pfad + "svalabs/bi-electra-ms-marco-german-uncased-training-fein-" + output
    elif mod == "bielectra-training-fein-tsdae":
        model_name = pfad + "svalabs/bi-electra-ms-marco-german-uncased-training-fein-tsdae"
        ausgabepfad = pfad + "svalabs/bi-electra-ms-marco-german-uncased-training-fein-tsdae-" + output
    elif mod == "bielectra-tsdae":
        model_name = pfad + "svalabs/bi-electra-ms-marco-german-uncased-tsdae"
        ausgabepfad = pfad + "svalabs/bi-electra-ms-marco-german-uncased-tsdae-" + output
    elif mod == "bielectra-tsdae-fein":
        model_name = pfad + "svalabs/bi-electra-ms-marco-german-uncased-tsdae-fein"
        ausgabepfad = pfad + "svalabs/bi-electra-ms-marco-german-uncased-tsdae-fein-" + output
    else:
        print("Es gab ein Problem beim Laden des Modells...")
        exit()

    ## Modell laden
    # SentenceTransformer
    if typ == "SentenceTransformer":
        if "bielectra"in mod or stexist:
            if name:
                return SentenceTransformer(model_name, device=device), ausgabepfad, model_name
            else:
                return SentenceTransformer(model_name, device=device), ausgabepfad
        else:
            word_embedding_model = models.Transformer(model_name)
            pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
            if name:
                return SentenceTransformer(modules=[word_embedding_model, pooling_model], device=device), ausgabepfad, model_name
            else:
                return SentenceTransformer(modules=[word_embedding_model, pooling_model], device=device), ausgabepfad
    # MaskedLM
    else:
        modell = AutoModelForMaskedLM.from_pretrained(model_name)
        tokenisierer = AutoTokenizer.from_pretrained(model_name)
        if name:
            return modell, tokenisierer, ausgabepfad, model_name
        else:
            return modell, tokenisierer, ausgabepfad


'''
    2. Datenvorbereitung
'''
def lese_datalisten (mod:str = None, pfad:str = "../In Medias Res/Vorbereitung/Daten/Kant/training/", name:str = "satzweise", klein:bool = False, teilen:bool = False, vorschau:bool = False):
    '''
        Resultat als Liste aus Textprozess einlesen
        Input: 
            mod:        String,     Name des Modells                                    
                                    ! ignoriert klein, falls mod gesetzt
            pfad:       String,     Pfad zu Ordner
            name:       String,     "satzweise" oder "absatzweise"
            klein:      Boolean,    Angabe ob lower() version genommen werden soll
            teilen:     Boolean,    Angabe ob geteilte Daten genommen werden sollen
            vorschau:   Boolean,    Angabe ob Dataset verkürzt werden soll
        Output:
            teilen == False:
                list,   Liste mit Ausschnitten;
          oder:
            teilen == True:
                list,   Liste mit Trainingsausschnitten;
                list,   Liste mit Evaluierungsausschnitten;
    '''
    kleiner = ""
    if (mod == None and klein) or (mod != None and "bielectra" in mod):
        kleiner = "_lower"
    
    if teilen:
        # Versuche Daten einzulesen
        datei = open(pfad + "train_" + name + kleiner + ".txt")
        trainingsdatenliste = datei.read().split("\n")
        datei.close()
        datei = open(pfad + "eval_" + name + kleiner + ".txt")
        evaluierungsdatenliste = datei.read().split("\n")
        datei.close()

        if vorschau:
            return trainingsdatenliste[:10], evaluierungsdatenliste[:3]
        else:
            return trainingsdatenliste, evaluierungsdatenliste
    
    else:
        # Versuche Daten einzulesen
        datei = open(pfad + name + kleiner + ".txt")
        datenliste = datei.read().split("\n")
        datei.close()

        if vorschau:
            return datenliste[:10]
        else:
            return datenliste


def lese_dataset (tokenizer:AutoTokenizer = None, mod:str = None, pfad:str = "../In Medias Res/Vorbereitung/Daten/Kant/training/", name:str = "satzweise", klein:bool = False, teilen:bool = False, blöcke:int = 128, tokens:bool = False, vorschau:bool = False, tokenhäufigkeitsminimum:int = 100, tokenhäufigkeitsmaximum:int = 1930):
    '''
        Resultat als Liste aus Textprozess einlesen
        Input: 
            tokenizer                   Autotokenizer   Tokenizer, der für die Tokenisierung genutzt wird
            mod:                        String,         Name des Modells                                    
                                                        ! ignoriert klein, falls mod gesetzt
            pfad:                       String,         Pfad zu Ordner
            name:                       String,         "satzweise" oder "absatzweise"
            klein:                      Boolean,        Angabe ob lower() version genommen werden soll
            teilen:                     Boolean,        Angabe ob geteilte Daten genommen werden sollen
            blöcke:                     Integer,        Größe der Blöcke                                    
                                                        ! bei <=0 wird nicht geteilt
            tokens:                     Boolean,        Angabe ob neue Tokens aufgenommen werden sollen
            vorschau:                   Boolean,        Angabe ob Dataset verkürzt werden soll
            tokenhäufigkeitsminimum:    Integer,        Minimum, wie häufig Worte vorkommen müssen um in Tokenizer aufgenommen zu werden
            tokenhäufigkeitsmaximum:    Integer,        Maximum, wie häufig Worte vorkommen müssen um in Tokenizer aufgenommen zu werden
        Output:
            dataset,    Datenset mit lokalen Inhalten
            falls tokens == True:
              Autotokenizer,  angepasster Tokenizer;
              int,        Anzahl an Tokens, die zu dem Vokabular hinzugefügt wurden;
    '''
    ## Relevante Funktionen
    # Tokenisierungsfunktion
    def vorprozessierung(beispiele):
        return tokenizer(beispiele["text"])

    # Unterteilung in Blöcke
    def blockteilung(beispiele):
        # Texte konkatenieren
        konkateniert = {k: sum(beispiele[k], []) for k in beispiele.keys()}
        # Totale Länge setzen
        gesamtlänge = len(konkateniert[list(beispiele.keys())[0]])
        if gesamtlänge >= blöcke:
            gesamtlänge = (gesamtlänge // blöcke) * blöcke
        # Teile entsprechend der geforderten Blockgröße
        ergebnis = {
            k: [t[i : i + blöcke] for i in range(0, gesamtlänge, blöcke)]
            for k, t in konkateniert.items()
        }
        return ergebnis
        
    # Tokenliste erstellen
    def erhalte_tokens():
        # Versuche Daten einzulesen
        datei = open(pfad + name + kleiner + ".txt")
        dateitext = datei.read()
        datei.close()
        # Vokabeln herausfinden
        nlp = blank("de") 
        nlp.max_length = 9000000
        dokument = nlp(dateitext, disable=['parser', 'tagger', 'ner'])
        # Gesamttokendictionary erstellen
        tokens = {}
        for wort in dokument:
            if wort.text in tokens:
                tokens[wort.text] += 1
            else:
                tokens[wort.text] = 1
        # Relevante Tokens setzen       ! Sortierung ist überflüssig, kann aber bei Untersuchung des Koprus hilfreich sein
        relevant =[]
        for token in sorted(tokens, key=tokens.get, reverse=True):
            if tokens[token] > tokenhäufigkeitsminimum and tokens[token] < tokenhäufigkeitsmaximum:
                if token not in relevant:
                    relevant.append(token)
        return relevant
    
    kleiner = ""
    if (mod == None and klein) or (mod != None and "bielectra" in mod):
        kleiner = "_lower"

    # Dataset laden
    if teilen:
        if vorschau:
            dataset = load_dataset("text", data_files={"train": pfad + "train_" + name + kleiner + ".txt", "test": pfad + "eval_" + name + kleiner + ".txt"})
            dataset["train"] = dataset["train"].select(range(10))
            dataset["test"] = dataset["test"].select(range(3))
        else:
            dataset = load_dataset("text", data_files={"train": pfad + "train_" + name + kleiner + ".txt", "test": pfad + "eval_" + name + kleiner + ".txt"})
    else:
        if vorschau:
            dataset = load_dataset("text", data_files={pfad + name + kleiner + ".txt"})
            dataset["train"] = dataset["train"].select(range(10))
        else:
            dataset = load_dataset("text", data_files={pfad + name + kleiner + ".txt"})
            
    # Behandlung des Tokenizers
    if tokenizer != None:
        # dataset Tokenisieren
        dataset = dataset.map(
            vorprozessierung,
            batched = True,
            remove_columns = ['text'],
        )  
        # Tokens einfügen
        if tokens:
            # Vokabeln in Tokenizer einfügen
            num = tokenizer.add_tokens(erhalte_tokens())

    # Behandlung der Unterteilung in Blöcke
    if blöcke > 0:
        dataset = dataset.map(blockteilung, batched=True)

    if tokens:
        return dataset, tokenizer, num
    return dataset


def lese_InputExample (mod:str = None, datasetname:str = "deepset/germandpr", max_wortanzahl:int = 400, klein:bool = False, eval:bool = False, bez_frage:str = 'question', bez_pos:str = 'positive_ctxs', bez_neg:str = 'hard_negative_ctxs', vorschau:bool = False):
    '''
        Resultat als Liste aus Textprozess einlesen
        Input: 
            mod:            String,     Name des Modells                        ! ignoriert klein, falls mod gesetzt
            datasetname:    String,     Name des HuggingFace Datasets
            max_wortanzahl:            Integer,    Maximale Wortanzahl für Frage, Positiv und Negativ (zusammenaddiert)
            klein:          Boolean,    Angabe ob lower() auf Text angewendet werden soll
            eval:           Boolean,    Angabe ob Evaluierungsdaten aus "test" erstellt werden soll
            bez_frage:      String,     Bezeichner für die Frage
            bez_pos:        String,     Bezeichner für die korrekte Antwort
            bez_neg:      String,     Bezeichner für die falsche Antwort
            vorschau:   Boolean,        Angabe ob Dataset verkürzt werden soll
        Output:
            list,       Liste mit InputExamples für das Training
            Integer,    Anzahl der Listeneinträge
            falls tokens == True:
              dict,       Dictionary der Form {"Fragen": [], "positiv": [], "negativ": []} mit Einträgen für die Evaluierung;
              Integer,    Länge der Listen im Dictionary;
    '''
    # Variablen initialisieren und dataset laden
    kleiner = False
    if (mod == None and klein) or (mod != None and "bielectra" in mod):
        kleiner = True
    dataset = load_dataset(datasetname)

    train_bspe = []
    anzahl = 0

    if vorschau:
        länge = 10
        testlänge = 3
    else:
        länge = dataset['train'].num_rows
        testlänge = dataset['test'].num_rows


    # Jeden Eintrag in den Trainingsdaten durchgehen und Daten extrahieren...
    for i in range(länge):
        bsp = dataset['train'][i]
        anker = bsp[bez_frage]
        pos = bsp[bez_pos]["text"][0]
        neg = bsp[bez_neg]["text"][0]
        if kleiner:
            anker = anker.lower()
            pos = pos.lower()
            neg = neg.lower()
        if len(anker.split(" ")) + len(pos.split(" ")) + len(neg.split(" ")) < max_wortanzahl:
            train_bspe.append(InputExample(texts=[anker, pos, neg]))
            anzahl += 1

    if eval:
        eval_bspe = {"Fragen": [], "positiv": [], "negativ": []}
        evalanzahl = 0

        # Jeden Eintrag in den Testdaten durchgehen und Daten extrahieren...
        for i in range(testlänge):
            bsp = dataset['test'][i]
            anker = bsp[bez_frage]
            pos = bsp[bez_pos]["text"][0]
            neg = bsp[bez_neg]["text"][0]
            if kleiner:
                anker = anker.lower()
                pos = pos.lower()
                neg = neg.lower()
            if len(anker.split(" ")) + len(pos.split(" ")) + len(neg.split(" ")) < max_wortanzahl:
                eval_bspe["Fragen"].append(anker)
                eval_bspe["positiv"].append( pos )
                eval_bspe["negativ"].append( neg )
                evalanzahl += 1

        return train_bspe, anzahl, eval_bspe, evalanzahl
    return train_bspe, anzahl

