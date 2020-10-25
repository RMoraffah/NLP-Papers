from textblob import TextBlob
import json
import random
import nltk
def duplicate_remove(answer_set, candidates):
    max_answer_set=4                                                            
    cnt=1                                                                       
    for can in candidates :                                                     
        if cnt==4 :                                                             
            break                                                               
        
        if can in answer_set:
            continue

        is_contained = [can for ans in answer_set if ans in can]
        if is_contained:
            continue
        if (can == "mr.") or (can == "ms."):
            continue
        answer_set.append(can)                                                  
    
        cnt+=1 
    return answer_set

def answer_generator(document, question, answer):
    answer_set = [answer[0].lower().encode("ascii", "ignore").decode()]
    span = answer[1][0]                                         

    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(document)
    candidates = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 

    #blob = TextBlob(document)                                                       
    #candidates = blob.noun_phrases                                                  

    candidates = [c.lower() for c in candidates if len(c) > 2]
    candidates = list(set(candidates))

    for ans in answer[0].split():                                                      
        if ans.lower() in candidates:                                                       
            list(filter((ans.lower()).__ne__, candidates))
    random.shuffle(candidates)
    answer_set = duplicate_remove(answer_set, candidates)
    
    return answer_set

def json_formmater(document, question, answer_set):
    gold_label = answer_set[0]
    random.shuffle(answer_set)
    answer = answer_set.index(gold_label)
    label_set ={"A":answer_set[0],"B":answer_set[1],"C":answer_set[2],"D":answer_set[3]}
    output_data={"Context":document,"Question":question,"Reasoning type":"coreference","Choices":label_set, "Answer":list(label_set)[answer]}
    return output_data

def pronoun_extractor(input_data):
    pronoun=['who', 'which']
    cnt=0
    output_data=[]
    for para in input_data:                                                       
        que = para['question.tokens']
        condition = [ bool(pn) for pn in pronoun if pn in que.lower()]
        if True in condition:
            doc = para['context.tokens']    
            doc = doc.encode("ascii", "ignore").decode()
            ans = para['answers']
            if ans[0].isnumeric() or len(ans[0])<=3:
                continue
            ans_set = answer_generator(doc, que, ans)
            output_data.append(json_formmater(doc, que, ans_set))
            cnt+=1 
            if cnt%100 == 0:
                print("--- Converting ",cnt," ---")
    print("Total :", cnt)

    return output_data
input_file = "data/narrative_dataset/dev.json"
with open(input_file,'r') as reader:                                          
    input_data = json.load(reader)
output_data=pronoun_extractor(input_data)
with open('valid.json', 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

input_file = "data/narrative_dataset/train.json"
with open(input_file,'r') as reader:                                          
    input_data = json.load(reader)
output_data=pronoun_extractor(input_data)
with open('train.json', 'w') as output_file:
    json.dump(output_data, output_file, indent=4)

