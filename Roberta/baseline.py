from transformers import EncoderDecoderModel, BertTokenizer
import torch

# NOTE: NEED ~/.conda/envs/pytorch-1.51-gpu/ activated

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#token = tokenizer.encode("Hello, my dog is cute", add_special_tokens=True)
token = tokenizer.tokenize("Hello, my dog is cute")
print(token)
token = tokenizer.encode(token, add_special_tokens=True)
print(token)
'''
model = EncoderDecoderModel.from_encoder_decoder_pretrained('bert-base-uncased', 'bert-base-uncased') # initialize Bert2Bert from pre-trained checkpoints

# forward
input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute", add_special_tokens=True)).unsqueeze(0)  # Batch size 1
outputs = model(input_ids=input_ids, decoder_input_ids=input_ids, return_dict=True)
print(outputs['logits'].size())
'''