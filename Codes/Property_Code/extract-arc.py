import glob
import json

file_ = glob.glob('./ARC-V1-Feb2018-2/ARC-Challenge/ARC-Challenge-Train.jsonl')[0]

with open(file_) as f:
  for line in f:
    arc_dic = json.loads(line)
    #print(arc_dic['question'])
    question = arc_dic['question']['stem']
    print(arc_dic)
    break
    if 'about' in question or 'regarding' in question:
        print(question)
        break
