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
from datasets import load_dataset
import spacy


##############################################################################################################
##
##      Funktionen
##
##############################################################################################################

def preprocess_function(examples):
     return tokenizer(examples["text"])

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


##############################################################################################################
##
##      Programm
##
##############################################################################################################

#Initialisierung
dictlist = []
li = []
block_size = 128
z = 0

mod = "bielectra"

'''
    Daten laden
'''
# Modell laden
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

# Daten laden
if mod == "bielectra":
    p_d = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/plaintext_lower/"
else:
    p_d = "Vorbereitung/Daten/Kant-Abt1-TEI-vorlaeufig/normalized/plaintext/"
strdata = ""
df = []
for i in range(1,10):
    df.append(p_d + str(i) + "_string.txt")
    f = open(p_d + str(i) + "_string.txt")
    strdata += f.read()
    f.close()

dataset = load_dataset("text", data_files=df)


'''
    Tokenisierung der Daten
'''
# Vokabeln herausfinden
nlp = spacy.blank("de") 
nlp.max_length = 9000000
doc = nlp(strdata, disable=['parser', 'tagger', 'ner'])

tokens = {}
for word in doc:
    if word.text in tokens:
        tokens[word.text] += 1
    else:
        tokens[word.text] = 1

adto =[]
for w in sorted(tokens, key=tokens.get, reverse=True):
    if tokens[w] > 5 and tokens[w] < 1930:
        if w not in adto:
            adto.append(w)

# Vokabeln in Tokenizer einfügen
num = tokenizer.add_tokens(adto)

# Modelldimensionen anpassen
model.resize_token_embeddings(len(tokenizer))

# Tokenizer abspeichern
tokenizer.save_pretrained(o)


# Tokenisierung des Datensatzes            
tokenized = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset["train"].column_names,
)


'''
    Training der Daten
'''
# Daten in Blöcke unterteilen und Maskierungen einfügen
lm_dataset = tokenized.map(group_texts, batched=True)


data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

# Trainingsvorgaben setzen
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
    data_collator=data_collator
)

# Modell trainieren
trainer.train()

# Modell speichern
trainer.save_model(o)
