##############################################################################################################
##############################################################################################################
###
###     Feintuning eines Sentencetransformermodells
###
##############################################################################################################
##############################################################################################################


##############################################################################################################
##
##      Import externer Bibliotheken
##
##############################################################################################################
from datasets import load_dataset
from sentence_transformers import SentenceTransformer, models, InputExample, losses, evaluation
from torch.utils.data import DataLoader
#import os


##############################################################################################################
##
##      Programm
##
##############################################################################################################

# OoM-Fehler (nicht genug Arbeitsspeicher) abwehren
# ! Achtung ! Kann Systemabsturz verursachen
#os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"


'''
    Vorgaben setzen
'''
dataset_id = "deepset/germandpr"        # Pfad zu Daten als Dataset
mod = "bielectra-tsdae"                 # Modell wählen
größe = 16                               # Batch Size setzen


'''
    Daten laden
'''
# Datenset laden
dataset = load_dataset(dataset_id)

# Modellinformationen setzen
if mod == "gelectra":
    model_name = "Vorbereitung/Modelle/deepset/gelectra-large-germanquad"
    o = "Vorbereitung/Modelle/deepset/gelectra-large-germanquad-fein"
elif mod == "convbert":
    model_name = "Vorbereitung/Modelle/dbmdz/convbert-base-german-europeana-cased"
    o = "Vorbereitung/Modelle/dbmdz/convbert-base-german-europeana-cased-fein"
elif mod == "distilbert":
    model_name = "Vorbereitung/Modelle/dbmdz/distilbert-base-german-europeana-cased"
    o = "Vorbereitung/Modelle/dbmdz/distilbert-base-german-europeana-cased-fein"
elif mod == "bielectra-tsdae":
    model_name = "Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-tsdae"
    o = "Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-tsdae-fein"
elif mod == "bielectra-tsdae-hwp":
    model_name = "Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-tsdae-hwp"
    o = "Vorbereitung/Modelle/svalabs/bi-electra-ms-marco-german-uncased-tsdae-hwp-fein"
else:
    print("Es gab ein Problem beim Laden des Modells...")
    exit()

# Modell laden
if "bielectra" in mod:
    # bereits existierendes Sentencetransformermodell laden
    model = SentenceTransformer(model_name, device='cpu', cache_folder=o + "/cache")
else:
    # Modell für die Worteinbettung laden, Dimensionen berechnen und daraus ein neues Sentencetransformermodell erstellen
    word_embedding_model = models.Transformer(model_name)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device='mps:0', cache_folder=o + "/cache")


'''
    Datenaufbereitung
'''
print("Datenaufbereitung --Anfang--")

# Trainingsdatenaufbereitung
train_bspe = []
anz = 0
# Jeden Eintrag durchgehen...
for i in range(dataset['train'].num_rows):
    bsp = dataset['train'][i]
    anker = bsp['question']
    pos = bsp['positive_ctxs']["text"][0]
    neg = bsp['hard_negative_ctxs']["text"][0]
    ges = anker
    if len(anker.split(" ")) + len(pos.split(" ")) + len(neg.split(" "))<400:
        train_bspe.append(InputExample(texts=[bsp['question'], pos, neg]))
        anz += 1


# Testdatenaufbereitung
ques = []
posl = []
negl = []
for i in range(dataset['test'].num_rows):
    example = dataset['test'][i]
    pos = example['positive_ctxs']["text"][0]
    neg = example['hard_negative_ctxs']["text"][0]
    if len(example['question'].split(" ")) + len(pos.split(" ")) + len(neg.split(" "))<400:
        ques.append(example['question'])
        posl.append( pos )
        negl.append( neg )

print("Datenaufbereitung --Ende--")


'''
    Modell anpassen
'''
# Vorgaben für das Anpassen des Models setzen
train_dataloader = DataLoader(train_bspe, batch_size=größe, shuffle=True)
train_loss = losses.TripletLoss(model=model)

evaluator = evaluation.TripletEvaluator(ques, posl,negl, 0, batch_size=größe)

if "bielectra" in mod:
    warm = 0
else:
    warm = int((anz/größe)/8)
   

# Model anpassen und speichern
model.fit(
    train_objectives=[(train_dataloader, train_loss)], 
    epochs=1, 
    evaluator=evaluator, 
    warmup_steps=warm, 
    evaluation_steps=5, 
    output_path=o, 
    checkpoint_save_steps=5,
    save_best_model=True )

model.save(o)