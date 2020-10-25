import json

with open("train.json", "r") as jr:
    dataset=json.load(jr)
    
with open("train_c.txt", "r") as c:
    context = c.readlines().split("\n\n\n")

with open("train_q.txt", "r") as q:
    question = q.readliens().split("\n\n\n")

merged=[]
for idx, instance in enumerate(dataset) :
    instance["Context"] = context[idx]
    instance["Question"] = question[idx]
    merged.append(instance)
with open("gen_train.json", "w") as jw:
    json.dump(merged, jw, indent=4)

                                                                                
with open("valid.json", "r") as jr:                                             
    dataset=json.load(jr)                                                       
                                                                                
with open("valid_c.txt", "r") as c:                                             
    context = c.readlines().split("\n\n\n")                                     
                                                                                
with open("valid_q.txt", "r") as q:                                             
    question = q.readliens().split("\n\n\n")                                    
                                                                                
merged=[]                                                                       
for idx, instance in enumerate(dataset) :                                       
    instance["Context"] = context[idx]                                          
    instance["Question"] = question[idx]                                        
    merged.append(instance)
with open("gen_valid.json", "w") as jw:                                     
    json.dump(merged, jw, indent=4)
