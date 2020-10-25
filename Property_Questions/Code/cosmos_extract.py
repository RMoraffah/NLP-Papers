import glob
import json
import re
file_ = glob.glob('train.csv')[0]
import csv
import json

dic_ = {0:'A',1:'B',2:'C',3:'D'}
with open(file_, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.__next__()
    for row in reader:
        #print(row)
        #print(len(row))
        context = row[1]
        question = row[2]
        answers = row[3:-1]
        correct = row[-1]
        #print(context)
        dataset = {}
        if 'about' in question or 'regarding' in question:
            dataset['context'] = context
            dataset['reasoning_type'] = 'property inference'
            dataset['question'] = question
            dataset['A'] = answers[0]
            dataset['B'] = answers[1]
            dataset['C'] = answers[2]
            dataset['D'] = answers[3]
            dataset['answer'] = dic_[int(correct)]
            json_dump = json.dumps(dataset)
            print(json_dump)
            #break
