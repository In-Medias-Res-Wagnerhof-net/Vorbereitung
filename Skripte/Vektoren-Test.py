### Test der Modelle im Terminal und Erstellung der Vektoren der Bände

import re
from bs4 import BeautifulSoup as bs

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def ladeTEI (num):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            pfad:   String, Pfad zu der zu öffnenden Datei
        Output:
            bs4.element.Tag,    Dateiinhalt
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    pfad = "Daten/Kant-Abt1-TEI-vorlaeufig/" + str(num) + "_out.xml"
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


def satzextraktion (data):
    """
        Gibt Datei als Beautiful Soup Element zurück
        Input: 
            pfad:   String, Pfad zu der zu öffnenden Datei
        Output:
            bs4.element.Tag,    Dateiinhalt
                ! Gibt es keinen Treffer, wird nur eine Fehlermeldung auf der Konsole ausgegeben
    """
    ret = []
    
    z=0
    for inh in data.find_all(id=True):
        
        if inh.name == "h1" or inh.name == "h2" or inh.name == "h3" or inh.name == "h4" or inh.name == "h5" or inh.name == "p":
            if inh.name != "p":
                t = str(inh)
                t = re.sub("\s+", " ", t)
                t = re.sub('<[^!].*?/?>', "", t)
                t = re.sub("\s+", " ", t)
                t = t.strip()
                if not t == " " and not t == "":
                    ret.append(t)
            else:
                t = str(inh)
                t = re.sub("\s+", " ", t)
                t = re.sub("<(.*?)>", "", t)
                t = re.sub("\s+", " ", t)
                t = t.strip()
                if not t == " " and not t == "":
                    ret.append(t)
        # Verzweigungen auflösen
        else:
            print("OOOOOOOOOOOOOOoooooooooooooooooh NEIN!!!")
            print(inh.name)
        
    return ret


docs = []
alldocs = []
end = 2                         # max: 10
for i in range(1,end):

    tei = ladeTEI(i)
    #print(tei)


    docs = satzextraktion(tei)

    print("****")
    alldocs.append(docs)

    #print(docs[0:44])
    print(len(docs))






mod = "bi-electra-ms-marco-german-uncased"

if mod == "gelectra-large-germanquad":
    bi_model = SentenceTransformer("deepset/gelectra-large-germanquad")
elif mod == "distilbert-base-german-cased":
    bi_model = SentenceTransformer("HuggingFace/distilbert-base-german-cased")
elif mod == "bi-electra-ms-marco-german-uncased":
    bi_model = SentenceTransformer("svalabs/bi-electra-ms-marco-german-uncased")
else:
    print("Es gab ein Problem beim Laden des Models...")
    exit()



K = 10 # number of top ranks to retrieve
# specify documents and queries
'''
docs = [
    "Auf Netflix gibt es endlich die neue Staffel meiner Lieblingsserie.",
    "Der Gepard jagt seine Beute.",
    "Wir haben in der Agentur ein neues System für Zeiterfassung.",
    "Mein Arzt sagt, dass mir dabei eher ein Orthopäde helfen könnte.",
    "Einen Impftermin kann mir der Arzt momentan noch nicht anbieten.",
    "Auf Kreta hat meine Tochter mit Muscheln eine schöne Sandburg gebaut.",
    "Das historische Zentrum (centro storico) liegt auf mehr als 100 Inseln in der Lagune von Venedig.",
    "Um in Zukunft sein Vermögen zu schützen, sollte man andere Investmentstrategien in Betracht ziehen.",
    "Die Ära der Dinosaurier wurde vermutlich durch den Einschlag eines gigantischen Meteoriten auf der Erde beendet.",
    "Bei ALDI sind die Bananen gerade im Angebot.",
    "Die Entstehung der Erde ist 4,5 milliarden jahre her.",
    "Finanzwerte treiben DAX um mehr als sechs Prozent nach oben Frankfurt/Main gegeben.",
    "DAX dreht ins Minus. Konjunkturdaten und Gewinnmitnahmen belasten Frankfurt/Main.",
]
'''


 # encode documents and queries
print("Erstelle/Speichere Korpus Model...")
for i in range(1,end):
    print("Band " + str(i))
    p = "Daten/Model/" + mod + "/" + str(i) + ".txt"
    try:
        if i == 1:
            features_docs = np.loadtxt(p)
        else:
            features_docs = np.concatenate((features_docs, np.loadtxt(p)))

    except IOError:
        print("Model wird erstellt")
        model = bi_model.encode(alldocs[i-1])
        if i == 1:
            features_docs = model
        else:
            features_docs = np.concatenate((features_docs, model))
        
        print("Model wird gespeichert")
        np.savetxt(p, model)


print("Bitte geben Sie einen Suchbegriff ein oder beenden Sie mit 'exit'!")
inp = input()
while( inp != "exit" ):
    
    queries = [
        inp
    ]

    print("Erstelle Text Vektoren...")

    features_queries = bi_model.encode(queries)

    #print(features_queries)

    # compute pairwise cosine similarity scores
    sim = cosine_similarity(features_queries, features_docs)

    # print results
    for i, query in enumerate(queries):
        ranks = np.argsort(-sim[i])
        print(sim[0,0])
        print("Query:", query)
        for j, r in enumerate(ranks[:K]):
            print(f"[{j}: {sim[i, r]: .3f}]", docs[r])
        print("-"*96)

    print("Bitte geben Sie einen neuen Suchbegriff ein oder beenden Sie mit 'exit'!")
    inp = input()


# Überschriften gesondert bearbeiten



"""
"""