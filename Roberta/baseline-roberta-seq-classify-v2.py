from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import RobertaConfig, RobertaModel
from create_dataset import create_dataset
import torch
import torch.nn as nn
import torch.optim as optim
import random
import time
import numpy as np

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base',num_labels=4, return_dict=True)

learning_rate=1e-3
optimizer = optim.Adam(model.parameters(),lr=learning_rate)

model.cuda()
     
# Dictionary for answer into numerical value
dic_ = {'A':0,'B':1,'C':2,'D':3}

# Get dataset
batch_size = 15
dataset = create_dataset()
batched_dataset = []
for index in range(int(len(dataset)/batch_size)):
    data_x,data_y = [],[]
    for data in dataset[int(index*batch_size):int((index*batch_size) + batch_size)]:
        context = data[0]
        question = data[1]
        a = data[2]
        b = data[3]
        c = data[4]
        d = data[5]
        answer = data[6]

        sentence = context + ' ' + question + '[SEP]' + a + '[SEP]' + b + '[SEP]' + c + '[SEP]' + d
        data_x.append(sentence) 
        data_y.append([dic_[answer]])
    
    data_x = tokenizer(data_x, padding=True, truncation=True ,return_tensors='pt')

    batched_dataset.append((data_x,data_y))

random.seed(123)
random.shuffle(batched_dataset)
# Train RobertaForSequenceClassification
model.train()
max_epoch = 50
total_epoch_loss = []
for epoch in range(max_epoch):
    epoch_loss = []
    start = time.time()
    for _,data in enumerate(batched_dataset):
        # Input data into model, alongside target
        inputs, target = data
        inputs['input_ids'] = inputs['input_ids'].cuda()
        inputs['attention_mask'] = inputs['attention_mask'].cuda()
        target = torch.LongTensor(target).cuda()
        outputs = model(**inputs, labels=target)
        loss = outputs.loss
        logits = outputs.logits
        epoch_loss.append(loss.item())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    end = time.time()
    epoch_loss = np.mean(epoch_loss)
    print(epoch, epoch_loss, 'epoch time:', end-start)
    total_epoch_loss.append(epoch_loss)
    # Save model
    model.save_pretrained("./models/roberta-batched-seq-classify-epoch-"+str(epoch)+'.model')
