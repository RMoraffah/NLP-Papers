# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:13:54 2020

@author: nickg
"""

import json

def load_cosmos_unanswerable_questions(json_path):
    with open(json_path) as f:
        cosmos_qa_dict = json.load(f)
        
def load_squad_unanswerable_questions(json_path):
    with open(json_path) as f:
        squad_qa_dict = json.load(f)
        
# The job of the data loader is basically to load and stage data from the 
# parsed unanswerable qa json files and prepare it for model input. For each
# qa entity in the dataset, there is a (context, question, answer-list) triplet
# and we may want to paraphrase parts of any of these three elements in different
# ways depending on the data source.
class UnanswerableQADataHandler(object):
    def read_data(self): pass
    def gen_context_paraphrase_span_ind(self, qa_key): pass
    def gen_question_paraphrase_span_ind(self, qa_key): pass
    def gen_answer_paraphrase_span_ind(self, qa_key, answer_ind): pass
        
class CosmosQADataHandler(UnanswerableQADataHandler):
    def __init__(self, parsed_unanswerableqa_path):
        self.load_path = parsed_unanswerableqa_path
        self.quail_nei_str = "not enough information"
        
    def read_data(self):
        with open(self.load_path) as f:
            self.data_dict = json.load(f)
            
    def gen_context_paraphrase_span_ind(self, qa_key):
        #context = self.data_dict[qa_key]['context']
        return None
    
    def gen_question_paraphrase_span_ind(self, qa_key):
        question = self.data_dict[qa_key]['question']
        return (0,len(question))
    
    def gen_answer_paraphrase_span_ind(self, qa_key, answer_ind):
        answer = self.data_dict[qa_key]['answer'+str(answer_ind)]
        if self.quail_nei_str in answer:
            return None
        else:
            return (0,len(answer))
        
#class SquadQA_Data_Loader(UnanswerableQA_Data_Pipeline):
            
#load_cosmos_unanswerable_questions('cosmos_qa_train_unanswerable.json')
cosmos_handler = CosmosQADataHandler('../../../datasets/cosmos_qa/parsed_unanswerable/cosmos_qa_train_unanswerable.json')
cosmos_handler.read_data()
