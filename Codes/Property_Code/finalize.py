import glob
import json
from googletrans import Translator

translator = Translator()

with open('dataset-final.jsonl','r') as f, open('dataset-final-2.jsonl','w') as w:
  for line in f:
    data = json.loads(line)
    
    if 'C' not in data.keys():
        a = translator.translate(data['A'], dest='de').text 
        b = translator.translate(a, dest='ja').text
        c = translator.translate(b, dest='en').text
        data['C'] = c
    if 'D' not in data.keys():
        a = translator.translate(data['A'], dest='de').text 
        b = translator.translate(a, dest='ja').text
        c = translator.translate(b, dest='en').text
        data['D'] = c 

    json_dump = json.dumps(data)
    #print(json_dump)
    w.write(json_dump  +'\n')
