from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import RobertaConfig, RobertaModel
from create_quail_dataset import create_dataset
import torch
import torch.nn as nn
import torch.optim as optim
import random
import time
import numpy as np
import sys

model_path = sys.argv[1]
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained(model_path, return_dict=True)

learning_rate=1e-3
optimizer = optim.Adam(model.parameters(),lr=learning_rate)

model.cuda()
     
# Dictionary for answer into numerical value
dic_ = {'A':0,'B':1,'C':2,'D':3}

# Get Test Dataset
batch_size = 5
_,_,dataset = create_dataset()
# Turn model into eval mode
model.eval()

correct = 0
incorrect = 0
total = 0
for i,data in enumerate(dataset):
    context = data[0]
    question = data[1]
    a = data[2]
    b = data[3]
    c = data[4]
    d = data[5]
    answer = data[6]
    # Tokenize the Context/Question/[SEP]A/[SEP]B/[SEP]C/[SEP]D
    inputs = tokenizer(context + ' ' + question + '[SEP]' + a + '[SEP]' + b + '[SEP]' + c + '[SEP]' + d , return_tensors="pt")
    # Turn inputs and attentino masks into cuda
    inputs['input_ids'] = inputs['input_ids'].cuda()
    inputs['attention_mask'] = inputs['attention_mask'].cuda()
    # Target as LongTensor and into cuda
    target = dic_[answer]
    # Input data into model
    outputs = model(**inputs)
    logits = outputs.logits
    #print(logits.size())
    if (torch.argmax(logits).item() == target):
        correct += 1
    else:
        incorrect += 1
    total += 1

print('Accuracy: ', float(correct/total))
