from transformers import RobertaTokenizer, RobertaForSequenceClassification
from transformers import RobertaConfig, RobertaModel
from create_dataset import create_dataset
import torch

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForSequenceClassification.from_pretrained('roberta-base',num_labels=4, return_dict=True)

# Get dataset
dataset = create_dataset()
# Dictionary for answer into numerical value
dic_ = {'A':0,'B':1,'C':2,'D':3}

for data in dataset:
    context = data[0]
    question = data[1]
    a = data[2]
    b = data[3]
    c = data[4]
    d = data[5]
    answer = data[6]
    # Tokenize the Context/Question/[SEP]A/[SEP]B/[SEP]C/[SEP]D
    inputs = tokenizer(context + ' ' + question + '[SEP]' + a + '[SEP]' + b + '[SEP]' + c + '[SEP]' + d , return_tensors="pt")
    # Get the indices of the [SEP] in the new tokenized list
    indices = [i+1 for i, x in enumerate(inputs) if x == "[SEP]"]
    target = torch.LongTensor([dic_[answer]])
    outputs = model(**inputs, labels=target)
    loss = outputs.loss
    logits = outputs.logits
    print(loss.item())
    loss.backward()
    break