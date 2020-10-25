import json
from googletrans import Translator                                              
                                                                                
trans = Translator()                                                            
quest = [] 
filename="data/train.json"
with open(filename, "r") as r:
    input_data = json.load(r)
    for para in input_data:
        quest.append(para["Question"])

with open("train_q.txt", "w") as f:
    for para in quest:
        fr = trans.translate(para, src='en', dest='fr')                                 
        en = trans.translate(fr.text, src='fr', dest='en')                              
        print(en.text)
        f.write(en.text+"\n\n\n")

filename="data/valid.json"
quest = []
with open(filename, "r") as r:
    input_data = json.load(r)
    for para in input_data:
        trans.append(para["Question"])

with open("valid_q.txt", "w") as f:
    for para in quest:
        fr = trans.translate(para, src='en', dest='fr')                                 
        en = trans.translate(fr.text, src='fr', dest='en')                              
        print(en.text)
        f.write(en.text+"\n\n\n")
