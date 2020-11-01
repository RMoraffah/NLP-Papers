from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import RobertaConfig, RobertaModel
from create_dataset import create_dataset
import torch
import torch.nn as nn
import torch.optim as optim

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base',num_labels=4, return_dict=True)

learning_rate=1e-3
optimizer = optim.Adam(model.parameters(),lr=learning_rate)

model.cuda()
     
# Dictionary for answer into numerical value
dic_ = {'A':0,'B':1,'C':2,'D':3}

# Get dataset
batch_size = 32
dataset = create_dataset()

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
    target = torch.LongTensor([dic_[answer]]).cuda()
    # Input data into model, alongside target
    outputs = model(**inputs, labels=target)
    loss = outputs.loss
    logits = outputs.logits
    print(loss.item())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if i > 5:
        break