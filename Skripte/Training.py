##############################################################################################################
##############################################################################################################
###
###     Training der Daten
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################

import re
from bs4 import BeautifulSoup as bs

from transformers import TrainingArguments, AutoModelForMaskedLM, AutoTokenizer, DataCollatorForLanguageModeling, Trainer
from datasets import Dataset, load_dataset
#from trl import SFTTrainer


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################

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
        Unterteilung der Daten in Absätze
        Input: 
            data:   bs4,    Beautiful Soup Element der zu bearbeitenden Datei 
                ! zu bearbeitende Textstellen sollten bereits mit id-tag ausgezeichnet sein
        Output:
            list,   Liste mit Stringelementen (den Absätzen)
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    # Initialisierungen
    ret = []
    z = 0
    # Lese alle Tags mit id aus
    for inh in data.find_all(id=True):
        
        # Alle Tags sollten eine Überschrift oder Absatz sein
        if inh.name == "h1" or inh.name == "h2" or inh.name == "h3" or inh.name == "h4" or inh.name == "h5" or inh.name == "p":
            t = str(inh)
            t = re.sub("\s+", " ", t)
            # Absätze die nur fremdsprachlichen Text, nur Datum oder nur röm. Ziffern beinhalten werden entfernt
            temp = re.sub("<foreign(.*?)>(.*?)</foreign>", "", t)
            temp = re.sub("<num rendition=\"#roman\"(.*?)>(.*?)</num>", "", temp)
            temp = re.sub("<date(.*?)>(.*?)</date>", "", temp)
            temp = re.sub("<(.*?)>", "", temp)
            temp = re.sub("\s+", " ", temp)
            if temp == " " or temp == "":
                t = ""
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


##############################################################################################################
##
##      Programm
##
##############################################################################################################

#Initialisierung
ps = satzextraktion(ladeTEI(2))
#p = ps[:10]
#print(p)

dictlist = []
li = []
block_size = 128
z = 0
# Modell laden
mod = "distilbert"

if mod == "gelectra":
    model = AutoModelForMaskedLM.from_pretrained("Vorbereitung/Modelle/deepset/gelectra-large-germanquad")
    o = "Vorbereitung/Modelle/deepset/gelectra-large-germanquad-test"
    tokenizer = AutoTokenizer.from_pretrained("Vorbereitung/Modelle/deepset/gelectra-large-germanquad")
elif mod == "distilbert":
    model = AutoModelForMaskedLM.from_pretrained("Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased")
    o = "Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased-test"
    tokenizer = AutoTokenizer.from_pretrained("Vorbereitung/Modelle/HuggingFace/distilbert-base-german-cased")
elif mod == "bielectra":
    model = AutoModelForMaskedLM.from_pretrained("Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased")
    o = "Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-test"
    tokenizer = AutoTokenizer.from_pretrained("Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased")
else:
    print("Es gab ein Problem beim Laden des Modells...")
    exit()

text = ""
"""
'''
# Trainingsdaten erstellen
for p in ps:
    if len(re.split(" ", p))<200 and len(re.split(" ", p))>5:
        li.append(p)
        dictlist.append({"text": p})
        z += 1
    elif len(re.split(" ", p))>=200:
        sep = ".!?"
        t = ""
        i = ""
        j = ""
        for b in p:
            if b in sep and not (b in "." and j in " "):
                t += b
                if len(re.split(" ", t))>5:
                    li.append(t)
                    dictlist.append({"text": t})
                    t = ""
                    z += 1
                else:
                    t = ""
            else:
                t += b
            j = i
            i = b
    if z > 10:
        break
'''
text = " ".join(ps)

f = open("Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/bearbeitet/2_string.txt", "a")
f.write(text)
f.close()
"""


dataset = load_dataset("text", data_files=["Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/bearbeitet/1_string.txt", "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/bearbeitet/2_string.txt"])
print(dataset)
#dataset = Dataset.from_list(dictlist, split="train[:5000]")

def preprocess_function(examples):
     return tokenizer(examples["text"])
            
tokenized = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset["train"].column_names,
)

#print(dataset["train"])
#print(tokenized["train"]['input_ids'])



def group_texts(examples):
    #print(examples)
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
    # customize this part to your needs.
    if total_length >= block_size:
        total_length = (total_length // block_size) * block_size
    # Split by chunks of block_size.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    return result

lm_dataset = tokenized.map(group_texts, batched=True)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

training_args = TrainingArguments(
    output_dir = o,
    evaluation_strategy = "epoch",
    learning_rate = 2e-5,
    num_train_epochs = 3,
    weight_decay = 0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=lm_dataset["train"],
    eval_dataset=lm_dataset["train"],
    data_collator=data_collator,
)

trainer.train()
# Modell speichern
trainer.save_model(o)

'''
#print(z)
#print(li[100:105])
#print(ps[:10])

#dataset = Dataset.from_list(li, split="train")  
DataCollatorForLanguageModeling

tokenized = tokenizer(li, return_tensors="pt", padding=True)
print(tokenized)

# Modell trainieren
outputs = model(**inputs)
print(outputs)

# Modell speichern
model.save_pretrained(o)
print("Modell gespeichert")



# Vorgaben machen
training_args = Seq2SeqTrainingArguments( output_dir = o )
#per_device_train_batch_size = 4, per_device_eval_batch_size = 4

trainer = Seq2SeqTrainer(
    model,
    training_args,
    train_dataset=li
)

# Modell trainieren
trainer.train()

# Modell speichern
trainer.save_model(o)


'''