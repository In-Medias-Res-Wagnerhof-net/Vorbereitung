### Training der Daten

import re
from bs4 import BeautifulSoup as bs

from transformers import TrainingArguments
from datasets import Dataset
from transformers import AutoModelForCausalLM
from transformers import DistilBertModel
from trl import SFTTrainer



def ladeTEI (num):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            pfad:   String, Pfad zu der zu öffnenden Datei
        Output:
            bs4.element.Tag,    Dateiinhalt
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    pfad = "Daten/Kant-Abt1-TEI-vorlaeufig/" + str(num) + ".xml"
    try:
        f = open(pfad)
        tei = f.read()
        if num == 3 or num == 9:
            tei = re.sub(r"<tei:(.*?)>", r"<\1>", tei)
            tei = re.sub(r"</tei:(.*?)>", r"</\1>", tei)
        data = bs(tei, 'xml')
        f.close()

    except IOError:
        print("Die Datei konnte nicht geladen werden.")
        return
    
    return data

def durchsucheDIV (xml):
    """
        Unterteilung der Dateien in Texte und Textteile
        Input: 
            xml: bs4.element.Tag,   Dateiinhalt
        Output:
            list, Liste der Kapitel als Beautiful Soup Formatierung
                ! Gibt es keinen Treffer, wird ein leerer String zurückgegeben
    """
    res = [""]
    if xml == None:
        print("---None---") 
        return None
    
    for child in xml:
        if child.name == "div" and child.has_attr("n"):
            res.append( durchsucheDIV(child) )
        elif child != "\n":
            res[0] += str(child)
    return res

def satzextraktion (data, head=1):
    """
        Unterteilung der Daten in Satz
        Input: 
            data:   Liste,      durchsucheDIV - Ergebnis
            head:   Integer,    Umgang mit Überschriften
                    0:  weglassen
                    1:  mit Auszeichnung und mit Kommentaren übernehmen
                    2:  mit Auszeichnung und ohne Kommentaren übernehmen
                    3:  ohne Auszeichnung und ohne Kommentaren übernehmen
                    ! Standardmäßig wird sie mit Auszeichnung übernommen
                    ! Wenn keine genannte Zahl gesetzt wird, wird weggelassen
        Output:
            Liste, Liste mit Sätzen
                ! Gibt es keinen Treffer, wird ein leerer String zurückgegeben
    """
    docs = []
    for dat in data:
        if (type(dat)==list):
            x = satzextraktion(dat, head)
            for y in x:
                docs.append(y)
        else:
            temp = dat
            temp = re.split("<p>", temp)
            for t in temp:
                if re.search("<head>", t) and head != 3:
                    if head == 1 or head == 2:
                        t = re.sub("\s+", " ", t)
                        if head == 1:
                            t = re.sub('<[^!].*?/?>', "", t)
                        else:
                            t = re.sub("<.*?>", "", t)
                        t = re.sub("\s+", " ", t)
                        t = "[head]" + t.strip()
                        #print (t)
                    else:
                        t = ""
                else:
                    t = re.sub("\s+", " ", t)
                    t = re.sub("<.*?>", "", t)
                    t = re.sub("\s+", " ", t)
                    #t = re.sub("(\d+). ", "\1 ", t)            # Ziffer wird entfernt????
                    t = t.strip()
                if not t == " " and not t == "":
                    docs.append(t)
    
    return docs



ps = satzextraktion(durchsucheDIV(ladeTEI(1).body), 2)

li = []

z = 0

for p in ps:
    if "[head]" in p:
        print(p)
    else:
        li.append({"text": p, "label": "text"})
        z+=1
    if z>10:
        break

print(li)
#print(ps[:10])

dataset = Dataset.from_list(li, split="train")

#model = DistilBertModel.from_pretrained("HuggingFace/distilbert-base-german-cased")
#o = "HuggingFace/distilbert-base-german-cased-test"
print(dataset)
model = AutoModelForCausalLM.from_pretrained("deepset/gelectra-large-germanquad")
o = "deepset/gelectra-large-germanquad-test"
#model = AutoModelForCausalLM.from_pretrained("svalabs/bi-electra-ms-marco-german-uncased")


training_args = TrainingArguments(output_dir = o, per_device_train_batch_size = 4, per_device_eval_batch_size = 4 )


trainer = SFTTrainer(
    model,
    training_args,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=512
)

trainer.train()

trainer.save_model(o)