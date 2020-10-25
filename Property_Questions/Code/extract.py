import glob
import json

file_ = glob.glob('train-v2.0.json')[0]

with open(file_) as f:
  data = json.load(f)

#print(len(data['data']))
for dat in data['data'][0]['paragraphs']:
    #print(dat['qas'])
    for qa in dat['qas']:
        #print(qa)
        #print(qa['question'])
        if 'about' in qa['question'] or 'regarding' in qa['question']:
            print(qa['question'])
