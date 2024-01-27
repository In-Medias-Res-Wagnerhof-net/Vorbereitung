### Training der Daten

## Import externer Bibliotheken
import re
from bs4 import BeautifulSoup as bs

from transformers import TrainingArguments
from datasets import Dataset
from transformers import AutoModelForCausalLM
from transformers import DistilBertModel
from trl import SFTTrainer


## Funktionen
def ladeTEI (num):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            num:    Integer,    Nummer des zu öffnenden Bandes
        Output:
            bs4.element,    Dateiinhalt
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    pfad = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/bearbeitet/" + str(num) + "_out.xml"

    # Versuche Datei zu öffnen
    try:
        f = open(pfad)
        tei = f.read()
        # Tags anpassen in Dateien 3 und 9 
        if num == 3 or num == 9:
            tei = re.sub(r"<tei:(.*?)>", r"<\1>", tei)
            tei = re.sub(r"</tei:(.*?)>", r"</\1>", tei)
        data = bs(tei, 'xml')
        f.close()
    # ... ansonsten: gebe Fehlermeldung aus
    except IOError:
        print("Die Datei konnte nicht geladen werden.")
        return
    
    return data


def satzextraktion (data):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            data:   bs4,    Beautiful Soup Element der zu bearbeitenden Datei 
                ! zu bearbeitende Textstellen sollten bereits mit id-tag ausgezeichnet sein
        Output:
            list,   Liste mit Stringelementen
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    ret = []

    # Lese alle Tags mit id aus
    for inh in data.find_all(id=True):
        
        # Alle Tags sollten eine Überschrift oder Absatz sein
        if inh.name == "h1" or inh.name == "h2" or inh.name == "h3" or inh.name == "h4" or inh.name == "h5" or inh.name == "p":
            t = str(inh)
            t = re.sub("\s+", " ", t)
            # Sonderbearbeitung der Überschriften
            if inh.name != "p":
                t = re.sub('<[^!].*?/?>', "", t)
            # Sonderbearbeitung der Absätze
            else:
                t = re.sub("<(.*?)>", "", t)
            t = re.sub("\s+", " ", t)
            t = t.strip()
            # Nichtleere Strings werden aufgenommen (leere Strings sollten eigentlich nicht vorkommen)
            if not t == " " and not t == "":
                    ret.append(t)
        # ... ansonsten: Probleme aufzeigen
        else:
            print("Es gab ein Problem mit den Inhalten eines Tags mit id. Sie hat nicht das geforderte Format (h1-5 oder p):")
            print(inh.name)
        
    return ret


## Programm

#Initialisierung
ps = satzextraktion(ladeTEI(1))
#p = ps[10]
#print(p)

li = []
z = 0

# Dataset erstellen
for p in ps:
    if "[head]" in p:
        print(p)
    else:
        li.append({"text": p, "label": "text"})
        z+=1
    #if z>10:
    #    break

print(li)
#print(ps[:10])

dataset = Dataset.from_list(li, split="train")

# Modell laden
#model = DistilBertModel.from_pretrained("Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased")
#o = "Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased-test"
model = AutoModelForCausalLM.from_pretrained("Vorbereitung/Modelle/deepset/gelectra-large-germanquad")
o = "Vorbereitung/Modelle/deepset/gelectra-large-germanquad-test"
#model = AutoModelForCausalLM.from_pretrained("Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased")
#o = "Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-test"

# Vorgaben machen
training_args = TrainingArguments(output_dir = o, per_device_train_batch_size = 4, per_device_eval_batch_size = 4 )

trainer = SFTTrainer(
    model,
    training_args,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=512
)

# Modell trainieren
trainer.train()

# Modell speichern
trainer.save_model(o)


'''
'''