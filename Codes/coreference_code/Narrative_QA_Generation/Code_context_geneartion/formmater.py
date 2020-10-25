import json
filename="train.json"
context=[]
with open("data/original/narrative_qa/"+filename, "r") as r:
    input_data = json.load(r)
    for para in input_data:
        context.append(para["Context"])
with open("data/raw_data/narrative_qa/narrative_train.txt", "w") as f:
    for para in context:
        f.write(para+"\n\n\n")

filename="valid.json"                                       
context=[]                                                                      
with open("data/original/narrative_qa/"+filename, "r") as r:                    
    input_data = json.load(r)                                                   
    for para in input_data:                                                     
        context.append(para["Context"])                                         
with open("data/raw_data/narrative_qa/narrative_train.txt", "w") as f:          
    for para in context:                                                        
        f.write(para+"\n\n\n") 
