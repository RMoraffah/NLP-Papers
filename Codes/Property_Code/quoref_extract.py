import glob
import json

file_ = glob.glob('./quoref-train-dev-v0.1/quoref-train-v0.1.json')[0]

with open(file_) as f:
    content = f.read()
    quoref_dic = json.loads(content)
    for i,dat in enumerate(quoref_dic['data']):
        for par in dat['paragraphs']:
            #print(par)
            for qa in par['qas']:
                question = qa['question']
                dataset = {}
                if 'about' in question or 'regarding' in question:
                    #print(par)
                    question
                    #break
    '''
    if '__' not in question:
        if 'about' in question or 'regarding' in question:
            print(question)
        #break
    '''
