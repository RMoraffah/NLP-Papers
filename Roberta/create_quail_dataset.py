import glob
import json

dic_ = {"0":"A","1":"B","2":"C","3":"D"}

def create_dataset():

    train_dataset = []
    val_dataset = []
    test_dataset = []

    # Gather Train Questions
    file_ = glob.glob('./../QUAIL/train.jsonl')[0]
    with open(file_,'r') as f:
        for i,line in enumerate(f):
            d = []
            data = json.loads(line)
            context = data['context']
            #print(data['context'])
            d.append(context)
            question = data['question']
            #print(data['question'])
            d.append(question)
            for answer in data['answers']:
                #print(answer)
                d.append(answer)
            #print(data['correct_answer_id'])
            correct_answer = dic_[data['correct_answer_id']]
            d.append(correct_answer)
            train_dataset.append(d)

    # Gather Val Questions
    file_ = glob.glob('./../QUAIL/dev.jsonl')[0]
    with open(file_,'r') as f:
        for i,line in enumerate(f):
            d = []
            data = json.loads(line)
            context = data['context']
            #print(data['context'])
            d.append(context)
            question = data['question']
            #print(data['question'])
            d.append(question)
            for answer in data['answers']:
                #print(answer)
                d.append(answer)
            #print(data['correct_answer_id'])
            correct_answer = dic_[data['correct_answer_id']]
            d.append(correct_answer)
            val_dataset.append(d)

    # Gather Test Questions
    file_ = glob.glob('./../QUAIL/challenge.jsonl')[0]
    with open(file_,'r') as f:
        for i,line in enumerate(f):
            d = []
            data = json.loads(line)
            context = data['context']
            #print(data['context'])
            d.append(context)
            question = data['question']
            #print(data['question'])
            d.append(question)
            for answer in data['answers']:
                #print(answer)
                d.append(answer)
            #print(data['correct_answer_id'])
            correct_answer = dic_[data['correct_answer_id']]
            d.append(correct_answer)
            test_dataset.append(d)

    return train_dataset,val_dataset,test_dataset

#train,val,test = create_dataset()
#rint(len(train),len(val),len(test))