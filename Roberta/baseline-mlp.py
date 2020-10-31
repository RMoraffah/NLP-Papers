from transformers import EncoderDecoderModel, BertTokenizer
import torch
import torch.nn as nn
import torch.nn.functional as F
from create_dataset import create_dataset

# NOTE: NEED ~/.conda/envs/pytorch-1.51-gpu/ activated
# NOTE: Baseline Model <=> Pretrained BERT + MLP
# NOTE: Input is Context/Question/[SEP]A/[SEP]B/[SEP]C/[SEP]D
# NOTE: Output of BERT model of tokenized input is inputed into an MLP that
#       output which [SEP] token associated with an answer is the correct answer.


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# initialize Bert2Bert from pre-trained checkpoints
model = EncoderDecoderModel.from_encoder_decoder_pretrained('bert-base-uncased', 'bert-base-uncased')

# MLP Model Delcaration
class MLP(nn.Module):

    def __init__(self):
        super(MLP,self).__init__()
        self.linear = nn.Linear(30522,2)

    def forward(self,x):
        return torch.softmax(torch.sigmoid(self.linear(x)),dim=1)

# Cross Entropy Loss for training
ce_loss = nn.CrossEntropyLoss()
# Initialization of MLP 
mlp = MLP()
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
    token = tokenizer.tokenize(context + ' ' + question + '[SEP]' + a + '[SEP]' + b + '[SEP]' + c + '[SEP]' + d )
    # Get the indices of the [SEP] in the new tokenized list
    indices = [i+1 for i, x in enumerate(token) if x == "[SEP]"]
    # Use the indices and the index [SEP] for the correct answer
    target = [0.0]*(len(token)+2)
    target[indices[dic_[answer]]] = 1.0
    target = torch.LongTensor(target)
    # Input the tokenized input into a torch input
    input_ids = torch.tensor(tokenizer.encode(token, add_special_tokens=True)).unsqueeze(0)
    ##print(token,len(token))
    ##print(indices, answer,dic_[answer])
    output = model(input_ids=input_ids, decoder_input_ids=input_ids, return_dict=True)
    ##print(token,len(token))
    ##print(output['logits'].size())
    # Go from one batch to input into MLP in one shot
    output = output['logits'].squeeze()
    output = mlp(output)
    # Calculate loss
    loss = ce_loss(output,target)
    # Print loss
    print(loss.item())
    # TODO: loss.backward()
    break

