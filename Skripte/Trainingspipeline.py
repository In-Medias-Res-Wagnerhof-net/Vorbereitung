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
from transformers import DataCollatorForLanguageModeling, TrainingArguments, Trainer
from sentence_transformers import losses, evaluation, datasets
from torch.utils.data import DataLoader
import math
from Training_functions import *

import nltk
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')
    

##############################################################################################################
##
##      Programm
##
##############################################################################################################
# Initialisierung
vorschau = False
größe = 8

modellnamen = ["bielectra", "distilbert", "convbert", "gelectra"]


## Alle Modelle durchgehen
for mod in modellnamen:
    print("######################################################################")
    print("# " + mod)
    print("######################################################################")
    '''
        Initiales Training
    '''
    print("-----------------------------------------------------------------------")
    print("Initiales Training")


    print("Modell laden...")
    modell, tokenisierer, rückgabe = lade_modell(mod)

    # Testen ob Modell schon existiert
    try:
        open(rückgabe + "/config.json")
        training = False
        print("Training wurde bereits ausgeführt!")
    except:
        training = True

    if training == True:
        print("Daten laden...")
        dataset = lese_dataset(tokenisierer, mod, teilen=True, vorschau=vorschau)
        tokenisierer.save_pretrained(rückgabe)

        print("Training starten...")
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenisierer, mlm_probability=0.15)

        # Vorgaben für das Anpassen des Models setzen
        training_args = TrainingArguments(
            output_dir = rückgabe,
            evaluation_strategy = "epoch",
            learning_rate = 2e-5,
            num_train_epochs = 5,
            weight_decay = 0.1,
            per_device_train_batch_size=größe, 
            gradient_accumulation_steps=4,
            save_total_limit = 3,
            save_strategy = "epoch",
            load_best_model_at_end=True
        )

        trainer = Trainer(
            model=modell,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["test"],
            data_collator=data_collator
        )

        # Model anpassen und speichern
        eval_results = trainer.evaluate()
        print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")
        trainer.train()

        eval_results = trainer.evaluate()
        print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")

        trainer.save_model(rückgabe)

    '''
        Feintuning
    '''
    print("-----------------------------------------------------------------------")
    print("Feintuning")
    modt = mod + "-training"
    print("Modell laden...")
    modell, rückgabe = lade_modell(modt, "fein", typ="SentenceTransformer", device="cpu")

    # Testen ob Modell schon existiert
    try:
        open(rückgabe + "/config.json")
        training = False
        print("Training wurde bereits ausgeführt!")
    except:
        training = True

    if training == True:
        print("Daten laden...")
        train_bspe, train_anzahl, eval_bspe, dicanz = lese_InputExample(modt, eval=True, vorschau=vorschau)

        print("Training starten...")
        # Vorgaben für das Anpassen des Models setzen
        train_dataloader = DataLoader(train_bspe, batch_size=größe, shuffle=True)
        train_loss = losses.TripletLoss(model=modell)

        evaluator = evaluation.TripletEvaluator(eval_bspe["Fragen"], eval_bspe["positiv"], eval_bspe["negativ"], 0, batch_size=größe)

        if "bielectra" in mod:
            warm = 0
        else:
            warm = int((train_anzahl/größe)/8)
        
        # Model anpassen und speichern
        modell.fit(
            train_objectives=[(train_dataloader, train_loss)], 
            epochs=5, 
            evaluator=evaluator, 
            evaluation_steps=train_anzahl/größe,
            warmup_steps=warm, 
            weight_decay = 0.1,
            output_path=rückgabe,
            checkpoint_path=rückgabe, 
            checkpoint_save_steps=train_anzahl/größe,
            checkpoint_save_total_limit=3,
            save_best_model=True
        )
        


    '''
        TSDAE Training
    '''
    if mod != "distilbert" and mod != "convbert":
        print("-----------------------------------------------------------------------")
        print("TSDAE Training")
        print("Modell laden...")
        modell, rückgabe, modellname = lade_modell(mod, "tsdae", "SentenceTransformer", name=True)

        # Testen ob Modell schon existiert
        try:
            open(rückgabe + "/config.json")
            training = False
            print("Training wurde bereits ausgeführt!")
        except:
            training = True

        if training == True:
            print("Daten laden...")
            sätze = lese_datalisten(mod, vorschau=vorschau,)

            # Daten korumpieren
            train_dataset = datasets.DenoisingAutoEncoderDataset(sätze)

            print("Training starten...")
            # Vorgaben für das Anpassen des Models setzen
            train_dataloader = DataLoader(train_dataset, batch_size=größe)

            train_loss = losses.DenoisingAutoEncoderLoss(
                modell, decoder_name_or_path=modellname, tie_encoder_decoder=True
            )

            # Model anpassen und speichern
            modell.fit(
                train_objectives=[(train_dataloader, train_loss)], 
                epochs=1, 
                weight_decay = 0,
                scheduler="constantlr",
                optimizer_params={"lr": 3e-5},
                output_path=rückgabe,
                checkpoint_path=rückgabe, 
                checkpoint_save_total_limit=3,
                save_best_model=True
            )



        '''
            TSDAE Feintuning
        '''
        print("-----------------------------------------------------------------------")
        print("TSDAE Feintuning")
        modt = mod + "-tsdae"
        print("Modell laden...")
        modell, rückgabe = lade_modell(modt, "fein", typ="SentenceTransformer", device="cpu")

        # Testen ob Modell schon existiert
        try:
            open(rückgabe + "/config.json")
            training = False
            print("Training wurde bereits ausgeführt!")
        except:
            training = True

        if training == True:
            print("Daten laden...")
            train_bspe, train_anzahl, eval_bspe, dicanz = lese_InputExample(modt, eval=True, vorschau=vorschau)

            print("Training starten...")
            # Vorgaben für das Anpassen des Models setzen
            train_dataloader = DataLoader(train_bspe, batch_size=größe, shuffle=True)
            train_loss = losses.TripletLoss(model=modell)

            evaluator = evaluation.TripletEvaluator(eval_bspe["Fragen"], eval_bspe["positiv"], eval_bspe["negativ"], 0, batch_size=größe)

            if "bielectra" in mod:
                warm = 0
            else:
                warm = int((train_anzahl/größe)/8)
            

            # Model anpassen und speichern
            modell.fit(
                train_objectives=[(train_dataloader, train_loss)], 
                epochs=5, 
                evaluator=evaluator, 
                evaluation_steps=train_anzahl/größe,
                warmup_steps=warm, 
                weight_decay = 0.1,
                output_path=rückgabe,
                checkpoint_path=rückgabe, 
                checkpoint_save_steps=train_anzahl/größe,
                checkpoint_save_total_limit=3,
                save_best_model=True
            )



        '''
            TSDAE Training auf feintuned
        '''
        print("-----------------------------------------------------------------------")
        print("TSDAE Training")
        print("Modell laden...")
        modt = mod + "-training-fein"
        modell, rückgabe, modellname = lade_modell(modt, "tsdae", "SentenceTransformer", stexist=True, name=True)

        # Testen ob Modell schon existiert
        try:
            open(rückgabe + "/config.json")
            training = False
            print("Training wurde bereits ausgeführt!")
        except:
            training = True

        if training == True:
            print("Daten laden...")
            sätze = lese_datalisten(mod, vorschau=vorschau,)

            # Daten korumpieren
            train_dataset = datasets.DenoisingAutoEncoderDataset(sätze)

            print("Training starten...")
            # Vorgaben für das Anpassen des Models setzen
            train_dataloader = DataLoader(train_dataset, batch_size=größe)

            train_loss = losses.DenoisingAutoEncoderLoss(
                modell, decoder_name_or_path=modellname, tie_encoder_decoder=True
            )

            # Model anpassen und speichern
            modell.fit(
                train_objectives=[(train_dataloader, train_loss)], 
                epochs=1, 
                weight_decay = 0,
                scheduler="constantlr",
                optimizer_params={"lr": 3e-5},
                output_path=rückgabe,
                checkpoint_path=rückgabe, 
                checkpoint_save_total_limit=3,
                save_best_model=True
            )