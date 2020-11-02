import glob
import json

def create_dataset():

    final_dataset = []

    # Gather Causality Questions
    file_ = glob.glob('./../Causality Questions/Causality_Data_Final.json')[0]
    with open(file_,'r') as f:
        dataset = json.loads(f.read())
        for key in dataset:
            #print(dataset[key])
            d = []
            context = dataset[key]['Context']
            d.append(context)
            #print(context)
            question = dataset[key]['Question']
            d.append(question)
            #print(question)
            for choice in dataset[key]['Choices']:
                #print(choice,dataset[key]['Choices'][choice])
                d.append(dataset[key]['Choices'][choice])
            answer = dataset[key]['Answer']
            d.append(answer)
            #print(answer)
            final_dataset.append(d)

    #print('----------')
    # Gather Property Questions
    file_ = glob.glob('./../Property_Questions/dataset-final.json')[0]
    with open(file_,'r') as f:
        for line in f:
            d = []
            data = json.loads(line)
            context = data['context']
            d.append(context)
            #print(context)
            question = data['question']
            d.append(question)
            #print(question)
            A = data['A']
            d.append(A)
            #print(A)
            B = data['B']
            d.append(B)
            #print(B)
            C = data['C']
            d.append(C)
            #print(C)
            D = data['D']
            d.append(D)
            #print(D)
            answer = data['answer']
            d.append(answer)
            #print(answer)
            final_dataset.append(d)

    #print('----------')

    # Gather Coreference Questions
    file_ = glob.glob('./../coreference_data/extracted/filtered_narrativei_train.json')[0]
    with open(file_,'r') as f:
        dataset = json.loads(f.read())
        for i in range(len(dataset)):
            d = []
            context = dataset[i]['Context']
            d.append(context)
            #print(context)
            question = dataset[i]['Question']
            d.append(question)
            #print(question)
            for choice in dataset[i]['Choices']:
                #print(choice,dataset[i]['Choices'][choice])
                d.append(dataset[i]['Choices'][choice])
            answer = dataset[i]['Answer']
            d.append(answer)
            #print(answer)
            final_dataset.append(d)
    #print('----------')

    # Gather Unanswerable Questions
    file_ = glob.glob('./../unanswerable_qa/unanswerable_qa.json')[0]
    with open(file_,'r') as f:
        content = f.read()
        content = content.strip('[')
        content = content.strip(']')
        content = content.replace('}, {', '}[JSON_SEP]{')
        content = content.split('[JSON_SEP]')
        for con in content:
            d = []
            data = json.loads(con)
            context = data['Context']
            d.append(context)
            #print(context)
            question = data['Question']
            #print(question)
            d.append(question)
            for choice in data['Choices']:
                #print(choice,data['Choices'][choice])
                d.append(data['Choices'][choice])
            answer = data['Answer']
            d.append(answer)
            #print(answer)
            final_dataset.append(d)
    #print('----------')

    # Gather Sequential Questions
    file_ = glob.glob('./../SequentialDataset/SequentailData.json')[0]
    with open(file_,'r') as f:
        dataset = json.loads(f.read())
        for key in dataset:
            d = []
            context = dataset[key]['Context']
            d.append(context)
            #print(context)
            question = dataset[key]['Question']
            d.append(question)
            #print(question)
            A = dataset[key]['A']
            d.append(A)
            #print(A)
            B = dataset[key]['B']
            d.append(B)
            #print(B)
            C = dataset[key]['C']
            d.append(C)
            #print(C)
            D = dataset[key]['D']
            d.append(D)
            #print(D)
            answer = dataset[key]['Answer']
            d.append(answer)
            #print(answer)
            final_dataset.append(d)
    #print('----------')
    return final_dataset

create_dataset()