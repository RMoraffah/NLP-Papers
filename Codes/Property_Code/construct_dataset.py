import glob
import json
from googletrans import Translator

file_ = glob.glob('./dataset.jsonl')[0]

translator = Translator()

# Translate the Context

with open(file_,'r') as f, open('dataset-b.jsonl','w') as w:
  for line in f:
    data = json.loads(line)
    context = data['context']
    question = data['question']
    
    context_a = translator.translate(context, dest='de').text 
    context_b = translator.translate(context_a, dest='ja').text
    context_c = translator.translate(context_b, dest='en').text

    data['context'] = context_c
    json_dump = json.dumps(data)
    #print(json_dump)
    w.write(json_dump  +'\n')

# Translate the Question
with open('dataset-b.jsonl','r') as f, open('dataset-c.jsonl','w') as w:
  for line in f:
    data = json.loads(line)
    question = data['question']
    
    question_a = translator.translate(question, dest='de').text 
    question_b = translator.translate(question_a, dest='ja').text
    question_c = translator.translate(question_b, dest='en').text

    data['question'] = question_c
    json_dump = json.dumps(data )
    #print(json_dump)
    w.write(json_dump +'\n')

# Translate both the Context and question
with open('dataset-c.jsonl','r') as f, open('dataset-d.jsonl','w') as w:
  for line in f:
    data = json.loads(line)
    context = data['context']
    question = data['question']

    context_a = translator.translate(context, dest='de').text 
    context_b = translator.translate(context_a, dest='ja').text
    context_c = translator.translate(context_b, dest='en').text

    question_a = translator.translate(question, dest='de').text 
    question_b = translator.translate(question_a, dest='ja').text
    question_c = translator.translate(question_b, dest='en').text

    data['question'] = question_c
    data['context'] = context_c
    json_dump = json.dumps(data)
    #print(json_dump)
    w.write(json_dump +'\n')