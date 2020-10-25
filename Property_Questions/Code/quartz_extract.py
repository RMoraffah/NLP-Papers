import glob
import json

file_ = glob.glob('./quartz-dataset-v1-aug2019/train.jsonl')[0]

with open(file_) as f:
  for line in f:
    quartz_dic = json.loads(line)
    question = quartz_dic['question']['stem']
    context = quartz_dic['para']
    choices = [c['text'] for c in quartz_dic['question']['choices']]
    answer = quartz_dic['answerKey']

    dataset = {}
    if '__' not in question:
        if 'about' in question or 'regarding' in question:
            dataset['context'] = context
            dataset['reasoning_type'] = 'property inference'
            dataset['question'] = question
            dataset['A'] = choices[0]
            dataset['B'] = choices[1]
            dataset['answer'] = answer
            json_dump = json.dumps(dataset)
            print(json_dump)
            #break
        #break
